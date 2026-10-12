#!/usr/bin/env python3
"""leaffw.py - the Budlum Leaf firmware manifest reference tool.

Firmware-Integrity team, revision L.6.0. Directory fw/boot/.

What it does
    build    hash every vendor blob, cut it into 4 KiB chunks, build the
             Merkle root of the chunks and write an unsigned manifest
    vsign    the vendor signs one blob entry (chip, version, svn, digest)
    sign     one Budlum release key adds its signature to the envelope
    hash     print the release hash that the governance vote records on chain
    verify   check an envelope and a device image set against the trust
             roots of U7, the U7 state (the anti-rollback floors) and the
             finalised chain record. Prints a per-chip verdict.
    commit   apply a confirmed release to the U7 state (raise the floors)
    keygen   make an ed25519 key pair (reference only, no HSM)
    demo     build a full example in a directory and verify it

Cryptography
    ed25519 (RFC 8032) through the `cryptography` package, SHA-256 as in the
    Budlum tree (`sha2`). Every hash and signature carries a domain tag.
    The production manifest adds an ML-DSA-87 release signature next to the
    ed25519 one. This reference checks the ed25519 half only. [HYPOTHESIS]

The encoding is canonical JSON: sorted keys, no spaces, UTF-8. The
production U7 format is a fixed binary record. This tool is the oracle that
the U7 code is tested against.
"""
import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)

# --------------------------------------------------------------- the tags ---
TAG_MANIFEST = b"BDLM_LEAF_FW_MANIFEST_V1"      # release key signature
TAG_RELEASE = b"BDLM_LEAF_FW_RELEASE_V1"        # the on-chain release hash
TAG_VENDOR = b"BDLM_LEAF_FW_VENDOR_BLOB_V1"     # vendor signature of a blob
TAG_LEAF = b"BDLM_LEAF_FW_CHUNK_LEAF_V1"        # Merkle leaf (one chunk)
TAG_NODE = b"BDLM_LEAF_FW_CHUNK_NODE_V1"        # Merkle inner node
TAG_KEYID = b"BDLM_LEAF_FW_KEY_ID_V1"           # key identifier

FORMAT = "budlum-leaf-fw-manifest/1"
CHUNK = 4096
MEASURE_METHODS = ("self-rom", "direct", "dice", "owner-key+scrub",
                   "handshake")


