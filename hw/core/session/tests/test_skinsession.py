"""Tests of the Skin session model: modes, the merge, the pairing, the roam."""
import os
import random
import sys
import unittest
from dataclasses import replace

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import skinsession as K  # noqa: E402
S = K.S

NAMES = ["leaf_wallet", "core_a", "core_b", "leaf_session", "val1", "val2", "val_evil"]


def rig(n=3, size=(1600, 3200), core="core_a"):
    keys = S.Keys(NAMES)
    reg = K.PairingRegistry()
    core = K.Core(core, keys, reg)
    skins = [K.Skin(f"skin{i}", *size) for i in range(n)]
    for sk in skins:
        reg.pair(sk.skin_id, core.core_id, wallet_signed=True)
        assert core.attach(sk)
    return keys, reg, core, skins


class SkinHoldsNothing(unittest.TestCase):
    def test_the_skin_has_no_signing_method(self):
        sk = K.Skin("s", 10, 10)
        self.assertFalse(any(n in dir(sk) for n in ("sign", "sign_tx", "wallet", "key_pair")))

    def test_the_held_state_has_no_session_field(self):
        held = K.Skin("s", 10, 10).held_state()
        for bad in ("session", "nonce", "balance", "state_root", "grant"):
            self.assertFalse(any(bad in str(v) for v in held.values()), bad)

    def test_a_power_cycle_loses_only_volatile_things(self):
        keys, reg, core, skins = rig(1)
        sk = skins[0]
        self.assertTrue(sk.link_key)
        sk.power_cycle()
        self.assertEqual(sk.link_key, b"")
        self.assertEqual(sk.skin_id, "skin0")

    def test_a_skin_power_cycle_leaves_the_session_root(self):
        keys, reg, core, skins = rig(1)
        led = core.open_session("S")
        core.bind(K.MIRROR, skins, sid="S")
        twin = K.CoreLedger("S", keys, "core_a", validators=("val1", "val2"))
        led.run_to(100)
        skins[0].power_cycle()
        led.run_to(200)
        twin.run_to(200)
        self.assertEqual(led.s.app_root(), twin.s.app_root())
        self.assertEqual(led.s.status, S.ACTIVE)

    def test_a_skin_that_comes_back_works_with_the_same_pairing(self):
        keys, reg, core, skins = rig(1)
        core.open_session("S")
        core.bind(K.MIRROR, skins, sid="S")
        skins[0].power_cycle()
        self.assertTrue(core.attach(skins[0]))
        core.bind(K.MIRROR, skins, sid="S")
        got = core.ingest([(skins[0].make_event("touch", 1, 1), 1.0)])
        self.assertEqual(len(got), 1)


