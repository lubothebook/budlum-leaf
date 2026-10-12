"""Tests of the manifest tool: the good path, tampering and rollback.

Run: python3 -m unittest discover -s fw/boot/tests -v
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import leaffw as L  # noqa: E402


def world(**kw):
    return L.demo_world(**kw)


def run(w):
    return L.verify(w["env"], w["images"], w["trust"], w["state"], w["chain"])


def resign(w):
    """Re-sign the manifest with the threshold of release keys."""
    env = L.envelope(w["env"]["manifest"])
    for k in w["release_keys"][:w["trust"]["threshold"]]:
        env = L.release_sign(env, k)
    w["env"] = env
    w["chain"]["release_hash"] = L.release_hash(env["manifest"])
    w["chain"]["release_seq"] = env["manifest"]["release_seq"]
    return w


class GoodPath(unittest.TestCase):
    def test_accept(self):
        r = run(world())
        self.assertEqual(r.decision, "ACCEPT", r.findings)
        self.assertEqual(r.install, "NEW")
        self.assertTrue(all(v == "PASS" for v in r.chips.values()))

    def test_release_hash_is_stable(self):
        a, b = world(), world()
        self.assertEqual(L.release_hash(a["env"]["manifest"]),
                         L.release_hash(b["env"]["manifest"]))

    def test_repair_same_release(self):
        w = world()
        w["state"]["installed_release_seq"] = 7
        w["state"]["installed_release_hash"] = L.release_hash(w["env"]["manifest"])
        r = run(w)
        self.assertEqual(r.decision, "ACCEPT", r.findings)
        self.assertEqual(r.install, "REPAIR")

    def test_merkle_single_chunk_and_odd(self):
        self.assertEqual(len(L.chunk_leaves(b"")), 1)
        leaves = L.chunk_leaves(b"x" * (3 * L.CHUNK + 1))
        self.assertEqual(len(leaves), 4)
        self.assertEqual(len(L.merkle_root(leaves[:3])), 32)


class Tampering(unittest.TestCase):
    def test_flip_one_byte_in_a_blob(self):
        w = world()
        d = bytearray(w["images"]["U2A.bin"])
        d[123_456] ^= 0x01
        w["images"]["U2A.bin"] = bytes(d)
        r = run(w)
        self.assertEqual(r.decision, "REFUSE")
        self.assertIn("sha256 mismatch", r.chips["U2A"])
        self.assertEqual(r.chips["U6"], "PASS")
        ref = L.demo_blob("U2A", "7.0", len(d))
        self.assertEqual(L.locate_tamper(bytes(d), ref), 123_456 // L.CHUNK)

    def test_truncated_blob(self):
        w = world()
        w["images"]["U4.bin"] = w["images"]["U4.bin"][:-1]
        r = run(w)
        self.assertIn("B4 size", r.chips["U4"])

    def test_missing_blob(self):
        w = world()
        del w["images"]["U3.bin"]
        self.assertIn("image missing", run(w).chips["U3"])

    def test_extra_file_in_image_set(self):
        w = world()
        w["images"]["payload.bin"] = b"\x90" * 64
        r = run(w)
        self.assertEqual(r.decision, "REFUSE")
        self.assertTrue(any("payload.bin" in f for f in r.findings))

    def test_manifest_field_edit_breaks_release_signature(self):
        w = world()
        w["env"]["manifest"]["blobs"][0]["svn"] += 1
        w["chain"]["release_hash"] = L.release_hash(w["env"]["manifest"])
        r = run(w)
        self.assertTrue(any(f.startswith("M2") and "needed" in f
                            for f in r.findings))

    def test_swapped_blob_with_matching_digest_needs_vendor(self):
        """An attacker rewrites a blob and its digests, and re-signs with
        release keys it holds. The vendor signature still fails."""
        w = world()
        evil = b"\x00" * 4096
        e = w["env"]["manifest"]["blobs"][0]
        e.update(size=len(evil), sha256=L.sha256(evil).hex(),
                 merkle_root=L.merkle_root(L.chunk_leaves(evil)).hex())
        w["images"][e["file"]] = evil
        resign(w)
        r = run(w)
        self.assertIn("B2 vendor signature fails", r.chips[e["chip"]])

    def test_vendor_key_of_other_chip(self):
        w = world()
        e = w["env"]["manifest"]["blobs"][0]
        other = w["vendor_keys"]["U5"]
        w["env"]["manifest"]["blobs"][0] = L.vendor_sign(e, other)
        resign(w)
        self.assertIn("B2", run(w).chips[e["chip"]])

    def test_below_threshold(self):
        w = world()
        w["env"]["signatures"] = w["env"]["signatures"][:2]
        r = run(w)
        self.assertEqual(r.decision, "REFUSE")
        self.assertTrue(any("2 valid release signatures" in f for f in r.findings))

    def test_duplicate_signature_counts_once(self):
        w = world()
        w["env"]["signatures"] = [w["env"]["signatures"][0]] * 3
        self.assertEqual(run(w).decision, "REFUSE")

    def test_unknown_release_key(self):
        w = world()
        stranger = L.Ed25519PrivateKey.from_private_bytes(b"\x07" * 32)
        w["env"]["signatures"] = w["env"]["signatures"][:2]
        w["env"] = L.release_sign(w["env"], stranger)
        r = run(w)
        self.assertEqual(r.decision, "REFUSE")
        self.assertTrue(any("unknown key" in f for f in r.findings))

    def test_domain_separation_vendor_sig_is_not_release_sig(self):
        """A vendor signature over the release hash bytes does not count."""
        w = world()
        k = w["release_keys"][0]
        rh = bytes.fromhex(L.release_hash(w["env"]["manifest"]))
        forged = k.sign(L.TAG_VENDOR + rh).hex()
        w["env"]["signatures"] = [{"key_id": L.key_id(L.pub_hex_of(k)),
                                   "sig": forged}]
        w["trust"]["threshold"] = 1
        self.assertEqual(run(w).decision, "REFUSE")

    def test_chain_hash_mismatch(self):
        w = world()
        w["chain"]["release_hash"] = "11" * 32
        r = run(w)
        self.assertTrue(any(f.startswith("M3") for f in r.findings))

    def test_revoked(self):
        w = world()
        w["chain"]["revoked"] = [L.release_hash(w["env"]["manifest"])]
        self.assertTrue(any("revoked" in f for f in run(w).findings))

    def test_wrong_product(self):
        w = world()
        w["trust"]["product"] = "leaf-80"
        self.assertTrue(any(f.startswith("M1") for f in run(w).findings))

    def test_missing_required_chip(self):
        w = world()
        w["trust"]["required_chips"].append("U9")
        self.assertTrue(any("U9" in f for f in run(w).findings))


class Rollback(unittest.TestCase):
    def test_older_release_refused(self):
        w = world()
        w["state"]["installed_release_seq"] = 8
        r = run(w)
        self.assertTrue(any("older than the installed" in f for f in r.findings))

    def test_release_floor_from_chain(self):
        w = world()
        w["chain"]["floor_release_seq"] = 8
        self.assertTrue(any("under the floor" in f for f in run(w).findings))

    def test_same_seq_other_hash(self):
        w = world()
        w["state"]["installed_release_seq"] = 7
        self.assertTrue(any("different hash" in f for f in run(w).findings))

    def test_chip_svn_below_floor(self):
        w = world()
        w["state"]["floor_svn"]["U5"] = 4
        r = run(w)
        self.assertIn("rollback", r.chips["U5"])
        self.assertEqual(r.chips["U6"], "PASS")

    def test_old_signed_release_replayed(self):
        """Release 6 was valid once. After release 7 commits, 6 is refused,
        even with valid signatures and a matching old chain record."""
        old = world(release_seq=6, floor_release_seq=5, version="6.0",
                    svn=2, floor_svn=2)
        new = world()
        st = L.commit(new["state"], new["env"], trial_passed=True)
        old["state"] = st
        r = run(old)
        self.assertEqual(r.decision, "REFUSE")
        self.assertTrue(any("older than the installed" in f for f in r.findings))

    def test_commit_raises_floor_to_floor_svn_only(self):
        w = world(svn=5, floor_svn=3)
        st = L.commit(w["state"], w["env"], trial_passed=True)
        self.assertEqual(st["floor_svn"]["U2A"], 3)
        self.assertEqual(st["installed_release_seq"], 7)
        self.assertEqual(st["floor_release_seq"], 5)

    def test_failed_trial_does_not_raise_floors(self):
        w = world(svn=5, floor_svn=5)
        st = L.commit(w["state"], w["env"], trial_passed=False)
        self.assertEqual(st, w["state"])

    def test_floor_never_drops(self):
        w = world(svn=5, floor_svn=1)
        w["state"]["floor_svn"]["U1"] = 4
        st = L.commit(w["state"], w["env"], trial_passed=True)
        self.assertEqual(st["floor_svn"]["U1"], 4)

    def test_make_entry_rejects_floor_above_svn(self):
        with self.assertRaises(ValueError):
            L.make_entry("U1", b"x", vendor="v", version="1", svn=1,
                         floor_svn=2, measure="direct", store="s", file="f")


class BootAttest(unittest.TestCase):
    def test_attest(self):
        w = world()
        m = w["env"]["manifest"]
        meas = {e["chip"]: e["merkle_root"] for e in m["blobs"]}
        meas["U2B"] = "ab" * 32
        del meas["U3"]
        out = L.attest(m, meas, w["state"])
        self.assertEqual(out["U2B"], "MISMATCH")
        self.assertEqual(out["U3"], "NO_REPORT")
        self.assertEqual(out["U6"], "PASS")


class Cli(unittest.TestCase):
    def test_demo_and_verify_cli(self):
        tool = os.path.join(os.path.dirname(HERE), "leaffw.py")
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable, tool, "demo", d], check=True,
                           capture_output=True)
            args = [os.path.join(d, n) for n in
                    ("manifest.json", "images", "trust.json", "state.json",
                     "chain.json")]
            ok = subprocess.run([sys.executable, tool, "verify", *args],
                                capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stdout)
            p = os.path.join(d, "images", "U6.bin")
            with open(p, "r+b") as f:
                f.seek(10)
                f.write(b"\xff")
            bad = subprocess.run([sys.executable, tool, "verify", *args],
                                 capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)
            self.assertIn("U6", json.loads(bad.stdout)["chips"])
            self.assertNotEqual(json.loads(bad.stdout)["chips"]["U6"], "PASS")


if __name__ == "__main__":
    unittest.main()
