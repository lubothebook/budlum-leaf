"""Tests of the Split: a stolen Skin holds no key, and a lying Skin signs nothing.

Run: python3 -m unittest discover -s tests   (from hw/core/trust)
"""
import hashlib
import os
import random
import struct
import sys
import unittest

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import skinauth as S  # noqa: E402

H = S.H


class DetRng:
    def __init__(self, seed=b"t"):
        self.seed, self.n = seed, 0

    def __call__(self, k):
        self.n += 1
        return hashlib.sha256(self.seed + struct.pack(">Q", self.n)).digest()[:k]


class Tick:
    """A clock that moves one second per read, so the chip rate limit passes."""

    def __init__(self):
        self.t = 0.0

    def __call__(self):
        self.t += 1.0
        return self.t


VENDOR = S.Vendor()
RNG = DetRng(b"link")


def world(seed_core=b"alice", seed_skin=b"s1", **kw):
    core = S.Core(VENDOR.pub, wallet_seed=seed_core, rng=DetRng(b"core" + seed_core), **kw)
    skin = S.SkinChip(seed_skin, VENDOR, clock=Tick())
    return core, skin


def paired(**kw):
    core, skin = world(**kw)
    v, ack, _ = S.pair(core, skin)
    assert ack is not None, v
    return core, skin


def live(core, skin, now=0.0):
    core.unlock(core.hw.press(), now)
    st, sess = S.connect(core, skin, DetRng(b"x"), now=now)
    assert st == "OK", st
    return sess


def value_tx(amount, to=b"\xaa" * 8):
    return {"to": to, "amount": amount, "fee": 1}


class Primitives(unittest.TestCase):
    def test_x25519_rfc7748(self):
        a = bytes.fromhex("77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a")
        b = bytes.fromhex("5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb")
        self.assertEqual(S.x25519_public(a).hex(),
                         "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a")
        self.assertEqual(S.x25519(a, S.x25519_public(b)).hex(),
                         "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742")

    def test_chacha20_poly1305_rfc8439(self):
        key = bytes(range(0x80, 0xa0))
        nonce = bytes.fromhex("070000004041424344454647")
        aad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
        pt = (b"Ladies and Gentlemen of the class of '99: If I could offer you only "
              b"one tip for the future, sunscreen would be it.")
        sealed = S.aead_seal(key, nonce, aad, pt)
        self.assertEqual(sealed[:16].hex(), "d31a8d34648e60db7b86afbc53ef7ec2")
        self.assertEqual(sealed[-16:].hex(), "1ae10b594f09e26a7e902ecbd0600691")
        self.assertEqual(S.aead_open(key, nonce, aad, sealed), pt)
        for i in (0, 40, len(sealed) - 1):
            bad = bytearray(sealed)
            bad[i] ^= 1
            self.assertIsNone(S.aead_open(key, nonce, aad, bytes(bad)))
        self.assertIsNone(S.aead_open(key, nonce, aad + b"x", sealed))
        self.assertIsNone(S.aead_open(key, b"\x01" + nonce[1:], aad, sealed))

    def test_poly1305_rfc8439(self):
        k = bytes.fromhex("85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b")
        self.assertEqual(S.poly1305(k, b"Cryptographic Forum Research Group").hex(),
                         "a8061dc1305136c6c22b8baf0c0127a9")

    def test_hkdf_rfc5869_case1(self):
        okm = S.hkdf(bytes([0x0b] * 22), bytes(range(13)), bytes(range(0xf0, 0xfa)), 42)
        self.assertEqual(okm.hex(), "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c5db02d56ecc4c5bf"
                                    "34007208d5b887185865")


class StolenSkin(unittest.TestCase):
    def test_a_stolen_skin_holds_no_wallet_key_and_no_session_key(self):
        core, skin = paired()
        live(core, skin)
        wallet = core._wallet
        self.assertIsNotNone(skin.send)
        skin.power_off()                                 # the thief unplugs it
        for level in ("powered_off", "decap"):
            got = skin.readout(level)
            blob = repr(got).encode()
            self.assertNotIn(wallet.hex().encode(), blob)
            self.assertNotIn(wallet, blob)
            self.assertNotIn("identity_key", got)        # a hardened chip
            self.assertNotIn("session_key", got)
        self.assertIsNone(skin.send)
        self.assertIsNone(skin.recv)

    def test_the_honest_leak_an_unhardened_chip_gives_the_identity_key(self):
        core, skin = world()
        weak = S.SkinChip(b"weak", VENDOR, hardened=False)
        self.assertIn("identity_key", weak.readout("decap"))
        self.assertNotIn("identity_key", weak.readout("powered_off"))
        self.assertNotIn("identity_key", skin.readout("decap"))

    def test_the_stolen_skin_still_names_the_cores_it_trusts(self):
        core, skin = paired()
        got = skin.readout("powered_off")
        self.assertIn(core.core_pub.hex(), got["pinned_cores"])

    def test_the_frame_store_dies_with_power(self):
        core, skin = world()
        skin.residual = b"last slice of the screen"
        self.assertIn("residual_pixels", skin.readout("decap"))
        skin.power_off()
        self.assertEqual(skin.readout("decap")["residual_pixels"], "")

    def test_a_thief_cannot_pair_the_skin_to_the_victims_core_without_the_button(self):
        core, skin = paired()
        with self.assertRaises(PermissionError):
            core.pair_challenge(None)
        with self.assertRaises(PermissionError):
            core.pair_challenge(b"\x00" * 40)             # a forged press

    def test_the_skin_holds_nothing_that_signs_for_the_wallet(self):
        core, skin = paired()
        self.assertFalse(hasattr(skin, "sign"))
        with self.assertRaises(PermissionError):
            skin.attest(b"SEND 1000 TO mallory")
        with self.assertRaises(PermissionError):
            skin.attest(S.TAG_SIGN + b"x" * 32)
        found = [k for k, v in vars(skin).items()
                 if isinstance(v, (bytes, bytearray)) and v == core._wallet]
        self.assertEqual(found, [])

    def test_the_chip_rate_limits_its_signatures(self):
        skin = S.SkinChip(b"r", VENDOR, clock=lambda: 5.0)   # time stands still
        skin.attest(S.TAG_PAIR + b"a")
        with self.assertRaises(PermissionError):
            skin.attest(S.TAG_PAIR + b"b")