class Pairing(unittest.TestCase):
    def test_pairing_needs_the_wallet(self):
        reg = K.PairingRegistry()
        with self.assertRaises(PermissionError):
            reg.pair("s", "core_a", wallet_signed=False)

    def test_an_unpaired_skin_cannot_attach(self):
        keys, reg, core, skins = rig(1)
        stranger = K.Skin("stranger", 10, 10)
        self.assertFalse(core.attach(stranger))

    def test_a_skin_paired_to_another_core_cannot_attach(self):
        keys, reg, a, skins = rig(1)
        b = K.Core("core_b", keys, reg)
        self.assertFalse(b.attach(skins[0]))

    def test_a_new_pairing_moves_the_skin_and_raises_the_epoch(self):
        keys, reg, a, skins = rig(1)
        e1 = reg.current("skin0")[1]
        reg.pair("skin0", "core_b", wallet_signed=True)
        self.assertEqual(reg.current("skin0")[1], e1 + 1)
        b = K.Core("core_b", keys, reg)
        self.assertTrue(b.attach(skins[0]))

    def test_an_allowed_core_takes_the_skin_without_the_wallet(self):
        keys, reg, a, skins = rig(1)
        reg.allow("skin0", "core_b", wallet_signed=True)
        e = reg.take("skin0", "core_b")
        self.assertEqual(reg.current("skin0")[:2], ("core_b", e))

    def test_a_core_the_wallet_did_not_allow_cannot_take_the_skin(self):
        keys, reg, a, skins = rig(1)
        with self.assertRaises(PermissionError):
            reg.take("skin0", "core_b")

    def test_allow_needs_the_wallet(self):
        keys, reg, a, skins = rig(1)
        with self.assertRaises(PermissionError):
            reg.allow("skin0", "core_b", wallet_signed=False)

    def test_the_old_core_loses_the_skin_at_once(self):
        keys, reg, a, skins = rig(1)
        a.open_session("S")
        a.bind(K.MIRROR, skins, sid="S")
        ev = skins[0].make_event("touch", 1, 1)
        reg.pair("skin0", "core_b", wallet_signed=True)
        self.assertEqual(a.ingest([(ev, 1.0)]), [])
        self.assertIn(a.dropped[-1][0], ("stale pairing", "bad mac"))

    def test_link_keys_differ_by_core_and_epoch(self):
        keys, reg, a, skins = rig(1)
        k1 = skins[0].link_key
        reg.pair("skin0", "core_b", wallet_signed=True)
        b = K.Core("core_b", keys, reg)
        sk2 = K.Skin("skin0", 10, 10)
        b.attach(sk2)
        self.assertNotEqual(k1, sk2.link_key)

    def test_a_revoked_skin_is_dropped(self):
        keys, reg, a, skins = rig(1)
        a.open_session("S")
        a.bind(K.MIRROR, skins, sid="S")
        ev = skins[0].make_event("touch", 1, 1)
        reg.revoke("skin0", wallet_signed=True)
        self.assertEqual(a.ingest([(ev, 1.0)]), [])

    def test_a_rogue_skin_with_a_guessed_key_is_dropped(self):
        keys, reg, a, skins = rig(1)
        a.open_session("S")
        a.bind(K.MIRROR, skins, sid="S")
        rogue = K.Skin("skin0", 10, 10)
        rogue.link_key = b"guess"
        rogue.pairing_epoch = 1
        self.assertEqual(a.ingest([(rogue.make_event("touch", 1, 1), 1.0)]), [])
        self.assertEqual(a.dropped[-1][0], "bad mac")

    def test_a_tampered_event_is_dropped(self):
        keys, reg, a, skins = rig(1)
        a.open_session("S")
        a.bind(K.MIRROR, skins, sid="S")
        ev = replace(skins[0].make_event("touch", 1, 1), x=999)
        self.assertEqual(a.ingest([(ev, 1.0)]), [])


