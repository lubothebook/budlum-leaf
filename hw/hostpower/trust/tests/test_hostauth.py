"""Tests of the host trust model: a host that feeds the Leaf gains no authority.

Run: python3 -m unittest discover -s tests   (from hw/hostpower/trust)
"""
import hashlib
import os
import random
import struct
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import hostauth as H  # noqa: E402


class DetRng:
    """A deterministic nonce source, so every test is repeatable."""

    def __init__(self, seed=b"t"):
        self.seed, self.n = seed, 0

    def __call__(self, k):
        self.n += 1
        return hashlib.sha256(self.seed + struct.pack(">Q", self.n)).digest()[:k]


def secret(label):
    return hashlib.sha256(b"secret:" + label.encode()).digest()


HOST = secret("host")
HOST_PUB = H.ed_public(HOST)
OTHER = secret("counterfeit")
OTHER_PUB = H.ed_public(OTHER)
ADAPTER = secret("port-part")
ADAPTER_PUB = H.ed_public(ADAPTER)
WALLET = secret("wallet")
PROGRAM = secret("program")


# byte offsets in the record: B Q 32s B B I H H B B Q Q 32s H H
OFF_KIND = 1 + 8 + 32
OFF_CLASS = OFF_KIND + 1
OFF_ROLE = OFF_CLASS + 1 + 4 + 2 + 2
OFF_LANES = OFF_ROLE + 1


def make(u7, key=HOST, cls=2, **kw):
    """Open a challenge and build a signed frame for it."""
    nonce = u7.challenge()
    _, vmin, vmax, pw = H.CLASSES[cls]
    f = dict(chain_id=1, host_key=H.ed_public(key), kind=H.KIND_HOST, cls=cls,
             max_power_mw=pw, v_min_mv=vmin, v_max_mv=vmax, role=H.ROLE_NONE,
             lanes=0, expiry=u7.anchor_height + 100, counter=1, nonce=nonce,
             meas_mv=5000, meas_ma=50)
    f.update(kw)
    rec = H.HostRecord(**f)
    return H.sign_record(key, rec)


def fresh(ceiling=3, lanes_ok=False, active=(), **kw):
    u7 = U7_(active=active, **kw)
    u7.pair(HOST_PUB, ceiling, lanes_ok=lanes_ok, presence=True)
    u7.attach(True, 5000)
    return u7


def U7_(active=(), **kw):
    u = H.U7(rng=DetRng(), active_validators=active, **kw)
    return u