class Cloned(unittest.TestCase):
    def test_two_live_sessions_under_one_identity_raise_a_clone_alert(self):
        core, skin = paired()
        live(core, skin)
        clone = S.SkinChip(b"s1", VENDOR, clock=Tick())      # same identity key
        self.assertEqual(clone.pub, skin.pub)
        clone.pins = dict(skin.pins)                          # copied from flash
        st, sess = S.connect(core, clone, DetRng(b"c"), now=1.0)
        self.assertIn("clone alert", st)
        self.assertEqual(core.sessions, {})                   # both dropped
        st, _ = S.connect(core, skin, DetRng(b"d"), now=2.0)
        self.assertIn("suspect", st)
        core.reinstate(skin.pub, core.hw.press())
        self.assertEqual(S.connect(core, skin, DetRng(b"e"), now=3.0)[0], "OK")

    def test_a_dropped_link_is_not_a_clone(self):
        core, skin = paired()
        live(core, skin, now=0.0)
        self.assertEqual(S.connect(core, skin, DetRng(b"f"), now=60.0)[0], "OK")

    def test_a_clone_against_a_locked_core_sees_only_the_lock_screen(self):
        core, skin = paired()
        clone = S.SkinChip(b"s1", VENDOR, clock=Tick())
        clone.pins = dict(skin.pins)
        st, sess = S.connect(core, clone, DetRng(b"c"), now=0.0)   # Core never unlocked
        self.assertEqual(st, "OK")
        out = core.compose([(S.PRIVATE, "balance 99"), (S.PUBLIC, "menu")], clone.pub, 1.0)
        self.assertEqual(out, [(S.PUBLIC, "locked")])
        rid = core.request_sign("VALUE", value_tx(1), 1.0)
        self.assertIn("REFUSED", core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=clone.pub))

    def test_the_residual_a_clone_of_an_unlocked_core_session_is_not_detectable_alone(self):
        """A clone that connects while the real Skin is off looks like the real
        Skin. Only the lock and the budget bound the loss."""
        core, skin = paired()
        core.unlock(core.hw.press(), 0.0)
        clone = S.SkinChip(b"s1", VENDOR, clock=Tick())
        clone.pins = dict(skin.pins)
        self.assertEqual(S.connect(core, clone, DetRng(b"c"), now=0.0)[0], "OK")
        out = core.compose([(S.PRIVATE, "balance 99")], clone.pub, 1.0)
        self.assertEqual(out, [(S.PRIVATE, "balance 99")])

    def test_a_counterfeit_skin_without_the_vendor_cert_is_viewer_only(self):
        core = S.Core(VENDOR.pub, rng=DetRng(b"c"))
        fake = S.SkinChip(b"fake", None, clock=Tick())
        v, ack, _ = S.pair(core, fake)
        self.assertIn("uncertified", v)
        self.assertEqual(core.state["skins"][fake.pub.hex()]["tier"], S.S1)

    def test_unlisted_decoder_firmware_is_viewer_only(self):
        core = S.Core(VENDOR.pub, rng=DetRng(b"c"))
        core.fw_list = {hashlib.sha256(b"skin-fw-1").digest()}
        odd = S.SkinChip(b"odd", VENDOR, fw=b"modified decoder", clock=Tick())
        v, ack, _ = S.pair(core, odd)
        self.assertIn("unlisted decoder firmware", v)
        self.assertEqual(core.state["skins"][odd.pub.hex()]["tier"], S.S1)
        good = S.SkinChip(b"good", VENDOR, clock=Tick())
        S.pair(core, good)
        self.assertEqual(core.state["skins"][good.pub.hex()]["tier"], S.S2)


class Pairing(unittest.TestCase):
    def test_pairing_needs_a_press_on_each_side(self):
        core, skin = world()
        with self.assertRaises(PermissionError):
            S.pair(core, skin, hw_press_core=False)
        core, skin = world()
        with self.assertRaises(PermissionError):
            S.pair(core, skin, hw_press_skin=False)

    def test_a_good_pairing_pins_both_sides_and_posts_a_commitment(self):
        core, skin = paired()
        e = core.state["skins"][skin.pub.hex()]
        self.assertEqual(e["status"], "ACTIVE")
        self.assertIn(core.core_pub, skin.pins)
        commit = bytes.fromhex(e["commit"])
        self.assertEqual(core.chain.state_of(core.wallet_pub, commit), "PAIRED")
        blob = repr(core.chain.records).encode()
        self.assertNotIn(skin.pub, blob)                      # no Skin identity on chain
        self.assertNotIn(skin.pub.hex().encode(), blob)

    def test_the_same_skin_gives_a_different_commitment_per_wallet(self):
        a, skin = paired(seed_core=b"alice")
        b = S.Core(VENDOR.pub, wallet_seed=b"bob", rng=DetRng(b"bob"))
        S.pair(b, skin)
        ca = a.state["skins"][skin.pub.hex()]["commit"]
        cb = b.state["skins"][skin.pub.hex()]["commit"]
        self.assertNotEqual(ca, cb)

    def test_a_replayed_pairing_frame_is_refused(self):
        core, skin = world()
        nonce, ck = core.pair_challenge(core.hw.press())
        frame, _ = skin.pair_respond(ck, nonce, True)
        v, _ = core.pair_accept(frame)
        self.assertEqual(v, "OK")
        v, _ = core.pair_accept(frame)                        # the same frame again
        self.assertIn("no open challenge", v)
        core.pair_challenge(core.hw.press())
        v, _ = core.pair_accept(frame)                        # a fresh nonce is open
        self.assertIn("nonce mismatch", v)

    def test_a_replayed_counter_with_a_fresh_nonce_is_refused_even_after_a_power_cut(self):
        core, skin = paired()
        core.power_cycle()
        skin.counter = 0                                      # the attacker rewinds
        nonce, ck = core.pair_challenge(core.hw.press())
        frame, _ = skin.pair_respond(ck, nonce, True)
        v, _ = core.pair_accept(frame)
        self.assertIn("replayed counter", v)

    def test_a_record_that_names_another_core_is_refused(self):
        core, skin = world()
        other = S.Core(VENDOR.pub, wallet_seed=b"eve", rng=DetRng(b"eve"))
        nonce, ck = core.pair_challenge(core.hw.press())
        frame, _ = skin.pair_respond(other.core_pub, nonce, True)
        v, _ = core.pair_accept(frame)
        self.assertIn("another Core", v)

    def test_an_expired_record_is_refused(self):
        core, skin = world()
        nonce, ck = core.pair_challenge(core.hw.press())
        frame, _ = skin.pair_respond(ck, nonce, True, expiry=core.anchor)
        self.assertIn("expired", core.pair_accept(frame)[0])

    def test_a_forged_or_tampered_record_fails_the_signature(self):
        core, skin = world()
        nonce, ck = core.pair_challenge(core.hw.press())
        frame, _ = skin.pair_respond(ck, nonce, True)
        bad = bytearray(frame)
        bad[1 + 32 + 32] = S.S2 if bad[1 + 32 + 32] != S.S2 else S.S1   # raise the tier
        v, _ = core.pair_accept(bytes(bad))
        self.assertIn("bad signature", v)

    def test_the_parser_is_fixed_and_survives_fuzz(self):
        core, skin = world()
        nonce, ck = core.pair_challenge(core.hw.press())
        frame, _ = skin.pair_respond(ck, nonce, True)
        self.assertEqual(len(frame), S.FRAME_LEN)
        rnd = random.Random(3)
        for _ in range(2000):
            b = bytearray(frame)
            for _ in range(rnd.randint(1, 4)):
                b[rnd.randrange(len(b))] = rnd.randrange(256)
            try:
                S.parse_frame(bytes(b))
            except S.ParseError:
                pass
        for n in (0, 1, S.FRAME_LEN - 1, S.FRAME_LEN + 1):
            with self.assertRaises(S.ParseError):
                S.parse_frame(b"\x01" * n)

    def _mitm_pairing(self, core, skin, user_ignores_sas):
        """The attacker pairs with the Skin as a Core and with the Core as a
        Skin. Each side sees a genuine looking pairing."""
        mal_core = S.Core(VENDOR.pub, wallet_seed=b"mallory-core", rng=DetRng(b"m"))
        mal_skin = S.SkinChip(b"mallory", None, clock=Tick())
        n1, ck = core.pair_challenge(core.hw.press())            # the victim Core asks
        n2, k2 = mal_core.pair_challenge(mal_core.hw.press())    # the attacker asks the Skin
        frame_s, sas_on_skin = skin.pair_respond(k2, n2, True)
        mal_core.pair_accept(frame_s)
        ack_s = mal_core.pair_commit(True, mal_core.hw.press())
        frame_c, _ = mal_skin.pair_respond(ck, n1, True)
        _, sas_on_core = core.pair_accept(frame_c)
        match = True if user_ignores_sas else (sas_on_skin == sas_on_core)
        ack_c = core.pair_commit(match, core.hw.press())
        return mal_skin, ack_s, ack_c, (sas_on_skin, sas_on_core), (k2, n2)

    def test_a_relay_at_pairing_is_caught_by_the_sas(self):
        core, skin = world()
        mal_skin, ack_s, ack_c, sases, _ = self._mitm_pairing(core, skin, False)
        self.assertNotEqual(sases[0], sases[1])                # the two strings differ
        self.assertIsNone(ack_c)                               # the owner refuses
        self.assertEqual(core.state["skins"], {})              # the Core paired nothing

    def test_the_residual_a_user_who_ignores_the_sas_pairs_the_attacker(self):
        core, skin = world()
        mal_skin, ack_s, ack_c, sases, _ = self._mitm_pairing(core, skin, True)
        self.assertIsNotNone(ack_c)
        self.assertIn(mal_skin.pub.hex(), core.state["skins"])
        self.assertEqual(core.state["skins"][mal_skin.pub.hex()]["tier"], S.S1)
        self.assertNotIn(skin.pub.hex(), core.state["skins"])