class Modes(unittest.TestCase):
    def test_mirror_binds_every_skin_to_one_session(self):
        keys, reg, core, skins = rig(3)
        core.open_session("S")
        views = core.bind(K.MIRROR, skins, sid="S")
        self.assertEqual({v.session_id for v in views}, {"S"})
        self.assertEqual(len(views), 3)

    def test_mirror_scales_a_touch_to_the_canvas(self):
        keys, reg, core, skins = rig(1)
        small = K.Skin("small", 800, 1600)
        reg.pair("small", "core_a", True)
        core.attach(small)
        core.open_session("S")
        core.bind(K.MIRROR, [small], sid="S")
        got = core.ingest([(small.make_event("touch", 400, 800), 1.0)])
        sid, pt, led = core.route(got[0])
        self.assertEqual(pt, (400, 800))     # scaled against the skin size, canvas = the skin here

    def test_extend_tiles_are_disjoint_and_cover_the_canvas(self):
        keys, reg, core, skins = rig(3)
        core.open_session("S")
        views = core.bind(K.EXTEND, skins, sid="S")
        sets = [K.tiles_of(v.rect) for v in views]
        for i in range(3):
            for j in range(i + 1, 3):
                self.assertEqual(sets[i] & sets[j], set())
        rects, canvas = K.extend_layout(skins)
        self.assertEqual(set().union(*sets), K.tiles_of((0, 0) + canvas))

    def test_extend_canvas_is_the_union(self):
        keys, reg, core, skins = rig(3)
        rects, canvas = K.extend_layout(skins)
        self.assertEqual(canvas, (4800, 3200))

    def test_extend_maps_the_second_skin_to_its_offset(self):
        keys, reg, core, skins = rig(3)
        core.open_session("S")
        core.bind(K.EXTEND, skins, sid="S")
        got = core.ingest([(skins[1].make_event("touch", 10, 20), 1.0)])
        sid, pt, led = core.route(got[0])
        self.assertEqual(pt, (1610, 20))

    def test_split_runs_independent_sessions(self):
        keys, reg, core, skins = rig(3)
        for i in range(3):
            core.open_session(f"S{i}")
        core.bind(K.SPLIT, skins, sids=["S0", "S1", "S2"])
        evs = [(skins[i].make_event("touch", 1, 1), 1.0 + i) for i in range(2)]
        ordered = core.ingest(evs)
        for e in core.state_changing(ordered):
            sid, pt, led = core.route(e)
            led.submit(10, core.sign_input(sid, e, 10))
        for led in core.ledgers.values():
            led.run_to(50)
        bal = [core.ledgers[f"S{i}"].s.app.balance for i in range(3)]
        self.assertEqual(bal, [1, 1, 0])

    def test_split_pause_of_one_session_leaves_the_others(self):
        keys, reg, core, skins = rig(2)
        for i in range(2):
            core.open_session(f"S{i}").run_to(50)
        led = core.ledgers["S0"]
        led.submit(50, S.sign_tx(keys, S.PauseTx("S0", 1, "VIEWS_LOST", 50, led.s.app_root()), signer="core_a"))
        for l in core.ledgers.values():
            l.run_to(100)
        self.assertEqual(core.ledgers["S0"].s.status, S.PAUSED)
        self.assertEqual(core.ledgers["S1"].s.status, S.ACTIVE)

    def test_the_ledger_sees_one_writer_for_every_mode(self):
        keys, reg, core, skins = rig(3)
        led = core.open_session("S")
        core.bind(K.EXTEND, skins, sid="S")
        evs = [(sk.make_event("touch", 5, 5), 1.0) for sk in skins]
        for e in core.state_changing(core.ingest(evs)):
            led.submit(10, core.sign_input("S", e, 10))
        led.run_to(50)
        self.assertEqual(led.rejects, [])
        self.assertEqual(led.s.app.balance, 3)
        self.assertEqual(led.writer, "core_a")


class Merge(unittest.TestCase):
    def _events(self, rnd, skins, n):
        out = []
        for i in range(n):
            sk = rnd.choice(skins)
            kind = rnd.choice(["touch", "pen", "key", "imu", "camera", "shutter"])
            out.append((sk.make_event(kind, rnd.randint(0, 99), rnd.randint(0, 99)),
                        rnd.uniform(0, 40)))
        return out

    def test_the_order_never_depends_on_arrival_order(self):
        keys, reg, core, skins = rig(4)
        core.open_session("S")
        core.bind(K.EXTEND, skins, sid="S")
        rnd = random.Random(1)
        batch = self._events(rnd, skins, 300)
        base = [(e.skin_id, e.seq) for e in core.ingest(list(batch))]
        for _ in range(20):
            rnd.shuffle(batch)
            self.assertEqual([(e.skin_id, e.seq) for e in core.ingest(list(batch))], base)

    def test_each_skin_keeps_its_own_order(self):
        keys, reg, core, skins = rig(3)
        core.open_session("S")
        core.bind(K.EXTEND, skins, sid="S")
        # one Skin sends in order and each event arrives no earlier than the last
        evs, t = [], 0.0
        for i in range(50):
            t += random.Random(i).uniform(0.0, 1.0)
            evs.append((skins[0].make_event("touch", i, 0), t))
        got = [e.seq for e in core.ingest(evs) if e.skin_id == "skin0"]
        self.assertEqual(got, sorted(got))

    def test_nothing_is_lost_in_the_merge(self):
        keys, reg, core, skins = rig(3)
        core.open_session("S")
        core.bind(K.MIRROR, skins, sid="S")
        batch = self._events(random.Random(2), skins, 400)
        self.assertEqual(len(core.ingest(batch)), 400)

    def test_pen_orders_before_touch_in_the_same_tick(self):
        keys, reg, core, skins = rig(2)
        core.open_session("S")
        core.bind(K.EXTEND, skins, sid="S")
        got = core.ingest([(skins[0].make_event("touch", 1, 1), 1.0),
                           (skins[1].make_event("pen", 1, 1), 1.0)])
        self.assertEqual([e.kind for e in got], ["pen", "touch"])

    def test_imu_and_camera_are_not_state_transactions(self):
        keys, reg, core, skins = rig(1)
        core.open_session("S")
        core.bind(K.MIRROR, skins, sid="S")
        got = core.ingest([(skins[0].make_event(k, 1, 1), 1.0) for k in ("imu", "camera", "shutter", "touch")])
        sc = core.state_changing(got)
        self.assertEqual(sorted(e.kind for e in sc), ["shutter", "touch"])

    def test_the_skin_never_stamps_the_tick(self):
        keys, reg, core, skins = rig(1)
        self.assertEqual(skins[0].make_event("touch").tick, -1)

    def test_a_tick_is_one_480_hz_scan(self):
        self.assertAlmostEqual(K.TICK_MS, 2.0833, places=3)

    def test_two_replicas_of_the_order_agree(self):
        keys, reg, core, skins = rig(3)
        core.open_session("S")
        core.bind(K.EXTEND, skins, sid="S")
        batch = self._events(random.Random(9), skins, 120)
        a = core.ingest(list(batch))
        b = K.Core.merge([replace(e) for e in a])
        self.assertEqual(a, b)