class Primitive(unittest.TestCase):
    def test_ed25519_rfc8032_vectors(self):
        sk = bytes.fromhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
        pk = bytes.fromhex("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
        sig = bytes.fromhex(
            "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555f"
            "b8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b")
        self.assertEqual(H.ed_public(sk), pk)
        self.assertEqual(H.ed_sign(sk, b""), sig)
        self.assertTrue(H.ed_verify_strict(pk, b"", sig))
        sk2 = bytes.fromhex("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb")
        pk2 = bytes.fromhex("3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c")
        self.assertEqual(H.ed_public(sk2), pk2)
        self.assertTrue(H.ed_verify_strict(pk2, b"\x72", H.ed_sign(sk2, b"\x72")))

    def test_strict_verify_refuses_malleable_and_small_order(self):
        sig = H.ed_sign(HOST, b"m")
        s = int.from_bytes(sig[32:], "little") + H._Q          # S + L
        mall = sig[:32] + s.to_bytes(32, "little")
        self.assertFalse(H.ed_verify_strict(HOST_PUB, b"m", mall))
        identity = b"\x01" + b"\x00" * 31                      # a small-order key
        self.assertFalse(H.ed_verify_strict(identity, b"m", sig))
        self.assertFalse(H.ed_verify_strict(HOST_PUB, b"other", sig))


class Parser(unittest.TestCase):
    def test_frame_is_fixed_length(self):
        u = fresh()
        self.assertEqual(len(make(u)), H.FRAME_LEN)
        self.assertEqual(H.FRAME_LEN, 169)

    def test_every_bad_field_is_refused(self):
        u = fresh()
        good = make(u)
        cases = {"version": (0, 9), "kind": (OFF_KIND, 7), "class": (OFF_CLASS, 0),
                 "role": (OFF_ROLE, 5), "lanes": (OFF_LANES, 2)}
        for name, (off, val) in cases.items():
            bad = bytearray(good)
            bad[off] = val
            with self.assertRaises(H.ParseError, msg=name):
                H.parse_frame(bytes(bad))
        for n in (0, 1, H.FRAME_LEN - 1, H.FRAME_LEN + 1, 4096):
            with self.assertRaises(H.ParseError):
                H.parse_frame(b"\x01" * n)

    def test_fuzz_only_parse_errors(self):
        u = fresh()
        good = make(u)
        rnd = random.Random(7)
        for _ in range(3000):
            b = bytearray(good)
            for _ in range(rnd.randint(1, 4)):
                b[rnd.randrange(len(b))] = rnd.randrange(256)
            try:
                H.parse_frame(bytes(b))
            except H.ParseError:
                pass
        for _ in range(2000):
            n = rnd.choice([H.FRAME_LEN, rnd.randrange(0, 400)])
            try:
                H.parse_frame(bytes(rnd.randrange(256) for _ in range(n)))
            except H.ParseError:
                pass

    def test_no_wallet_identifier_before_the_handshake(self):
        u = fresh()
        nonce = u.challenge()
        self.assertEqual(len(nonce), 32)        # the only thing that leaves U7
        self.assertNotIn(WALLET, nonce)


class Classes(unittest.TestCase):
    def test_every_class_row_inside_the_leaf_rating(self):
        for c in H.CLASSES:
            self.assertTrue(H.leaf_current_ok(c), c)

    def test_p1_covers_the_islanded_ring(self):
        self.assertGreaterEqual(H.CLASSES[1][3], 400)   # hw/energy/03 Section 1.2

    def test_bridge_envelope_does_not_trust_the_class(self):
        p0 = H.Grant(0, "R1", "")
        p1 = H.Grant(1, "R2", "")
        p3 = H.Grant(3, "R4", "")
        for v in (0, 5000, 20000, 36000):
            self.assertEqual(H.bridge_state(p0, v, 1)[0], "OPEN")
        self.assertEqual(H.bridge_state(p1, 9000, 100)[0], "OPEN")
        self.assertEqual(H.bridge_state(p1, 5000, 100)[0], "CLOSED")
        self.assertEqual(H.bridge_state(p1, 5000, 5000)[0], "LIMIT")
        self.assertEqual(H.bridge_state(p3, 15000, 20000)[0], "CLOSED")
        self.assertEqual(H.bridge_state(p3, 24500, 20000)[0], "OPEN")
        self.assertEqual(H.bridge_state(p3, 12000, 20000)[0], "OPEN")


class Handshake(unittest.TestCase):
    def test_valid_host_gets_its_class(self):
        u = fresh(ceiling=3)
        g = u.respond(make(u, cls=2))
        self.assertEqual((g.cls, g.row, g.lanes), (2, "R4", False))

    def test_unauthenticated_host_gets_power_only_low_class(self):
        u = H.U7(rng=DetRng())
        g = u.attach(True, 5000)
        self.assertEqual((g.cls, g.row, g.lanes), (1, "R2", False))
        g = u.respond(b"")
        self.assertEqual((g.cls, g.lanes), (1, False))

    def test_refused_adapter_keeps_pads_at_zero(self):
        u = H.U7(rng=DetRng())
        g = u.attach(False, 5000)
        self.assertEqual((g.cls, g.row), (0, "R1"))
        u.challenge()
        self.assertEqual(u.respond(make(u)).cls, 0)

    def test_unauthenticated_host_at_the_wrong_volts_gets_nothing(self):
        u = H.U7(rng=DetRng())
        self.assertEqual(u.attach(True, 9000).cls, 0)
        self.assertEqual(u.attach(True, 20000).cls, 0)

    def test_counterfeit_host_with_an_unknown_key(self):
        u = fresh()
        g = u.respond(make(u, key=OTHER, cls=3))
        self.assertEqual(g.cls, 1)
        self.assertIn("unknown host key", g.reason)

    def test_counterfeit_host_forges_a_trusted_key(self):
        u = fresh()
        nonce = u.challenge()
        rec = H.HostRecord(1, HOST_PUB, 0, 3, 27000, 13500, 16500, 0, 0, 2000, 1,
                           nonce, 5000, 50)
        frame = rec.pack() + H.ed_sign(OTHER, rec.signing_bytes())   # wrong key
        g = u.respond(frame)
        self.assertEqual(g.cls, 1)
        self.assertIn("bad signature", g.reason)

    def test_tampered_record_fails_the_signature(self):
        u = fresh(ceiling=3)
        frame = bytearray(make(u, cls=2))
        frame[OFF_CLASS] = 3                 # raise the class after signing
        g = u.respond(bytes(frame))
        self.assertEqual(g.cls, 1)
        self.assertIn("bad signature", g.reason)

    def test_replayed_frame_and_single_use_nonce(self):
        u = fresh()
        frame = make(u)
        self.assertEqual(u.respond(frame).cls, 2)
        self.assertEqual(u.respond(frame).cls, 1)         # no open challenge
        u.challenge()
        g = u.respond(frame)                              # a new nonce is open
        self.assertIn("nonce mismatch", g.reason)

    def test_replayed_counter_with_a_fresh_nonce(self):
        u = fresh()
        self.assertEqual(u.respond(make(u, counter=5)).cls, 2)
        g = u.respond(make(u, counter=5))
        self.assertIn("replayed counter", g.reason)
        g = u.respond(make(u, counter=4))
        self.assertIn("replayed counter", g.reason)
        self.assertEqual(u.respond(make(u, counter=6)).cls, 2)

    def test_replay_after_a_power_cut_is_refused_with_nvm_counters(self):
        u = fresh()
        self.assertEqual(u.respond(make(u, counter=9)).cls, 2)
        u.power_cycle()                                   # the host cuts power
        u.attach(True, 5000)
        g = u.respond(make(u, counter=9))
        self.assertIn("replayed counter", g.reason)

    def test_the_hole_ram_counters_reopen_replay_after_a_power_cut(self):
        """The finding. fw/u7 keeps session state in RAM (open issue U7-8). A
        host that controls power resets any RAM counter."""
        u = fresh(ram_counters=True)
        self.assertEqual(u.respond(make(u, counter=9)).cls, 2)
        u.power_cycle()
        u.attach(True, 5000)
        self.assertEqual(u.respond(make(u, counter=9)).cls, 2)   # accepted again

    def test_expired_record(self):
        u = fresh()
        g = u.respond(make(u, expiry=u.anchor_height))
        self.assertIn("expired", g.reason)
        g = u.respond(make(u, expiry=u.anchor_height - 5))
        self.assertEqual(g.cls, 1)
        self.assertEqual(u.respond(make(u, expiry=u.anchor_height + 1)).cls, 2)

    def test_a_stale_anchor_expires_every_record(self):
        u = fresh()
        u.tick(H.MAX_ANCHOR_AGE_S + 1)
        u.attach(True, 5000)
        g = u.respond(make(u, expiry=10 ** 9))
        self.assertIn("stale", g.reason)
        u.advance_anchor(u.anchor_height + 10)
        self.assertEqual(u.respond(make(u, expiry=10 ** 9, counter=2)).cls, 2)

    def test_over_class_request(self):
        u = fresh(ceiling=2)
        g = u.respond(make(u, cls=3))
        self.assertEqual(g.cls, 1)
        self.assertIn("over-class", g.reason)

    def test_a_lower_request_gets_the_lower_class(self):
        u = fresh(ceiling=3)
        self.assertEqual(u.respond(make(u, cls=1, counter=1)).cls, 1)
        self.assertEqual(u.respond(make(u, cls=2, counter=2)).cls, 2)

    def test_a_record_outside_its_class_row_is_refused(self):
        u = fresh(ceiling=3)
        g = u.respond(make(u, cls=2, max_power_mw=40000))
        self.assertIn("outside its class row", g.reason)
        g = u.respond(make(u, cls=2, v_max_mv=20000, counter=2))
        self.assertIn("outside its class row", g.reason)

    def test_wrong_chain(self):
        u = fresh()
        self.assertIn("wrong chain", u.respond(make(u, chain_id=2)).reason)

    def test_relay_fails_the_power_channel_binding(self):
        """A relay forwards the genuine host's record, but its own power line
        measures other volts than the host reports."""
        u = fresh()
        g = u.respond(make(u, meas_mv=9000))              # local pad shows 5000
        self.assertIn("binding", g.reason)
        self.assertEqual(g.cls, 1)
        self.assertEqual(u.respond(make(u, meas_mv=5100, counter=2)).cls, 2)

    def test_a_vouch_never_exceeds_p2_and_keeps_lanes_dead(self):
        u = H.U7(rng=DetRng())
        u.pair(ADAPTER_PUB, 3, lanes_ok=True, presence=True, origin="FACTORY")
        u.attach(True, 5000)
        g = u.respond(make(u, key=ADAPTER, cls=3, kind=H.KIND_VOUCH))
        self.assertIn("never exceeds P2", g.reason)
        g = u.respond(make(u, key=ADAPTER, cls=2, kind=H.KIND_VOUCH, lanes=1, counter=2))
        self.assertEqual((g.cls, g.row, g.lanes), (2, "R3", False))

    def test_the_grant_dies_without_a_fresh_record(self):
        u = fresh()
        self.assertEqual(u.respond(make(u)).cls, 2)
        self.assertEqual(u.tick(H.REAUTH_S - 1).cls, 2)
        g = u.tick(2)
        self.assertEqual((g.cls, g.row), (1, "R6"))
        u.challenge()
        self.assertEqual(u.respond(make(u, counter=2)).cls, 2)

    def test_pairing_needs_the_owner(self):
        u = H.U7(rng=DetRng())
        with self.assertRaises(PermissionError):
            u.pair(HOST_PUB, 3)
        with self.assertRaises(PermissionError):
            u.unpair(HOST_PUB)
        u.pair(HOST_PUB, 3, presence=True)
        u.unpair(HOST_PUB, presence=True)
        u.attach(True, 5000)
        self.assertEqual(u.respond(make(u)).cls, 1)

    def test_data_lanes_are_dead_unless_every_condition_holds(self):
        # not requested, not allowed by the owner, class P1, a vouch
        u = fresh(lanes_ok=False)
        self.assertFalse(u.respond(make(u, lanes=1)).lanes)
        u = fresh(lanes_ok=True)
        self.assertFalse(u.respond(make(u, lanes=0)).lanes)
        self.assertFalse(u.respond(make(u, cls=1, lanes=1, counter=2)).lanes)
        self.assertTrue(u.respond(make(u, cls=2, lanes=1, counter=3)).lanes)
        # every failure path leaves them dead
        for bad in (b"", b"\x00" * H.FRAME_LEN, make(u, key=OTHER, lanes=1)):
            u.challenge()
            self.assertFalse(u.respond(bad).lanes)

    def test_every_policy_row_is_reached(self):
        seen = set()
        u = H.U7(rng=DetRng())
        seen.add(u.attach(False, 5000).row)
        seen.add(u.attach(True, 5000).row)
        u.pair(HOST_PUB, 3, presence=True)
        u.pair(ADAPTER_PUB, 2, presence=True, origin="FACTORY")
        u.attach(True, 5000)
        seen.add(u.respond(make(u, key=ADAPTER, cls=2, kind=H.KIND_VOUCH)).row)
        seen.add(u.respond(make(u, counter=2)).row)
        u.active = {HOST_PUB}
        seen.add(u.respond(make(u, counter=3, role=H.ROLE_VALIDATOR)).row)
        seen.add(u.tick(H.REAUTH_S + 1).row)
        self.assertEqual(seen, set(H.POLICY_ROWS))


class ValidatorHost(unittest.TestCase):
    def test_the_role_claim_never_moves_the_power_class(self):
        for ceiling in (1, 2, 3):
            a = fresh(ceiling=ceiling, active={HOST_PUB})
            b = fresh(ceiling=ceiling, active={HOST_PUB})
            ga = a.respond(make(a, cls=min(ceiling, 2), role=H.ROLE_VALIDATOR))
            gb = b.respond(make(b, cls=min(ceiling, 2), role=H.ROLE_NONE))
            self.assertEqual(ga.cls, gb.cls)
            self.assertLessEqual(ga.cls, ceiling)
        # an unknown validator key gets the unauthenticated class whatever it claims
        u = H.U7(rng=DetRng(), active_validators={OTHER_PUB})
        u.attach(True, 5000)
        g = u.respond(make(u, key=OTHER, role=H.ROLE_VALIDATOR, cls=3))
        self.assertEqual(g.cls, 1)

    def test_a_false_role_claim_is_ignored(self):
        u = fresh(active=set())
        g = u.respond(make(u, role=H.ROLE_VALIDATOR))
        self.assertEqual(g.cls, 2)
        self.assertFalse(g.role_claim_ok)
        self.assertEqual(g.row, "R4")

    def test_validator_host_with_a_bad_stream_key(self):
        """A valid P3 host that streams with a key outside the active set gets
        its power and the safe screen. Power and rendering are independent."""
        u = fresh(ceiling=3, active={HOST_PUB})
        g = u.respond(make(u, cls=3, role=H.ROLE_VALIDATOR))
        self.assertEqual((g.cls, g.row, g.role_claim_ok), (3, "R5", True))
        self.assertEqual(u.render(OTHER_PUB), "SAFE_SCREEN")
        self.assertEqual(u.render(b"\x00" * 32), "SAFE_SCREEN")
        self.assertEqual(u.render(HOST_PUB), "STREAM")
        self.assertEqual(u.grant.cls, 3)

    def test_render_needs_no_power_class(self):
        u = H.U7(rng=DetRng(), active_validators={HOST_PUB})
        u.attach(True, 5000)                                   # P1 only
        self.assertEqual(u.render(HOST_PUB), "STREAM")         # radios carry it
        self.assertEqual(u.grant.cls, 1)

    def test_a_validator_that_left_the_set_loses_the_stream(self):
        u = fresh(active={HOST_PUB})
        self.assertEqual(u.render(HOST_PUB), "STREAM")
        u.active.discard(HOST_PUB)
        self.assertEqual(u.render(HOST_PUB), "SAFE_SCREEN")

    def test_a_stale_anchor_refuses_the_stream(self):
        """The eclipse rule. A host that is the only network path cannot
        starve the light client and keep a rotated-out validator alive."""
        u = fresh(active={HOST_PUB})
        u.tick(H.MAX_ANCHOR_AGE_S + 1)
        self.assertEqual(u.render(HOST_PUB), "SAFE_SCREEN")
        u.advance_anchor(u.anchor_height + 1)
        self.assertEqual(u.render(HOST_PUB), "STREAM")


class Signing(unittest.TestCase):
    def test_island_signing_survives_a_host_cut_at_every_phase(self):
        for phase in range(0, 6):
            u = fresh()
            o = H.sign_atomic(u, WALLET, b"input batch", host_cut_at=phase)
            self.assertEqual(o.reason, "RELEASED", phase)
            body = struct.pack(">Q", 1) + b"input batch"
            self.assertTrue(H.ed_verify_strict(H.ed_public(WALLET), body, o.released))
            self.assertEqual(u.state["lastsign"], 1)          # burned exactly once

    def test_the_naive_design_loses_or_reuses(self):
        lost = reused = 0
        for phase in range(0, 7):
            u = fresh()
            o = H.sign_atomic(u, WALLET, b"A", design="naive", host_cut_at=phase)
            if o.released == b"":
                lost += 1
            if o.reason.startswith("RELEASED then"):
                reused += 1
                # the counter never committed: the next signature reuses it
                o2 = H.sign_atomic(u, WALLET, b"B", design="naive")
                self.assertEqual(o2.counter, o.counter + 1)
                self.assertEqual(o2.counter, u.state["lastsign"])
                body = struct.pack(">Q", o2.counter) + b"A"
                self.assertTrue(H.ed_verify_strict(H.ed_public(WALLET), body, o.released))
        self.assertGreater(lost, 0)
        self.assertEqual(reused, 1)

    def test_island_design_never_reuses_a_counter(self):
        u = fresh()
        seen = []
        for i, phase in enumerate([None, 1, 3, 5, 2]):
            o = H.sign_atomic(u, WALLET, f"m{i}".encode(), host_cut_at=phase)
            seen.append(o.counter)
        self.assertEqual(seen, [1, 2, 3, 4, 5])

    def test_a_glitch_during_signing_releases_nothing(self):
        u = fresh()
        o = H.sign_atomic(u, WALLET, b"m", glitch_phase=3)
        self.assertEqual(o.released, b"")
        self.assertIn("FAULT", o.reason)
        self.assertEqual(o.faults, 1)
        o2 = H.sign_atomic(u, WALLET, b"m")
        self.assertEqual(o2.counter, 2)                       # the burned one is gone

    def test_a_glitch_campaign_ends_in_a_lockout_not_a_leak(self):
        u = fresh()
        released = 0
        for _ in range(H.FAULT_LIMIT):
            released += len(H.sign_atomic(u, WALLET, b"m", glitch_phase=3).released)
        self.assertEqual(released, 0)
        o = H.sign_atomic(u, WALLET, b"m", glitch_phase=3)
        self.assertIn("LOCKOUT", o.reason)
        o = H.sign_atomic(u, WALLET, b"m", attached=False)    # the owner detaches
        self.assertEqual(o.reason, "RELEASED")
        self.assertEqual(u.state["faults"], 0)

    def test_residual_a_double_glitch_releases_a_faulty_signature(self):
        """The honest limit. A second glitch that skips the self-verify
        releases a bad signature. The chain refuses it; the silicon needs
        redundant checks (open issue O3)."""
        u = fresh()
        o = H.sign_atomic(u, WALLET, b"m", glitch_phase=3, glitch_hits_verify=True)
        self.assertNotEqual(o.released, b"")
        body = struct.pack(">Q", o.counter) + b"m"
        self.assertFalse(H.ed_verify_strict(H.ed_public(WALLET), body, o.released))

    def test_a_low_store_refuses_without_burning_the_counter(self):
        u = fresh()
        o = H.sign_atomic(u, WALLET, b"m", store_mJ=0.5, e_chunk_mJ=1.0)
        self.assertIn("REFUSED", o.reason)
        self.assertEqual(u.state["lastsign"], 0)


class Atomic(unittest.TestCase):
    def test_nvm_cut_at_every_step_reads_old_or_new(self):
        for step in range(H.NVM_COMMIT_STEPS):
            nvm = H.NVM()
            nvm.commit({"v": 1})
            try:
                nvm.commit({"v": 2}, cut_at=step)
            except H.PowerLoss:
                pass
            self.assertIn(nvm.read()["v"], (1, 2), step)
            nvm.commit({"v": 3})                              # it keeps working
            self.assertEqual(nvm.read()["v"], 3)
        # a cut on the very first write leaves nothing or the new value, never junk
        for step in range(H.NVM_COMMIT_STEPS):
            nvm = H.NVM()
            try:
                nvm.commit({"v": 1}, cut_at=step)
            except H.PowerLoss:
                pass
            self.assertIn(nvm.read(), (None, {"v": 1}))

    def test_a_cut_in_the_counter_commit_never_leaves_a_grant(self):
        for step in range(H.NVM_COMMIT_STEPS):
            u = fresh()
            with self.assertRaises(H.PowerLoss):
                u.respond(make(u, counter=7), cut_at=step)
            u.power_cycle()
            self.assertEqual(u.grant.cls, 0)                  # RAM grant is gone
            self.assertIn(u.state["ctr"].get(HOST_PUB.hex(), 0), (0, 7))
            u.attach(True, 5000)
            g = u.respond(make(u, counter=8))                 # the host tries again
            self.assertEqual(g.cls, 2)

    def _device(self):
        first = H.make_release(PROGRAM, 1)
        return H.Device(H.ed_public(PROGRAM), first), H.make_release(PROGRAM, 2)

    def _total_ticks(self):
        d, new = self._device()
        d.install(new)
        d.boot()
        return d.ticks

    def test_update_cut_at_every_tick_never_bricks_and_resumes(self):
        total = self._total_ticks()
        self.assertGreater(total, 10)
        for cut in range(total):
            d, new = self._device()
            d.cut_at = cut
            try:
                d.install(new)
                d.boot()
            except H.PowerLoss:
                pass
            d.cut_at = None
            s = d.nvm.read()
            self.assertIn(s["floor"], (1, 2), cut)
            # a boot that is not cut: it must find a verified slot
            probe, _ = self._probe(d)
            self.assertIsNotNone(probe, f"brick at tick {cut}")
            self.assertIn(d.flash[probe].seq, (1, 2))
            # the host returns: the update resumes and completes
            d2 = d
            d2.install(new)
            slot, verdict = d2.boot()
            self.assertEqual(d2.flash[slot].seq, 2, cut)
            self.assertEqual(d2.nvm.read()["floor"], 2)

    def _probe(self, d):
        """Which slot would a boot pick, with no side effect."""
        s = d.nvm.read()
        for slot in (s["active"], "B" if s["active"] == "A" else "A"):
            if d.bootable(slot, s["floor"]):
                return slot, None
        return None, None

    def test_the_floor_rises_only_with_a_clean_trial(self):
        d, new = self._device()
        self.assertEqual(d.install(new), "TRIAL_PENDING")
        self.assertEqual(d.nvm.read()["floor"], 1)
        slot, verdict = d.boot(trial_clean=False)
        self.assertEqual((slot, verdict), ("A", "REVERTED"))
        self.assertEqual(d.nvm.read()["floor"], 1)

    def test_a_hostile_host_cutting_every_trial_only_defers(self):
        d, new = self._device()
        d.install(new)
        for _ in range(H.TRIAL_LIMIT):
            d.ticks, d.cut_at = 0, 0
            with self.assertRaises(H.PowerLoss):
                d.boot()
        d.cut_at = None
        slot, verdict = d.boot()
        self.assertEqual((slot, verdict), ("A", "DEFERRED"))
        self.assertEqual(d.nvm.read()["floor"], 1)
        # a stable host later: the update installs
        d.install(new)
        self.assertEqual(d.boot()[1], "COMMITTED")

    def test_a_host_that_cuts_after_every_chunk_cannot_stop_progress(self):
        d, new = self._device()
        attempts = 0
        while attempts < 3 * len(new.chunks) + 6:
            attempts += 1
            d.ticks, d.cut_at = 0, 3
            try:
                r = d.install(new)
                break
            except H.PowerLoss:
                continue
        self.assertEqual(r, "TRIAL_PENDING")
        self.assertLessEqual(attempts, len(new.chunks) + 2)

    def test_an_update_needs_the_energy_of_its_commit(self):
        d, new = self._device()
        self.assertIn("REFUSED", d.install(new, store_ok=False))
        self.assertEqual(d.nvm.read()["target"], None)

    def test_a_bad_image_never_boots(self):
        d, new = self._device()
        evil = H.make_release(secret("not the program key"), 2)
        d.install(evil)
        self.assertEqual(d.nvm.read()["pending"], None)       # the verify refused it
        slot, verdict = d.boot()
        self.assertEqual((slot, verdict), ("A", "OK"))
        new.chunks[2] = b"tampered"
        d2, _ = self._device()
        self.assertEqual(d2.install(new), "REJECTED")


class Analysis(unittest.TestCase):
    def test_store_sizing(self):
        for e in (1.0, 5.0, 20.0):
            z = H.store_sizing(e)
            self.assertLess(z["C_iteration_mF"], z["C_mean_mF"])
            self.assertLess(z["C_mean_mF"], z["C_worst_mF"])
        z = H.store_sizing(5.0)
        self.assertAlmostEqual(z["C_iteration_mF"], 0.64, places=2)
        self.assertEqual(z["k_99_99"], 31)
        self.assertAlmostEqual(H.loop_count_entropy_bits(), 3.18, places=2)

    def test_the_island_rail_rides_through_a_short_host_drop(self):
        r = H.simulate_rail(H.drop_wave(100, 2000), 6000, dt_us=2.0)
        self.assertTrue(r.in_window)
        self.assertEqual(r.bod_trip_us, float("inf"))

    def test_the_brownout_trip_leads_the_loss_of_the_island_rail(self):
        r = H.simulate_rail(H.drop_wave(100, 20000), 25000, dt_us=2.0)
        self.assertFalse(r.in_window)
        self.assertGreater(r.bod_margin_us, 1000)     # at least 1 ms of warning
        self.assertAlmostEqual(r.bod_trip_us / 1000, H.ride_through_ms(), delta=0.3)

    def test_a_host_spike_does_not_reach_the_island(self):
        for us in (1, 100, 5000):
            r = H.simulate_rail(H.spike_wave(100, us), 100 + us + 2000, dt_us=0.5)
            self.assertTrue(r.in_window)
            self.assertLess(r.v_island_max, 1.8 * 1.01)

    def test_filtering_alone_is_not_a_defence(self):
        self.assertGreater(H.line_attenuation_db(1e6), -40)   # about 34 dB at 1 MHz
        self.assertLess(H.line_attenuation_db(1e6), -30)

    def test_the_update_window_comes_from_fw_boot(self):
        self.assertAlmostEqual(H.update_window_s(), 9.04, places=1)

    def test_the_sideband_precharge_is_slow_but_bounded(self):
        self.assertLess(H.sideband_precharge_ms(), 150)


if __name__ == "__main__":
    unittest.main()