class Link(unittest.TestCase):
    def test_session_roundtrip_hides_the_plaintext(self):
        core, skin = paired()
        sess = live(core, skin)
        msg = b"private balance 12345"
        frame = sess.send.seal(msg)
        self.assertNotIn(msg, frame)
        self.assertEqual(skin.recv.open(frame), msg)
        back = skin.send.seal(b"tap 10,20")
        self.assertEqual(sess.recv.open(back), b"tap 10,20")

    def test_tamper_replay_reorder_and_reflection_are_refused(self):
        core, skin = paired()
        sess = live(core, skin)
        f1, f2 = sess.send.seal(b"one"), sess.send.seal(b"two")
        bad = bytearray(f1)
        bad[12] ^= 1
        self.assertIsNone(skin.recv.open(bytes(bad)))
        self.assertEqual(skin.recv.open(f2), b"two")
        self.assertIsNone(skin.recv.open(f1))                  # reorder
        self.assertIsNone(skin.recv.open(f2))                  # replay
        f3 = sess.send.seal(b"three")
        self.assertIsNone(sess.recv.open(f3))                  # reflection to the Core

    def test_a_man_in_the_middle_cannot_swap_an_ephemeral_key(self):
        core, skin = paired()
        core.unlock(core.hw.press(), 0.0)
        mitm_eph = S.x25519_public(b"\x42" * 32)

        def swap_core(name, msg):
            if name == "core_hello":
                return (mitm_eph, msg[1], msg[2], msg[3])
            return msg

        st, _ = S.connect(core, skin, DetRng(b"m"), mitm=swap_core)
        self.assertIn("Skin refused the Core", st)

        core2, skin2 = paired(seed_core=b"bob", seed_skin=b"s2")
        core2.unlock(core2.hw.press(), 0.0)

        def swap_skin(name, msg):
            if name == "skin_hello":
                return (mitm_eph, msg[1], msg[2])
            return msg

        st, _ = S.connect(core2, skin2, DetRng(b"m2"), mitm=swap_skin)
        self.assertIn("refused", st)

    def test_a_forged_skin_signature_is_refused(self):
        core, skin = paired()

        def forge(name, msg):
            return b"\x00" * 64 if name == "skin_sig" else msg

        st, sess = S.connect(core, skin, DetRng(b"m"), mitm=forge)
        self.assertIn("Core refused the Skin signature", st)
        self.assertIsNone(sess)

    def test_every_session_has_fresh_keys(self):
        core, skin = paired()
        s1 = live(core, skin, now=0.0)
        k1 = s1.send.key
        core.drop(skin.pub)
        st, s2 = S.connect(core, skin, DetRng(b"other"), now=1.0)
        self.assertNotEqual(k1, s2.send.key)
        old = s1.send.seal(b"old session")
        self.assertIsNone(skin.recv.open(old))                 # the old key is dead

    def test_an_unpaired_skin_is_refused(self):
        core, skin = paired()
        stranger = S.SkinChip(b"stranger", VENDOR, clock=Tick())
        st, _ = S.connect(core, stranger, DetRng(b"s"))
        self.assertIn("unknown Skin", st)