class Handoff(unittest.TestCase):
    def test_a_handoff_never_pauses_the_session(self):
        keys, reg, core, skins = rig(2)
        led = core.open_session("S")
        core.bind(K.SPLIT, skins[:1], sids=["S"])
        led.run_to(100)
        v = core.handoff("S", "skin0", "skin1")
        led.run_to(200)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertEqual(led.s.resume_seq, 0)
        self.assertEqual(v.epoch, 1)

    def test_the_old_skin_is_cut_off_after_a_handoff(self):
        keys, reg, core, skins = rig(2)
        core.open_session("S")
        core.bind(K.SPLIT, skins[:1], sids=["S"])
        ev = skins[0].make_event("touch", 1, 1)
        core.handoff("S", "skin0", "skin1")
        self.assertEqual(core.ingest([(ev, 1.0)]), [])
        self.assertEqual(core.dropped[-1][0], "no view")

    def test_the_new_skin_drives_the_session(self):
        keys, reg, core, skins = rig(2)
        led = core.open_session("S")
        core.bind(K.SPLIT, skins[:1], sids=["S"])
        core.handoff("S", "skin0", "skin1")
        got = core.ingest([(skins[1].make_event("touch", 1, 1), 1.0)])
        self.assertEqual(len(got), 1)

    def test_a_handoff_of_a_session_the_skin_does_not_show_fails(self):
        keys, reg, core, skins = rig(2)
        core.open_session("S")
        core.bind(K.SPLIT, skins[:1], sids=["S"])
        with self.assertRaises(KeyError):
            core.handoff("T", "skin0", "skin1")

    def test_the_frame_store_stays_on_the_core(self):
        keys, reg, core, skins = rig(2)
        core.open_session("S")
        core.frame_store["S"] = b"last frame"
        core.bind(K.SPLIT, skins[:1], sids=["S"])
        core.handoff("S", "skin0", "skin1")
        self.assertEqual(core.frame_store["S"], b"last frame")


def roam_run(events, end, pause_at, gap, grant_b=True, dead_a=False):
    """A session on Core A, paused (or lapsed), resumed by Core B as a second writer."""
    keys = S.Keys(NAMES)
    led = K.CoreLedger("S", keys, "core_a", validators=("val1", "val2"))
    nonce = 0
    for f, ev in [(f, e) for f, e in events if f < pause_at]:
        led.submit(f, S.sign_tx(keys, S.InputTx("S", 0, nonce, f, ev), signer="core_a"))
        nonce += 1
    led.run_to(pause_at)
    if dead_a:
        led.run_to(pause_at + 3 * S.FPS)
        led.submit(led.wall, S.sign_tx(keys, S.LapseTx("S", 1, led.s.last_leaf_second, "val1")))
        led.run_to(led.wall + 1)
        paused_at = led.wall
        gap_eff = gap
    else:
        led.submit(pause_at, S.sign_tx(keys, S.PauseTx("S", 1, "VIEWS_LOST", led.s.frame_no,
                                                       led.s.app_root()), signer="core_a"))
        led.run_to(pause_at + 1)
        paused_at = pause_at
    if grant_b:
        led.submit(led.wall, K.sign_grant(keys, K.GrantWriterTx("S", "core_b", 10 ** 12)))
        led.run_to(led.wall + 1)
    led.run_to(paused_at + gap)
    r = led.wall
    res = S.sign_tx(keys, S.ResumeTx("S", 1, 1, led.s.paused_root, "core_b"), signer="core_b")
    led.submit(r, res)
    led.run_to(r + 1)
    return keys, led, r