# ------------------------------------------------------------- utilities ---
def canon(obj) -> bytes:
    """Canonical JSON bytes: sorted keys, no whitespace, UTF-8."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256(*parts: bytes) -> bytes:
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
    return h.digest()


def u32(n: int) -> bytes:
    return n.to_bytes(4, "big")


def u64(n: int) -> bytes:
    return n.to_bytes(8, "big")


def key_id(pub_hex: str) -> str:
    return sha256(TAG_KEYID, bytes.fromhex(pub_hex)).hex()[:16]


def pub_hex_of(priv: Ed25519PrivateKey) -> str:
    return priv.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()


def priv_from_hex(h: str) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(h))


def priv_to_hex(k: Ed25519PrivateKey) -> str:
    return k.private_bytes(serialization.Encoding.Raw,
                           serialization.PrivateFormat.Raw,
                           serialization.NoEncryption()).hex()


def ed_verify(pub_hex: str, sig_hex: str, msg: bytes) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(
            bytes.fromhex(sig_hex), msg)
        return True
    except (InvalidSignature, ValueError):
        return False


# ---------------------------------------------------------- Merkle chunks ---
def chunk_leaves(data: bytes, chunk: int = CHUNK):
    n = max(1, (len(data) + chunk - 1) // chunk)
    return [sha256(TAG_LEAF, u32(i), data[i * chunk:(i + 1) * chunk])
            for i in range(n)]


def merkle_root(leaves):
    level = list(leaves)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            if i + 1 < len(level):
                nxt.append(sha256(TAG_NODE, level[i], level[i + 1]))
            else:
                nxt.append(level[i])          # an odd node is promoted
        level = nxt
    return level[0]


def first_bad_chunk(data: bytes, expected_leaves):
    """Index of the first chunk whose leaf differs, or None."""
    got = chunk_leaves(data)
    for i in range(max(len(got), len(expected_leaves))):
        if i >= len(got) or i >= len(expected_leaves) or got[i] != expected_leaves[i]:
            return i
    return None


# ------------------------------------------------------- the blob entries ---
def vendor_message(entry: dict) -> bytes:
    """What a vendor signs: the chip, its version, its svn and the digests."""
    return (TAG_VENDOR + b"|" + entry["chip"].encode() + b"|" +
            entry["version"].encode() + b"|" + u64(entry["svn"]) + b"|" +
            bytes.fromhex(entry["sha256"]) + bytes.fromhex(entry["merkle_root"]))


def make_entry(chip: str, data: bytes, *, vendor: str, version: str, svn: int,
               floor_svn: int, measure: str, store: str, file: str) -> dict:
    if measure not in MEASURE_METHODS:
        raise ValueError(f"unknown measure method {measure!r}")
    if not 0 <= floor_svn <= svn:
        raise ValueError("floor_svn must lie in [0, svn]")
    return {
        "chip": chip, "vendor": vendor, "version": version, "svn": svn,
        "floor_svn": floor_svn, "size": len(data), "chunk": CHUNK,
        "sha256": sha256(data).hex(),
        "merkle_root": merkle_root(chunk_leaves(data)).hex(),
        "measure": measure, "store": store, "file": file, "vendor_sig": "",
    }


def vendor_sign(entry: dict, vendor_priv: Ed25519PrivateKey) -> dict:
    e = dict(entry)
    e["vendor_sig"] = vendor_priv.sign(vendor_message(e)).hex()
    return e


# ------------------------------------------------------- the manifest ---
def make_manifest(product: str, release_seq: int, floor_release_seq: int,
                  entries) -> dict:
    if not 0 <= floor_release_seq <= release_seq:
        raise ValueError("floor_release_seq must lie in [0, release_seq]")
    chips = [e["chip"] for e in entries]
    if len(set(chips)) != len(chips):
        raise ValueError("one entry per chip")
    return {"format": FORMAT, "product": product, "release_seq": release_seq,
            "floor_release_seq": floor_release_seq,
            "blobs": sorted(entries, key=lambda e: e["chip"])}


def release_hash(manifest: dict) -> str:
    """The 32-byte hash that the governance record carries on chain."""
    return sha256(TAG_RELEASE, canon(manifest)).hex()


def manifest_message(manifest: dict) -> bytes:
    return TAG_MANIFEST + bytes.fromhex(release_hash(manifest))


def envelope(manifest: dict) -> dict:
    return {"manifest": manifest, "signatures": []}


def release_sign(env: dict, priv: Ed25519PrivateKey) -> dict:
    pub = pub_hex_of(priv)
    sig = priv.sign(manifest_message(env["manifest"])).hex()
    out = {"manifest": env["manifest"],
           "signatures": [s for s in env["signatures"]
                          if s["key_id"] != key_id(pub)]}
    out["signatures"].append({"key_id": key_id(pub), "sig": sig})
    out["signatures"].sort(key=lambda s: s["key_id"])
    return out


# ----------------------------------------------------- the verification ---
@dataclass
class Report:
    decision: str = "ACCEPT"                 # ACCEPT or REFUSE
    install: str = "NEW"                     # NEW, REPAIR or n/a
    findings: list = field(default_factory=list)
    chips: dict = field(default_factory=dict)  # chip -> PASS or reason

    def refuse(self, code: str, text: str):
        self.decision = "REFUSE"
        self.findings.append(f"{code}: {text}")

    def to_dict(self):
        return {"decision": self.decision, "install": self.install,
                "findings": self.findings, "chips": self.chips}


def verify(env: dict, images: dict, trust: dict, state: dict,
           chain: dict) -> Report:
    """Check a signed manifest and an image set.

    env     the envelope {manifest, signatures}
    images  {file name: bytes} of the inactive slot, or of a staged set
    trust   the U7 roots: product, release_keys, threshold, vendor_keys,
            required_chips
    state   the U7 state: installed_release_seq, installed_release_hash,
            floor_release_seq, floor_svn {chip: n}
    chain   the finalised governance record that U7 proved: release_hash,
            release_seq, floor_release_seq, revoked [hashes]
    """
    r = Report()
    m = env.get("manifest", {})

    # M1 the format and the product
    if m.get("format") != FORMAT:
        r.refuse("M1", f"unknown format {m.get('format')!r}")
        return r
    if m.get("product") != trust["product"]:
        r.refuse("M1", f"product {m.get('product')!r} is not "
                       f"{trust['product']!r}")

    # M2 the release signatures: threshold of distinct, known keys
    rh = release_hash(m)
    msg = manifest_message(m)
    known = {key_id(p): p for p in trust["release_keys"]}
    good = set()
    for s in env.get("signatures", []):
        pub = known.get(s.get("key_id"))
        if pub is None:
            r.findings.append(f"M2: signature by unknown key {s.get('key_id')}")
            continue
        if ed_verify(pub, s.get("sig", ""), msg):
            good.add(s["key_id"])
        else:
            r.findings.append(f"M2: bad signature by key {s['key_id']}")
    if len(good) < trust["threshold"]:
        r.refuse("M2", f"{len(good)} valid release signatures, "
                       f"{trust['threshold']} needed")

    # M3 the chain: the release hash is the finalised one, and not revoked
    if rh in chain.get("revoked", []):
        r.refuse("M3", "the release hash is revoked on chain")
    if chain.get("release_hash") != rh:
        r.refuse("M3", "the release hash differs from the finalised record")
    elif chain.get("release_seq") != m["release_seq"]:
        r.refuse("M3", "the release sequence differs from the finalised record")

    # M4 the release-level rollback rules
    floor_rs = max(state.get("floor_release_seq", 0),
                   chain.get("floor_release_seq", 0))
    if m["release_seq"] < floor_rs:
        r.refuse("M4", f"release_seq {m['release_seq']} is under the "
                       f"floor {floor_rs}")
    inst = state.get("installed_release_seq", 0)
    if m["release_seq"] < inst:
        r.refuse("M4", f"release_seq {m['release_seq']} is older than the "
                       f"installed {inst}")
    elif m["release_seq"] == inst:
        if rh == state.get("installed_release_hash"):
            r.install = "REPAIR"
        else:
            r.refuse("M4", "same release_seq with a different hash")

    # M5 coverage: every required chip, and nothing unknown
    names = {e["chip"] for e in m["blobs"]}
    for c in trust["required_chips"]:
        if c not in names:
            r.refuse("M5", f"required chip {c} has no entry")
    files = {e["file"] for e in m["blobs"]}
    for f in sorted(images):
        if f not in files:
            r.refuse("M5", f"file {f} in the image set is not in the manifest")

    # B1..B4 per blob
    for e in m["blobs"]:
        c = e["chip"]
        why = []
        vk = trust["vendor_keys"].get(c)
        if vk is None:
            why.append("B1 no vendor key for this chip")
        elif not ed_verify(vk, e.get("vendor_sig", ""), vendor_message(e)):
            why.append("B2 vendor signature fails")
        if e.get("measure") not in MEASURE_METHODS:
            why.append("B1 unknown measure method")
        if not 0 <= e["floor_svn"] <= e["svn"]:
            why.append("B3 floor_svn is above svn")
        floor = state.get("floor_svn", {}).get(c, 0)
        if e["svn"] < floor:
            why.append(f"B3 rollback: svn {e['svn']} < floor {floor}")
        data = images.get(e["file"])
        if data is None:
            why.append("B4 image missing")
        else:
            if len(data) != e["size"]:
                why.append(f"B4 size {len(data)} != {e['size']}")
            if sha256(data).hex() != e["sha256"]:
                why.append("B4 sha256 mismatch")
            if merkle_root(chunk_leaves(data)).hex() != e["merkle_root"]:
                why.append("B4 Merkle root mismatch")
        r.chips[c] = "PASS" if not why else "; ".join(why)
        if why:
            r.refuse("B", f"{c}: {'; '.join(why)}")
    if r.decision == "REFUSE":
        r.install = "n/a"
    return r


def locate_tamper(data: bytes, reference: bytes):
    """Which 4 KiB chunk differs. U6 does this inline during a download."""
    return first_bad_chunk(data, chunk_leaves(reference))


# --------------------------------------------- the boot-time attestation ---
def attest(manifest: dict, measurements: dict, state: dict) -> dict:
    """Compare chip measurements with the installed manifest.

    measurements: {chip: merkle_root hex} as reported at boot (DICE report,
    direct U7 hash, or the dead-pad handshake). Returns {chip: PASS|reason}.
    """
    out = {}
    for e in manifest["blobs"]:
        c = e["chip"]
        got = measurements.get(c)
        if got is None:
            out[c] = "NO_REPORT"
        elif got != e["merkle_root"]:
            out[c] = "MISMATCH"
        elif e["svn"] < state.get("floor_svn", {}).get(c, 0):
            out[c] = "ROLLBACK"
        else:
            out[c] = "PASS"
    return out


# ------------------------------------------------------------- commit ---
def commit(state: dict, env: dict, trial_passed: bool) -> dict:
    """Apply a release to the U7 state after the trial boot.

    The floors rise only when the trial boot passed. A floor rises to the
    manifest floor_svn, not to svn, so the previous slot stays bootable
    unless the release names a security fix.
    """
    if not trial_passed:
        return dict(state)
    m = env["manifest"]
    s = json.loads(json.dumps(state))
    s["installed_release_seq"] = m["release_seq"]
    s["installed_release_hash"] = release_hash(m)
    s["floor_release_seq"] = max(s.get("floor_release_seq", 0),
                                 m["floor_release_seq"])
    fl = s.setdefault("floor_svn", {})
    for e in m["blobs"]:
        fl[e["chip"]] = max(fl.get(e["chip"], 0), e["floor_svn"])
    return s


# ---------------------------------------------------------------- I/O ---
def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write("\n")


def load_images(d):
    out = {}
    for n in sorted(os.listdir(d)):
        p = os.path.join(d, n)
        if os.path.isfile(p):
            with open(p, "rb") as f:
                out[n] = f.read()
    return out


# ------------------------------------------------------------- the demo ---
DEMO_CHIPS = [
    # chip,  vendor,          size,     measure,           store
    ("U1", "tcon-vendor", 256 * 1024, "direct", "boot-nor"),
    ("U2A", "wifi-vendor", 4 * 1024 * 1024, "dice", "boot-nor"),
    ("U2B", "mmw-vendor", 1536 * 1024, "dice", "boot-nor"),
    ("U3", "audio-vendor", 128 * 1024, "direct", "boot-nor"),
    ("U4", "pmic-vendor", 32 * 1024, "direct", "u4-otp-patch"),
    ("U5", "modem-vendor", 2 * 1024 * 1024, "owner-key+scrub", "u5-nand"),
    ("U6", "decoder-vendor", 1024 * 1024, "dice", "boot-nor"),
    ("U7", "se-vendor", 384 * 1024, "self-rom", "u7-internal"),
    ("U8", "imu-vendor", 16 * 1024, "direct", "boot-nor"),
    ("QN", "qi-vendor", 64 * 1024, "handshake", "quadrant-flash"),
]
# The demo modem blob is 2 MiB to keep the tests fast. The planned size is
# 48 MiB (chips.json); the size does not change the logic.


def demo_blob(chip: str, version: str, size: int) -> bytes:
    seed = sha256(b"demo", chip.encode(), version.encode())
    out = bytearray()
    while len(out) < size:
        seed = sha256(seed)
        out += seed
    return bytes(out[:size])


def demo_world(release_seq=7, floor_release_seq=5, svn=3, floor_svn=2,
               version="7.0", n_release=5, threshold=3, seed=b"leaf"):
    """Deterministic keys, blobs, trust, state and chain for tests."""
    def k(name):
        return Ed25519PrivateKey.from_private_bytes(sha256(seed, name.encode()))
    rel = [k(f"release-{i}") for i in range(n_release)]
    vend = {c: k(f"vendor-{v}") for c, v, *_ in DEMO_CHIPS}
    images, entries = {}, []
    for c, v, size, meas, store in DEMO_CHIPS:
        data = demo_blob(c, version, size)
        fn = f"{c}.bin"
        images[fn] = data
        e = make_entry(c, data, vendor=v, version=version, svn=svn,
                       floor_svn=floor_svn, measure=meas, store=store, file=fn)
        entries.append(vendor_sign(e, vend[c]))
    m = make_manifest("leaf-160", release_seq, floor_release_seq, entries)
    env = envelope(m)
    for p in rel[:threshold]:
        env = release_sign(env, p)
    trust = {"product": "leaf-160",
             "release_keys": [pub_hex_of(p) for p in rel],
             "threshold": threshold,
             "vendor_keys": {c: pub_hex_of(p) for c, p in vend.items()},
             "required_chips": [c for c, *_ in DEMO_CHIPS]}
    state = {"installed_release_seq": release_seq - 1,
             "installed_release_hash": "00" * 32,
             "floor_release_seq": floor_release_seq - 1,
             "floor_svn": {c: floor_svn - 1 for c, *_ in DEMO_CHIPS}}
    chain = {"release_hash": release_hash(m), "release_seq": release_seq,
             "floor_release_seq": floor_release_seq, "revoked": []}
    return {"env": env, "images": images, "trust": trust, "state": state,
            "chain": chain, "release_keys": rel, "vendor_keys": vend}


# ---------------------------------------------------------------- CLI ---
def cmd_keygen(a):
    k = Ed25519PrivateKey.generate()
    save_json(a.out, {"private": priv_to_hex(k), "public": pub_hex_of(k),
                      "key_id": key_id(pub_hex_of(k))})
    print(f"wrote {a.out} key_id={key_id(pub_hex_of(k))}")


def cmd_build(a):
    """spec.json: {product, release_seq, floor_release_seq, blobs: [{chip,
    vendor, version, svn, floor_svn, measure, store, file}]}"""
    spec = load_json(a.spec)
    entries = []
    for b in spec["blobs"]:
        with open(os.path.join(a.images, b["file"]), "rb") as f:
            data = f.read()
        entries.append(make_entry(b["chip"], data, vendor=b["vendor"],
                                  version=b["version"], svn=b["svn"],
                                  floor_svn=b["floor_svn"],
                                  measure=b["measure"], store=b["store"],
                                  file=b["file"]))
    m = make_manifest(spec["product"], spec["release_seq"],
                      spec["floor_release_seq"], entries)
    save_json(a.out, envelope(m))
    print(f"wrote {a.out}, {len(entries)} blobs, unsigned")


def cmd_vsign(a):
    env = load_json(a.envelope)
    k = priv_from_hex(load_json(a.key)["private"])
    for i, e in enumerate(env["manifest"]["blobs"]):
        if e["chip"] == a.chip:
            env["manifest"]["blobs"][i] = vendor_sign(e, k)
            env["signatures"] = []   # the manifest changed: re-sign
            save_json(a.envelope, env)
            print(f"vendor signed {a.chip}; release signatures cleared")
            return 0
    print(f"no entry for chip {a.chip}", file=sys.stderr)
    return 2


def cmd_sign(a):
    env = load_json(a.envelope)
    env = release_sign(env, priv_from_hex(load_json(a.key)["private"]))
    save_json(a.envelope, env)
    print(f"{len(env['signatures'])} release signatures")


def cmd_hash(a):
    print(release_hash(load_json(a.envelope)["manifest"]))


def cmd_verify(a):
    r = verify(load_json(a.envelope), load_images(a.images),
               load_json(a.trust), load_json(a.state), load_json(a.chain))
    print(json.dumps(r.to_dict(), indent=1))
    return 0 if r.decision == "ACCEPT" else 1


def cmd_commit(a):
    s = commit(load_json(a.state), load_json(a.envelope), a.trial_passed)
    save_json(a.state, s)
    print(json.dumps(s, indent=1, sort_keys=True))


def cmd_demo(a):
    w = demo_world()
    os.makedirs(os.path.join(a.dir, "images"), exist_ok=True)
    for n, d in w["images"].items():
        with open(os.path.join(a.dir, "images", n), "wb") as f:
            f.write(d)
    for n in ("trust", "state", "chain"):
        save_json(os.path.join(a.dir, f"{n}.json"), w[n])
    save_json(os.path.join(a.dir, "manifest.json"), w["env"])
    r = verify(w["env"], w["images"], w["trust"], w["state"], w["chain"])
    print(f"demo in {a.dir}: release hash {release_hash(w['env']['manifest'])}")
    print(json.dumps(r.to_dict(), indent=1))
    return 0 if r.decision == "ACCEPT" else 1


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("keygen"); s.add_argument("out"); s.set_defaults(f=cmd_keygen)
    s = sp.add_parser("build"); s.add_argument("spec"); s.add_argument("images")
    s.add_argument("out"); s.set_defaults(f=cmd_build)
    s = sp.add_parser("vsign"); s.add_argument("envelope"); s.add_argument("chip")
    s.add_argument("key"); s.set_defaults(f=cmd_vsign)
    s = sp.add_parser("sign"); s.add_argument("envelope"); s.add_argument("key")
    s.set_defaults(f=cmd_sign)
    s = sp.add_parser("hash"); s.add_argument("envelope"); s.set_defaults(f=cmd_hash)
    s = sp.add_parser("verify")
    for n in ("envelope", "images", "trust", "state", "chain"):
        s.add_argument(n)
    s.set_defaults(f=cmd_verify)
    s = sp.add_parser("commit"); s.add_argument("state"); s.add_argument("envelope")
    s.add_argument("--trial-passed", action="store_true"); s.set_defaults(f=cmd_commit)
    s = sp.add_parser("demo"); s.add_argument("dir"); s.set_defaults(f=cmd_demo)
    a = p.parse_args(argv)
    return a.f(a) or 0


if __name__ == "__main__":
    sys.exit(main())