class Revocation(unittest.TestCase):
    def test_a_revoked_skin_is_cut_off_and_refused(self):
        core, skin = paired()
        sess = live(core, skin)
        e = core.state["skins"][skin.pub.hex()]
        self.assertEqual(core.revoke(skin.pub, core.hw.press()), "REVOKED")
        self.assertFalse(sess.live)
        self.assertNotIn(skin.pub, core.sessions)
        st, _ = S.connect(core, skin, DetRng(b"r"), now=100.0)
        self.assertIn("revoked", st)
        self.assertEqual(core.chain.state_of(core.wallet_pub, bytes.fromhex(e["commit"])),
                         "REVOKED")
        clone = S.SkinChip(b"s1", VENDOR, clock=Tick())
        clone.pins = dict(skin.pins)
        self.assertIn("revoked", S.connect(core, clone, DetRng(b"r2"), now=101.0)[0])

    def test_revocation_survives_a_power_cut(self):
        core, skin = paired()
        core.revoke(skin.pub, core.hw.press())
        core.power_cycle()
        self.assertIn("revoked", S.connect(core, skin, DetRng(b"r"))[0])

    def test_revocation_needs_the_button_of_the_core(self):
        core, skin = paired()
        with self.assertRaises(PermissionError):
            core.revoke(skin.pub, None)
        rid = core.request_sign("KEYOP", {"op": "revoke"}, 0.0)
        self.assertIn("REFUSED", core.confirm(rid, S.SKIN_TAP, 1.0, skin_key=skin.pub))

    def test_the_chain_refuses_a_replayed_pairing_or_revocation(self):
        core, skin = paired()
        e = core.state["skins"][skin.pub.hex()]
        commit = bytes.fromhex(e["commit"])
        old = core.chain.records[0]
        core.revoke(skin.pub, core.hw.press())
        kind, w, c, tier, epoch, ctr, exp = old
        body = kind + w + c + bytes([tier]) + struct.pack(">QQQ", epoch, ctr, exp)
        sig = core._sign_wallet(body)                          # a perfectly valid old record
        self.assertIn("counter not new", core.chain.post(kind, w, c, tier, epoch, ctr, exp, sig))
        rev = core.chain.records[-1]
        k, w, c, tier, epoch, ctr, exp = rev
        body = k + w + c + bytes([tier]) + struct.pack(">QQQ", epoch, ctr, exp)
        self.assertIn("counter not new",
                      core.chain.post(k, w, c, tier, epoch, ctr, exp, core._sign_wallet(body)))
        self.assertEqual(core.chain.state_of(core.wallet_pub, commit), "REVOKED")

    def test_the_chain_refuses_a_record_not_signed_by_the_wallet(self):
        core, skin = paired()
        evil = H.ed_sign(hashlib.sha256(b"evil").digest(), b"x")
        r = core.chain.post(S.TAG_CHAIN_REVOKE, core.wallet_pub, b"\x00" * 32, 2, 9, 99, 0, evil)
        self.assertIn("bad wallet signature", r)


class RogueCore(unittest.TestCase):
    def test_a_rogue_core_cannot_pair_a_skin_without_a_press_on_the_skin(self):
        core, skin = paired()
        rogue = S.Core(VENDOR.pub, wallet_seed=b"rogue", rng=DetRng(b"rogue"))
        with self.assertRaises(PermissionError):
            S.pair(rogue, skin, hw_press_skin=False)

    def test_a_rogue_core_cannot_drive_a_skin_it_is_not_paired_to(self):
        core, skin = paired()
        rogue = S.Core(VENDOR.pub, wallet_seed=b"rogue", rng=DetRng(b"rogue"))
        # even if the rogue knows the Skin key, its Core record has no such Skin
        st, _ = S.connect(rogue, skin, DetRng(b"x"))
        self.assertIn("unknown Skin", st)
        # a rogue that fakes its own state still fails: the Skin pins one key
        rogue.state_forged = True
        self.assertNotIn(rogue.core_pub, skin.pins)

    def test_a_paired_rogue_core_shows_a_different_strip_and_has_no_camera(self):
        core, skin = paired()
        rogue = S.Core(VENDOR.pub, wallet_seed=b"rogue", rng=DetRng(b"rogue"))
        S.pair(rogue, skin, role="GUEST")
        rogue.unlock(rogue.hw.press(), 0.0)
        S.connect(rogue, skin, DetRng(b"x"))
        fp_rogue = skin.strip()
        core.drop(skin.pub)
        core.unlock(core.hw.press(), 0.0)
        S.connect(core, skin, DetRng(b"y"), now=100.0)
        self.assertNotEqual(fp_rogue, skin.strip())            # the user can see which Core
        self.assertEqual(S.effective_caps(rogue, skin) & S.CAP_CAMERA, 0)

    def test_a_camera_lane_needs_a_press_on_both_sides(self):
        core, skin = paired()
        core.enable_cap(skin.pub, S.CAP_CAMERA, core.hw.press())
        self.assertEqual(S.effective_caps(core, skin) & S.CAP_CAMERA, 0)
        with self.assertRaises(PermissionError):
            skin.enable_cap(core.core_pub, S.CAP_CAMERA, press=False)
        skin.enable_cap(core.core_pub, S.CAP_CAMERA, press=True)
        self.assertEqual(S.effective_caps(core, skin) & S.CAP_CAMERA, S.CAP_CAMERA)

    def test_a_rogue_core_holds_no_wallet_of_the_owner(self):
        core, skin = paired()
        rogue = S.Core(VENDOR.pub, wallet_seed=b"rogue", rng=DetRng(b"rogue"))
        self.assertNotEqual(rogue.wallet_pub, core.wallet_pub)
        rid = core.request_sign("VALUE", value_tx(50), 0.0)
        self.assertIn("REFUSED", rogue.confirm(rid, S.CORE_BUTTON, 10.0, token=rogue.hw.press()))