class Roam(unittest.TestCase):
    def test_core_b_resumes_the_same_state(self):
        keys, led, r = roam_run([(10, ("tap",)), (30, ("key", 65))], 200, 100, 5000)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertEqual(led.writer, "core_b")
        self.assertEqual(led.s.app.balance, 1)
        self.assertEqual(led.s.app.text, (65,))

    def test_a_roam_leaves_the_state_of_a_run_with_no_roam(self):
        rnd = random.Random(5)
        for trial in range(40):
            frames = sorted(rnd.sample(range(5, 2000), 12))
            events = [(f, rnd.choice([("tap",), ("key", rnd.randint(65, 90)),
                                      ("scroll", rnd.randint(-200, 200)), ("fling", rnd.randint(-60, 60))]))
                      for f in frames]
            pause_at = rnd.randint(20, 2000)
            gap = rnd.choice([3, 240, 10 ** 5, 10 ** 7])
            # the reference: the same events, one Core, no pause
            keys = S.Keys(NAMES)
            ref = K.CoreLedger("S", keys, "core_a", validators=("val1", "val2"))
            for i, (f, ev) in enumerate(events):
                ref.submit(f, S.sign_tx(keys, S.InputTx("S", 0, i, f, ev), signer="core_a"))
            before = [(f, e) for f, e in events if f < pause_at]
            after = [(f, e) for f, e in events if f >= pause_at]
            keys2, led, r = roam_run(events, 0, pause_at, gap)
            shift = r - pause_at
            for i, (f, ev) in enumerate(after):
                led.submit(f + shift, S.sign_tx(keys2, S.InputTx("S", 1, len(before) + i, f + shift, ev),
                                                signer="core_b"))
            ref.run_to(2100)
            led.run_to(2100 + shift)
            self.assertEqual(led.s.app_root(), ref.s.app_root(), (trial, pause_at, gap))
            self.assertEqual([x for x in led.rejects], [], (trial, led.rejects[:2]))

    def test_a_core_without_a_grant_cannot_resume(self):
        keys, led, r = roam_run([], 100, 50, 500, grant_b=False)
        self.assertEqual(led.s.status, S.PAUSED)
        self.assertEqual(led.rejects[-1][2], "NOT_A_WRITER")

    def test_a_grant_not_signed_by_the_wallet_is_refused(self):
        keys = S.Keys(NAMES)
        led = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        bad = K.GrantWriterTx("S", "core_b", 10 ** 12, sig=keys.sign("core_b", K.GRANT_DOMAIN, "S", "core_b", 10 ** 12))
        led.submit(0, bad)
        led.run_to(2)
        self.assertEqual(led.rejects[-1][2], "BAD_SIGNATURE")
        self.assertNotIn("core_b", led.grants)

    def test_the_old_core_cannot_write_after_the_roam(self):
        keys, led, r = roam_run([], 100, 50, 500)
        late = S.sign_tx(keys, S.InputTx("S", 1, led.s.nonce, led.wall, ("tap",)), signer="core_a")
        led.submit(led.wall, late)
        led.run_to(led.wall + 2)
        self.assertEqual(led.s.app.balance, 0)
        self.assertEqual(led.rejects[-1][2], "BAD_SIGNATURE")

    def test_an_input_withheld_by_core_a_cannot_fire_on_core_b(self):
        keys = S.Keys(NAMES)
        led = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        held = S.sign_tx(keys, S.InputTx("S", 0, 0, 20, ("tap",)), signer="core_a")
        led.run_to(20)
        led.submit(20, S.sign_tx(keys, S.PauseTx("S", 1, "VIEWS_LOST", 20, led.s.app_root()), signer="core_a"))
        led.run_to(25)
        led.submit(25, K.sign_grant(keys, K.GrantWriterTx("S", "core_b", 10 ** 12)))
        led.run_to(30)
        led.submit(30, S.sign_tx(keys, S.ResumeTx("S", 1, 1, led.s.paused_root, "core_b"), signer="core_b"))
        led.run_to(31)
        led.submit(32, held)
        led.run_to(40)
        self.assertEqual(led.s.app.balance, 0)

    def test_a_stale_root_resume_by_core_b_is_refused(self):
        keys = S.Keys(NAMES)
        led = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        led.run_to(20)
        led.submit(20, S.sign_tx(keys, S.PauseTx("S", 1, "VIEWS_LOST", 20, led.s.app_root()), signer="core_a"))
        led.run_to(25)
        led.submit(25, K.sign_grant(keys, K.GrantWriterTx("S", "core_b", 10 ** 12)))
        led.run_to(30)
        led.submit(30, S.sign_tx(keys, S.ResumeTx("S", 1, 1, b"\x00" * 32, "core_b"), signer="core_b"))
        led.run_to(31)
        self.assertEqual(led.rejects[-1][2], "RESUME_STATE_MISMATCH")

    def test_the_session_is_never_live_on_two_cores(self):
        keys, led, r = roam_run([], 100, 50, 500)
        # Core A tries to pause again: it is not the writer
        led.submit(led.wall, S.sign_tx(keys, S.PauseTx("S", 2, "X", 1, led.s.app_root()), signer="core_a"))
        led.run_to(led.wall + 2)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertEqual(led.writer, "core_b")

    def test_core_a_dead_the_session_follows_by_lapse(self):
        keys, led, r = roam_run([(10, ("tap",))], 100, 50, 3000, dead_a=True)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertEqual(led.writer, "core_b")
        self.assertEqual(led.s.app.balance, 1)

    def test_an_expired_writer_grant_is_refused(self):
        keys = S.Keys(NAMES)
        led = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        led.run_to(20)
        led.submit(20, S.sign_tx(keys, S.PauseTx("S", 1, "VIEWS_LOST", 20, led.s.app_root()), signer="core_a"))
        led.submit(21, K.sign_grant(keys, K.GrantWriterTx("S", "core_b", 100)))
        led.run_to(500)
        led.submit(500, S.sign_tx(keys, S.ResumeTx("S", 1, 1, led.s.paused_root, "core_b"), signer="core_b"))
        led.run_to(501)
        self.assertEqual(led.rejects[-1][2], "GRANT_EXPIRED")

    def test_core_b_adopts_the_nonce_from_the_chain(self):
        keys, led, r = roam_run([(10, ("tap",)), (20, ("tap",))], 100, 50, 500)
        b = K.Core("core_b", keys, K.PairingRegistry())
        b.adopt_session(led)
        self.assertEqual(b.nonce["S"], led.s.nonce)
        self.assertEqual(led.s.nonce, 2)