class ForgedTap(unittest.TestCase):
    def setUp(self):
        self.core, self.skin = paired(blind_budget=100)
        self.sess = live(self.core, self.skin)

    def test_a_forged_tap_cannot_confirm_a_key_operation(self):
        for op in ("revoke", "pair", "export", "policy"):
            rid = self.core.request_sign("KEYOP", {"op": op}, 1.0)
            r = self.core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=self.skin.pub)
            self.assertIn("REFUSED", r)

    def test_a_forged_tap_cannot_confirm_a_value_above_the_budget(self):
        rid = self.core.request_sign("VALUE", value_tx(5000), 1.0)
        r = self.core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=self.skin.pub)
        self.assertIn("REFUSED", r)

    def test_a_flood_of_forged_taps_loses_at_most_the_blind_budget(self):
        signed = 0
        total = 0
        for i in range(100):
            rid = self.core.request_sign("VALUE", value_tx(10), 1.0 + i)
            r = self.core.confirm(rid, S.SKIN_TAP, 2.0 + i, skin_key=self.skin.pub)
            if isinstance(r, tuple) and r[0] == "SIGNED":
                signed += 1
                total += 10
        self.assertEqual(signed, 10)
        self.assertLessEqual(total, 100)
        self.core.power_cycle()                               # cutting power resets nothing
        self.core.unlock(self.core.hw.press(), 500.0)
        S.connect(self.core, self.skin, DetRng(b"z"), now=500.0)
        rid = self.core.request_sign("VALUE", value_tx(10), 501.0)
        self.assertIn("REFUSED", self.core.confirm(rid, S.SKIN_TAP, 502.0, skin_key=self.skin.pub))

    def test_the_budget_resets_with_the_next_day(self):
        for i in range(10):
            rid = self.core.request_sign("VALUE", value_tx(10), 1.0)
            self.core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=self.skin.pub)
        self.core.anchor += S.DAY_BLOCKS
        rid = self.core.request_sign("VALUE", value_tx(10), 3.0)
        self.assertEqual(self.core.confirm(rid, S.SKIN_TAP, 4.0, skin_key=self.skin.pub)[0],
                         "SIGNED")

    def test_a_viewer_skin_tap_never_confirms_anything(self):
        core = S.Core(VENDOR.pub, rng=DetRng(b"v"))
        fake = S.SkinChip(b"fake", None, clock=Tick())
        S.pair(core, fake)
        core.unlock(core.hw.press(), 0.0)
        S.connect(core, fake, DetRng(b"f"))
        rid = core.request_sign("VALUE", value_tx(1), 1.0)
        self.assertIn("REFUSED", core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=fake.pub))
        rid = core.request_sign("INPUT", {"scan": 1}, 1.0)
        self.assertIn("REFUSED", core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=fake.pub))

    def test_a_locked_core_signs_nothing_for_a_tap(self):
        self.core.unlocked_until = -1
        rid = self.core.request_sign("VALUE", value_tx(1), 1.0)
        self.assertIn("REFUSED", self.core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=self.skin.pub))

    def test_an_input_batch_carries_no_value(self):
        r = self.core.request_sign("INPUT", {"scan": 1, "amount": 5}, 1.0)
        self.assertIn("carries no value", r)
        rid = self.core.request_sign("INPUT", {"scan": 1}, 1.0)
        self.assertEqual(self.core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=self.skin.pub)[0],
                         "SIGNED")

    def test_a_lying_skin_summary_is_ignored_and_the_press_binds_to_the_core_summary(self):
        tx = value_tx(5000, to=b"\xee" * 8)                    # the real payee: Mallory
        rid = self.core.request_sign("VALUE", tx, 10.0)
        fake_summary = b"SEND 5 TO alice"                      # what the Skin paints
        fake_hash = hashlib.sha256(fake_summary).digest()
        real = self.core.summarise(tx)
        self.assertEqual(self.core.hw.shown_hash, hashlib.sha256(real).digest())
        self.assertNotEqual(self.core.hw.shown_hash, fake_hash)
        r = self.core.confirm(rid, S.CORE_BUTTON, 12.0, token=self.core.hw.press(),
                              presented_hash=fake_hash)
        self.assertIn("hash is not the request", r)
        r = self.core.confirm(rid, S.CORE_BUTTON, 12.0, token=self.core.hw.press())
        self.assertEqual(r[0], "SIGNED")
        self.assertEqual(r[2], hashlib.sha256(real).digest())

    def test_the_press_needs_dwell_a_real_token_and_the_display(self):
        rid = self.core.request_sign("VALUE", value_tx(5000), 10.0)
        self.assertIn("not shown long enough",
                      self.core.confirm(rid, S.CORE_BUTTON, 10.5, token=self.core.hw.press()))
        self.assertIn("no hardware press", self.core.confirm(rid, S.CORE_BUTTON, 12.0, token=None))
        self.assertIn("no hardware press",
                      self.core.confirm(rid, S.CORE_BUTTON, 12.0, token=b"\x00" * 40))
        tok = self.core.hw.press()
        self.assertEqual(self.core.confirm(rid, S.CORE_BUTTON, 12.0, token=tok)[0], "SIGNED")
        rid2 = self.core.request_sign("VALUE", value_tx(5000), 20.0)
        self.assertIn("no hardware press",
                      self.core.confirm(rid2, S.CORE_BUTTON, 22.0, token=tok))   # a reused press

    def test_a_second_request_replaces_the_display_and_blocks_the_first(self):
        a = self.core.request_sign("VALUE", value_tx(5000, b"\x01" * 8), 10.0)
        b = self.core.request_sign("VALUE", value_tx(6000, b"\x02" * 8), 11.0)
        self.assertIn("did not show this request",
                      self.core.confirm(a, S.CORE_BUTTON, 14.0, token=self.core.hw.press()))
        self.assertEqual(self.core.confirm(b, S.CORE_BUTTON, 14.0, token=self.core.hw.press())[0],
                         "SIGNED")

    def test_a_confirmation_is_single_use_and_expires(self):
        rid = self.core.request_sign("VALUE", value_tx(5000), 10.0)
        self.assertEqual(self.core.confirm(rid, S.CORE_BUTTON, 12.0, token=self.core.hw.press())[0],
                         "SIGNED")
        self.assertIn("already used",
                      self.core.confirm(rid, S.CORE_BUTTON, 13.0, token=self.core.hw.press()))
        rid = self.core.request_sign("VALUE", value_tx(5000), 100.0)
        self.assertIn("expired",
                      self.core.confirm(rid, S.CORE_BUTTON, 100.0 + S.CONFIRM_TTL + 1,
                                        token=self.core.hw.press()))

    def test_a_validator_core_cannot_mint_a_press(self):
        """The compute of a Core that is also a validator has no handle to the
        press secret. It can replay an old press or invent one. Both fail."""
        old = self.core.hw.press()
        rid = self.core.request_sign("VALUE", value_tx(5000), 10.0)
        self.assertEqual(self.core.confirm(rid, S.CORE_BUTTON, 12.0, token=old)[0], "SIGNED")
        rid = self.core.request_sign("VALUE", value_tx(5000), 20.0)
        self.assertIn("no hardware press", self.core.confirm(rid, S.CORE_BUTTON, 23.0, token=old))
        invented = struct.pack(">Q", 99) + hashlib.sha256(b"guess").digest()
        self.assertIn("no hardware press",
                      self.core.confirm(rid, S.CORE_BUTTON, 23.0, token=invented))

    def test_a_changed_trusted_part_blocks_signing_until_the_owner_confirms(self):
        parts = {p: hashlib.sha256(p.encode()).digest() for p in
                 ("U7", "U4", "U1", "RDISP", "BUTTON", "U2A", "U6")}
        swapped = dict(parts, U2A=hashlib.sha256(b"new radio").digest())
        changed, tcb = self.core.measure(swapped)
        self.assertEqual((changed, tcb), (["U2A"], []))
        self.assertTrue(self.core.state["tcb_ok"])
        swapped["U1"] = hashlib.sha256(b"evil display path").digest()
        changed, tcb = self.core.measure(swapped)
        self.assertEqual(tcb, ["U1"])
        self.assertIn("trusted part changed", self.core.request_sign("VALUE", value_tx(1), 1.0))
        self.assertIn("trusted part changed", self.core.request_sign("KEYOP", {"op": "x"}, 1.0))
        self.core.ack_config(swapped, self.core.hw.press())
        self.assertNotIn("REFUSED", str(self.core.request_sign("VALUE", value_tx(1), 2.0)))


class Screen(unittest.TestCase):
    ITEMS = [(S.PUBLIC, "menu"), (S.PRIVATE, "balance 12345"), (S.SECRET, "PIN 4821"),
             (S.TXSUM, "SEND 5")]

    def test_a_secret_never_reaches_any_tier_or_the_link(self):
        core, skin = paired()
        sess = live(core, skin)
        for unlocked in (False, True):
            core.unlocked_until = 100.0 if unlocked else -1
            out = core.compose(self.ITEMS, skin.pub, 1.0)
            self.assertNotIn(b"4821", repr(out).encode())
            frame = sess.send.seal(repr(out).encode())
            self.assertNotIn(b"4821", skin.recv.open(frame) or b"")
        viewer = S.Core(VENDOR.pub, rng=DetRng(b"v"))
        fake = S.SkinChip(b"fake", None, clock=Tick())
        S.pair(viewer, fake)
        viewer.unlock(viewer.hw.press(), 0.0)
        S.connect(viewer, fake, DetRng(b"f"))
        self.assertNotIn(b"4821", repr(viewer.compose(self.ITEMS, fake.pub, 1.0)).encode())

    def test_private_pixels_need_the_owner_tier_and_an_unlocked_core(self):
        core, skin = paired()
        live(core, skin)
        core.unlocked_until = -1
        self.assertEqual(core.compose(self.ITEMS, skin.pub, 1.0), [(S.PUBLIC, "locked")])
        core.unlocked_until = 100.0
        out = core.compose(self.ITEMS, skin.pub, 1.0)
        self.assertIn((S.PRIVATE, "balance 12345"), out)
        viewer = S.Core(VENDOR.pub, rng=DetRng(b"v"))
        fake = S.SkinChip(b"fake", None, clock=Tick())
        S.pair(viewer, fake)
        viewer.unlock(viewer.hw.press(), 0.0)
        S.connect(viewer, fake, DetRng(b"f"))
        out = viewer.compose(self.ITEMS, fake.pub, 1.0)
        self.assertEqual([c for c, _ in out if c != S.SECRET], [S.PUBLIC])

    def test_the_residual_the_rogue_skin_reads_every_private_pixel_it_is_given(self):
        """The worst hole in confidentiality. A paired Skin that is hostile
        sees everything the Core composes for it. Only the class rule bounds it."""
        core, skin = paired()
        sess = live(core, skin)
        out = core.compose(self.ITEMS, skin.pub, 1.0)
        plain = skin.recv.open(sess.send.seal(repr(out).encode()))
        self.assertIn(b"balance 12345", plain)
        self.assertNotIn(b"4821", plain)


class Roam(unittest.TestCase):
    def test_a_skin_moved_to_a_new_core(self):
        a, skin = paired(seed_core=b"alice")
        live(a, skin, now=0.0)
        b = S.Core(VENDOR.pub, wallet_seed=b"bob", rng=DetRng(b"bob"))
        with self.assertRaises(PermissionError):
            S.pair(b, skin, hw_press_skin=False)               # no press, no pairing
        self.assertIn("unknown Skin", S.connect(b, skin, DetRng(b"x"))[0])
        S.pair(b, skin, role="GUEST")
        b.unlock(b.hw.press(), 0.0)
        a.drop(skin.pub)                                       # the link to A ended
        self.assertEqual(S.connect(b, skin, DetRng(b"x"), now=10.0)[0], "OK")
        self.assertEqual(skin.active, b.core_pub)
        self.assertEqual(S.effective_caps(b, skin) & S.CAP_CAMERA, 0)   # guest: no camera
        # the old Core cannot see through the Skin any more
        self.assertNotIn(skin.pub, [s for s in a.sessions])
        # the Skin returns to A with no new pairing
        a.unlock(a.hw.press(), 20.0)
        self.assertEqual(S.connect(a, skin, DetRng(b"y"), now=30.0)[0], "OK")
        self.assertEqual(skin.active, a.core_pub)

    def test_a_session_does_not_roam_with_the_skin(self):
        a, skin = paired(seed_core=b"alice")
        live(a, skin)
        rid = a.request_sign("VALUE", value_tx(5000), 1.0)
        b = S.Core(VENDOR.pub, wallet_seed=b"bob", rng=DetRng(b"bob"))
        S.pair(b, skin)
        self.assertNotEqual(a.wallet_pub, b.wallet_pub)
        self.assertIn("REFUSED", b.confirm(rid, S.CORE_BUTTON, 5.0, token=b.hw.press()))
        ca = bytes.fromhex(a.state["skins"][skin.pub.hex()]["commit"])
        cb = bytes.fromhex(b.state["skins"][skin.pub.hex()]["commit"])
        self.assertEqual(a.chain.state_of(a.wallet_pub, ca), "PAIRED")
        self.assertNotEqual(ca, cb)

    def test_the_skin_has_four_pairing_slots(self):
        core, skin = paired()
        for i in range(S.MAX_PINS - 1):
            S.pair(S.Core(VENDOR.pub, wallet_seed=b"c%d" % i, rng=DetRng(b"c%d" % i)), skin)
        self.assertEqual(len(skin.pins), S.MAX_PINS)
        extra = S.Core(VENDOR.pub, wallet_seed=b"extra", rng=DetRng(b"extra"))
        with self.assertRaises(PermissionError):
            S.pair(extra, skin)
        with self.assertRaises(PermissionError):
            skin.unpin_all(press=False)
        skin.unpin_all(press=True)
        self.assertEqual(skin.pins, {})


class Budget(unittest.TestCase):
    def test_the_aead_cost_of_a_minimal_skin_decoder(self):
        b = S.aead_budget(12.3)
        self.assertAlmostEqual(b["slice_us"], 20.83, places=1)
        self.assertAlmostEqual(b["buffer_KiB"], 31.3, delta=0.5)
        self.assertEqual(b["engines"], 1)
        self.assertAlmostEqual(b["power_mW"][1.0], 12.3, places=1)
        self.assertAlmostEqual(b["hours_to_2_32_slices"], 24.9, delta=0.1)
        self.assertLess(b["tag_overhead_pct"], 0.1)
        small = S.aead_budget(6.1)
        self.assertLess(small["buffer_KiB"], b["buffer_KiB"])

    def test_the_cipher_is_a_small_share_of_the_skin_load(self):
        b = S.aead_budget(12.3)
        self.assertLess(b["power_mW"][1.0] / 800.0, 0.02)       # of the 0.80 W surface load

    def test_the_record_frame_is_fixed(self):
        self.assertEqual(S.FRAME_LEN, 276)