class TakeOver(unittest.TestCase):
    """RG-19A rule R13: a granted writer takes a live session with no pause."""

    def _pair(self):
        keys = S.Keys(NAMES)
        led = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        led.submit(0, K.sign_grant(keys, K.GrantWriterTx("S", "core_b", 10 ** 12)))
        led.run_to(1)
        return keys, led

    def _inp(self, keys, who, epoch, nonce, at, ev=("tap",)):
        return S.sign_tx(keys, S.InputTx("S", epoch, nonce, at, ev), signer=who)

    def test_takeover_changes_the_writer_and_not_the_state(self):
        keys, led = self._pair()
        ref = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        for i, f in enumerate((10, 20)):
            led.submit(f, self._inp(keys, "core_a", 0, i, f))
            ref.submit(f, self._inp(keys, "core_a", 0, i, f))
        led.submit(30, K.sign_takeover(keys, K.TakeOverTx("S", "core_b", 0)))
        for i, f in enumerate((40, 50)):
            led.submit(f, self._inp(keys, "core_b", 1, 2 + i, f))
            ref.submit(f, self._inp(keys, "core_a", 0, 2 + i, f))
        led.run_to(200)
        ref.run_to(200)
        self.assertEqual(led.rejects, [])
        self.assertEqual(led.writer, "core_b")
        self.assertEqual(led.s.app_root(), ref.s.app_root())
        self.assertEqual(led.s.status, S.ACTIVE)

    def test_takeover_needs_a_grant(self):
        keys = S.Keys(NAMES)
        led = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        led.submit(5, K.sign_takeover(keys, K.TakeOverTx("S", "core_b", 0)))
        led.run_to(10)
        self.assertEqual(led.rejects[-1][2], "NOT_A_WRITER")
        self.assertEqual(led.writer, "core_a")

    def test_takeover_with_a_forged_signature_is_refused(self):
        keys, led = self._pair()
        bad = K.TakeOverTx("S", "core_b", 0, sig=keys.sign("core_a", K.TAKEOVER_DOMAIN, "S", "core_b", 0))
        led.submit(5, bad)
        led.run_to(10)
        self.assertEqual(led.rejects[-1][2], "BAD_SIGNATURE")

    def test_the_old_writer_is_refused_after_a_takeover(self):
        keys, led = self._pair()
        led.submit(5, K.sign_takeover(keys, K.TakeOverTx("S", "core_b", 0)))
        led.submit(6, self._inp(keys, "core_a", 0, 0, 6))
        led.run_to(20)
        self.assertEqual(led.s.app.balance, 0)
        self.assertEqual(led.rejects[-1][2], "BAD_SIGNATURE")

    def test_an_input_ordered_before_the_takeover_still_counts(self):
        keys, led = self._pair()
        led.submit(5, self._inp(keys, "core_a", 0, 0, 5))
        led.submit(6, K.sign_takeover(keys, K.TakeOverTx("S", "core_b", 0)))
        led.run_to(20)
        self.assertEqual(led.s.app.balance, 1)

    def test_a_takeover_with_a_stale_epoch_is_refused(self):
        keys, led = self._pair()
        led.submit(5, K.sign_takeover(keys, K.TakeOverTx("S", "core_b", 3)))
        led.run_to(10)
        self.assertEqual(led.rejects[-1][2], "STALE_EPOCH")

    def test_a_takeover_of_a_paused_session_is_refused(self):
        keys, led = self._pair()
        led.submit(5, S.sign_tx(keys, S.PauseTx("S", 1, "X", 5, led.s.app_root()), signer="core_a"))
        led.run_to(8)
        led.submit(9, K.sign_takeover(keys, K.TakeOverTx("S", "core_b", 0)))
        led.run_to(12)
        self.assertEqual(led.rejects[-1][2], "SESSION_NOT_ACTIVE")

    def test_an_expired_writer_grant_cannot_take_over(self):
        keys = S.Keys(NAMES)
        led = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        led.submit(0, K.sign_grant(keys, K.GrantWriterTx("S", "core_b", 50)))
        led.run_to(100)
        led.submit(100, K.sign_takeover(keys, K.TakeOverTx("S", "core_b", 0)))
        led.run_to(110)
        self.assertEqual(led.rejects[-1][2], "GRANT_EXPIRED")

    def test_two_cores_pass_the_session_back_and_forth(self):
        keys, led = self._pair()
        ref = K.CoreLedger("S", keys, "core_a", validators=("val1",))
        who, epoch, nonce = "core_a", 0, 0
        for step in range(20):
            f = 10 + step * 20
            led.submit(f, self._inp(keys, who, epoch, nonce, f))
            ref.submit(f, self._inp(keys, "core_a", 0, nonce, f))
            nonce += 1
            nxt = "core_b" if who == "core_a" else "core_a"
            led.submit(f + 5, K.sign_takeover(keys, K.TakeOverTx("S", nxt, epoch)))
            who, epoch = nxt, epoch + 1
        led.run_to(600)
        ref.run_to(600)
        self.assertEqual(led.rejects, [])
        self.assertEqual(led.s.resume_seq, 20)
        self.assertEqual(led.s.app_root(), ref.s.app_root())


if __name__ == "__main__":
    unittest.main()