class DistanceOrder(unittest.TestCase):
    """Block HP-3: the Core can be kilometres away. Classes C0, C1, C2."""

    def test_the_trust_model_by_distance_class(self):
        c0, c1, c2 = (S.trust_model(c) for c in ("C0", "C1", "C2"))
        for m in (c0, c1):
            self.assertEqual(m["wallet_in"], "Core U7")
            self.assertTrue(m["skin_zero_key"])
            self.assertFalse(m["surface_in_boundary"])
        self.assertEqual(c2["wallet_in"], "Leaf U7, as L.6.0")
        self.assertFalse(c2["skin_zero_key"])
        self.assertTrue(c2["surface_in_boundary"])
        self.assertTrue(c0["core_button_reachable"])
        self.assertFalse(c1["core_button_reachable"])
        self.assertIn(S.CORE_BUTTON, c0["confirm_sources"])
        self.assertNotIn(S.CORE_BUTTON, c1["confirm_sources"])
        self.assertIn("none", c2["far_end_authority"])
        with self.assertRaises(ValueError):
            S.trust_model("C3")

    def test_the_core_button_is_out_of_reach_beyond_c0(self):
        core, skin = paired()
        live(core, skin)
        core.distance = "C1"
        rid = core.request_sign("VALUE", value_tx(5000), 10.0)
        r = core.confirm(rid, S.CORE_BUTTON, 12.0, token=core.hw.press())
        self.assertIn("out of reach", r)

    def test_a_confirmation_device_carries_the_press_at_c1(self):
        core, skin = paired()
        live(core, skin)
        core.distance = "C1"
        dev = S.ConfirmDevice(b"ring")
        core.pair_confirm_device(dev.pub, core.hw.press())
        tx = value_tx(5000, to=b"\xee" * 8)
        rid = core.request_sign("VALUE", tx, 10.0)
        summary, dn = core.confirm_blob(rid)
        self.assertEqual(summary, core.summarise(tx))
        sig = dev.confirm(summary, dn, 10.0, 12.0)
        r = core.confirm(rid, S.CONFIRM_DEVICE, 12.0, device_pub=dev.pub, device_sig=sig)
        self.assertEqual(r[0], "SIGNED")

    def test_a_confirmation_device_refuses_a_summary_the_skin_or_relay_changed(self):
        core, skin = paired()
        live(core, skin)
        core.distance = "C1"
        dev = S.ConfirmDevice(b"ring")
        core.pair_confirm_device(dev.pub, core.hw.press())
        rid = core.request_sign("VALUE", value_tx(5000, to=b"\xee" * 8), 10.0)
        summary, dn = core.confirm_blob(rid)
        sig = dev.confirm(b"SEND 5 TO alice", dn, 10.0, 12.0)        # a relay swapped it
        self.assertIn("did not confirm",
                      core.confirm(rid, S.CONFIRM_DEVICE, 12.0, device_pub=dev.pub, device_sig=sig))
        self.assertIsNone(dev.confirm(summary, dn, 10.0, 10.5))       # too quick a press
        # a signature for another request cannot be replayed on this one
        rid2 = core.request_sign("VALUE", value_tx(5000, to=b"\xee" * 8), 20.0)
        s2, dn2 = core.confirm_blob(rid2)
        good = dev.confirm(s2, dn2, 20.0, 22.0)
        self.assertIn("did not confirm",
                      core.confirm(rid, S.CONFIRM_DEVICE, 22.0, device_pub=dev.pub, device_sig=good))
        stranger = S.ConfirmDevice(b"stranger")
        sig = stranger.confirm(summary, dn, 10.0, 12.0)
        self.assertIn("not a paired confirmation device",
                      core.confirm(rid, S.CONFIRM_DEVICE, 12.0, device_pub=stranger.pub,
                                   device_sig=sig))
        with self.assertRaises(PermissionError):
            core.pair_confirm_device(stranger.pub, None)

    def test_proximity_gives_no_authority_even_through_a_relay(self):
        core, skin = paired()
        relayed = lambda name, msg: msg                      # a relay passes bits unchanged
        st, sess = S.connect(core, skin, DetRng(b"p"), mitm=relayed)
        self.assertEqual(st, "OK")
        self.assertFalse(core.unlocked(1.0))                  # a session is not an unlock
        self.assertEqual(core.compose([(S.PRIVATE, "balance")], skin.pub, 1.0),
                         [(S.PUBLIC, "locked")])
        rid = core.request_sign("VALUE", value_tx(1), 1.0)
        self.assertIn("REFUSED", core.confirm(rid, S.SKIN_TAP, 2.0, skin_key=skin.pub))

    def test_a_downgrade_of_the_link_suite_fails(self):
        core, skin = paired()

        def strip(name, msg):
            return (msg[0], msg[1], bytes([S.SUITE_WEAK])) if name == "skin_hello" else msg

        st, _ = S.connect(core, skin, DetRng(b"d1"), mitm=strip)
        self.assertIn("no suite at or above the floor", st)
        # a Core with a lowered floor picks the weak suite, and the Skin refuses it
        core.min_suite = S.SUITE_WEAK
        st, _ = S.connect(core, skin, DetRng(b"d2"), mitm=strip, now=100.0)
        self.assertIn("Skin refused the Core", st)

        def force(name, msg):
            return (msg[0], msg[1], S.SUITE_WEAK, msg[3]) if name == "core_hello" else msg

        core.min_suite = S.SUITE_STRONG
        st, _ = S.connect(core, skin, DetRng(b"d3"), mitm=force, now=200.0)
        self.assertIn("Skin refused the Core", st)

    def test_a_jammed_link_blanks_the_skin_and_locks_the_core(self):
        core, skin = paired()
        sess = live(core, skin, now=0.0)
        self.assertEqual(skin.rx(sess.send.seal(b"private pixels" * 4), 1.0)[:7], b"private")
        self.assertNotEqual(skin.residual, b"")
        self.assertEqual(skin.tick(1.05), "LINK")
        self.assertEqual(skin.tick(1.0 + S.DEADMAN_S + 0.01), "NO LINK")
        self.assertEqual(skin.residual, b"")                  # nothing left to read
        core.drop(skin.pub)                                   # the Core lost the link
        self.assertFalse(core.unlocked(2.0))
        self.assertEqual(S.connect(core, skin, DetRng(b"j"), now=60.0)[0], "OK")
        self.assertEqual(core.compose([(S.PRIVATE, "balance")], skin.pub, 61.0),
                         [(S.PUBLIC, "locked")])
        skin.power_off()
        self.assertIsNone(skin.rx(b"\x00" * 40, 70.0))        # no plaintext fallback

    def test_a_rogue_base_station_reads_and_forges_nothing_at_c2(self):
        validator = S.Core(VENDOR.pub, wallet_seed=b"validator", rng=DetRng(b"val"))
        validator.distance = "C2"
        leaf = S.SkinChip(b"leaf-u7", VENDOR, clock=Tick())
        S.pair(validator, leaf)                               # the lease, in the model
        validator.unlock(validator.hw.press(), 0.0)
        seen = []

        def tap(name, msg):
            seen.append(repr(msg).encode())
            return msg

        st, sess = S.connect(validator, leaf, DetRng(b"c2"), mitm=tap)
        self.assertEqual(st, "OK")
        slice_ = sess.send.seal(b"frame 1 balance 12345")
        self.assertNotIn(b"balance", slice_)
        bad = bytearray(slice_)
        bad[-1] ^= 1
        self.assertIsNone(leaf.recv.open(bytes(bad)))         # a forged slice
        self.assertEqual(leaf.recv.open(slice_), b"frame 1 balance 12345")
        self.assertIsNone(leaf.recv.open(slice_))              # a replayed slice

    def test_the_aead_at_c2_costs_almost_nothing(self):
        b = S.aead_budget(0.15)
        self.assertLess(b["power_mW"][5.0], 1.0)
        self.assertLess(b["buffer_KiB"], 1.0)

    def test_the_rtt_proof_only_bounds_distance_from_above(self):
        self.assertEqual(S.fibre_slack_km(), 100.0)           # the 1 ms margin
        self.assertEqual(S.rtt_class(2000, "wifi", True), "room")
        self.assertEqual(S.rtt_class(2000, "wifi", False), "metro")
        self.assertEqual(S.rtt_class(5100, "wifi", False), "far")
        self.assertEqual(S.rtt_class(4900, "5g", False), "cell")
        rank = {"room": 0, "metro": 1, "cell": 1, "far": 2}
        for bearer in ("wifi", "5g"):
            for uwb in (True, False):
                prev = 0
                for rtt in range(500, 9000, 100):
                    r = rank[S.rtt_class(rtt, bearer, uwb)]
                    self.assertGreaterEqual(r, prev)         # more delay, never nearer
                    prev = r
        # a relay adds delay and never removes it
        base = S.rtt_class(2500, "wifi", False)
        self.assertEqual(base, "metro")
        self.assertEqual(S.rtt_class(2500 + 3000, "wifi", False), "far")


class MixedFleet(unittest.TestCase):
    """One account, a Skin at C0 and a Leaf at C2."""

    def setUp(self):
        self.core, self.skin = paired(seed_core=b"home-core")
        self.leaf = S.Core(VENDOR.pub, wallet_seed=b"leaf-u7", rng=DetRng(b"leafrng"))
        self.acct = S.Account(self.core.wallet_pub)
        body = self.acct._body(S.TAG_ACCT + b"add", self.leaf.wallet_pub, 50, 1)
        self.assertEqual(self.acct.add(self.core.wallet_pub, self.leaf.wallet_pub, 50, 1,
                                       H.ed_sign(self.core._wallet, body)), "OK")

    def spend(self, who, amount, day=1):
        body = self.acct._body(S.TAG_ACCT + b"spend", who.wallet_pub, amount, day)
        return self.acct.spend(who.wallet_pub, amount, day, H.ed_sign(who._wallet, body))

    def test_a_stolen_skin_cannot_spend_at_all(self):
        raw = hashlib.sha256(b"skin:s1").digest()
        body = self.acct._body(S.TAG_ACCT + b"spend", self.skin.pub, 1, 1)
        r = self.acct.spend(self.skin.pub, 1, 1, H.ed_sign(raw, body))   # the thief's best try
        self.assertIn("unknown or revoked", r)

    def test_a_stolen_leaf_is_not_glass_it_drains_to_its_cap_and_no_further(self):
        self.assertEqual(self.spend(self.leaf, 30), "OK")
        self.assertEqual(self.spend(self.leaf, 20), "OK")
        self.assertIn("over the cap", self.spend(self.leaf, 1))
        self.assertEqual(self.spend(self.leaf, 1, day=2), "OK")       # the next day it resets

    def test_the_core_revokes_a_stolen_leaf_and_the_leaf_cannot_revoke_the_core(self):
        body = self.acct._body(S.TAG_ACCT + b"rev", self.leaf.wallet_pub, 0, 2)
        self.assertEqual(self.acct.revoke(self.core.wallet_pub, self.leaf.wallet_pub, 2,
                                          H.ed_sign(self.core._wallet, body)), "OK")
        self.assertIn("revoked", self.spend(self.leaf, 1))
        body = self.acct._body(S.TAG_ACCT + b"rev", self.core.wallet_pub, 0, 3)
        self.assertEqual(self.acct.revoke(self.leaf.wallet_pub, self.core.wallet_pub, 3,
                                          H.ed_sign(self.leaf._wallet, body)), "REFUSED")
        body = self.acct._body(S.TAG_ACCT + b"add", b"\x09" * 32, 10 ** 9, 3)
        self.assertEqual(self.acct.add(self.leaf.wallet_pub, b"\x09" * 32, 10 ** 9, 3,
                                       H.ed_sign(self.leaf._wallet, body)), "REFUSED")

    def test_a_capped_leaf_key_cannot_add_keys_or_replay_the_add(self):
        body = self.acct._body(S.TAG_ACCT + b"add", self.leaf.wallet_pub, 10 ** 6, 1)
        self.assertEqual(self.acct.add(self.core.wallet_pub, self.leaf.wallet_pub, 10 ** 6, 1,
                                       H.ed_sign(self.core._wallet, body)), "REFUSED")   # ctr 1 used

    def test_the_two_surfaces_use_two_trust_models_under_one_account(self):
        self.assertEqual(S.trust_model("C0")["wallet_in"], "Core U7")
        self.assertEqual(S.trust_model("C2")["wallet_in"], "Leaf U7, as L.6.0")
        self.assertNotEqual(self.core.wallet_pub, self.leaf.wallet_pub)   # keys never copy
        self.assertEqual(self.acct.keys[self.leaf.wallet_pub]["cap"], 50)
        self.assertIsNone(self.acct.keys[self.core.wallet_pub]["cap"])


if __name__ == "__main__":
    unittest.main()
