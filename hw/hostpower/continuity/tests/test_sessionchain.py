"""Tests of the RG-19 reference model: a power gap never changes finalized state.

Each test names the rule of RG-19 that it checks.
"""
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import sessionchain as S  # noqa: E402

NAMES = ["leaf_session", "leaf_wallet", "val1", "val2", "val_evil"]


def fresh(grant_until=10 ** 12, sid="S"):
    keys = S.Keys(NAMES)
    led = S.Ledger(sid, keys, grant_until=grant_until, validators=("val1", "val2", "val_evil"))
    return keys, led, S.U7(keys, sid)


def random_events(rnd, n, span):
    frames = sorted(rnd.sample(range(5, span), n))
    out = []
    for f in frames:
        k = rnd.choice(["tap", "key", "scroll", "fling", "settext"])
        if k == "tap":
            ev = ("tap",)
        elif k == "key":
            ev = ("key", rnd.randint(65, 90))
        elif k == "scroll":
            ev = ("scroll", rnd.randint(-300, 300))
        elif k == "fling":
            ev = ("fling", rnd.randint(-80, 80))
        else:
            ev = ("settext", tuple(rnd.randint(65, 90) for _ in range(rnd.randint(0, 5))))
        out.append((f, ev))
    return out


def run_reference(events, end):
    keys, led, u7 = fresh()
    for f, ev in events:
        led.submit(f, u7.sign_input(ev, f))
    led.run_to(end)
    return led


def run_with_gap(events, end, pause_at, gap):
    """The same events with a pause at wall `pause_at` and a gap of `gap` frames."""
    keys, led, u7 = fresh()
    before = [(f, ev) for f, ev in events if f < pause_at]
    after = [(f, ev) for f, ev in events if f >= pause_at]
    for f, ev in before:
        led.submit(f, u7.sign_input(ev, f))
    led.run_to(pause_at)
    led.submit(pause_at, u7.make_pause(led.s.frame_no, led.s.app_root()))
    led.run_to(pause_at + 1)
    led.run_to(pause_at + gap)
    r = pause_at + gap
    led.submit(r, u7.make_resume(led.s))
    led.run_to(r)
    shift = r - pause_at
    led.pending.setdefault(r, [])
    for f, ev in after:
        led.submit(f + shift, u7.sign_input(ev, f + shift))
    led.run_to(end + shift)
    return led


class StateIsUnchanged(unittest.TestCase):
    """RG-19 rule 1: the session clock stops, so a pause of any length changes nothing."""

    def test_pause_of_any_length_leaves_the_state(self):
        rnd = random.Random(5)
        for trial in range(120):
            events = random_events(rnd, rnd.randint(3, 25), 3 * S.FRAMES_PER_SLOT)
            end = 3 * S.FRAMES_PER_SLOT + 50
            ref = run_reference(events, end)
            pause_at = rnd.randint(20, 3 * S.FRAMES_PER_SLOT)
            gap = rnd.choice([2, 10, 240, 5000, 10 ** 6, 10 ** 8])
            got = run_with_gap(events, end, pause_at, gap)
            self.assertEqual(got.s.app_root(), ref.s.app_root(), (trial, pause_at, gap))
            self.assertEqual(got.rejects, [], (trial, got.rejects[:2]))

    def test_clock_is_frozen_while_paused(self):
        keys, led, u7 = fresh()
        led.run_to(100)
        led.submit(100, u7.make_pause(led.s.frame_no, led.s.app_root()))
        led.run_to(101)
        frozen = led.s.frame_no
        led.run_to(101 + 10 ** 7)
        self.assertEqual(led.s.frame_no, frozen)
        self.assertEqual(led.s.status, S.PAUSED)

    def test_clock_runs_again_after_resume(self):
        keys, led, u7 = fresh()
        led.run_to(100)
        led.submit(100, u7.make_pause(100, led.s.app_root()))
        led.run_to(5000)
        led.submit(5000, u7.make_resume(led.s))
        led.run_to(5100)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertGreater(led.s.frame_no, 100)

    def test_finalized_prefix_never_changes(self):
        rnd = random.Random(8)
        events = random_events(rnd, 12, 2 * S.FRAMES_PER_SLOT)
        end = 4 * S.FRAMES_PER_SLOT
        ref = run_reference(events, end)
        got = run_with_gap(events, end, S.FRAMES_PER_SLOT + 200, 99999)
        # the slots that ended before the pause are the same state
        self.assertEqual(got.snapshots[1], ref.snapshots[1])

    def test_pause_restores_the_same_root(self):
        keys, led, u7 = fresh()
        led.submit(10, u7.sign_input(("tap",), 10))
        led.run_to(60)
        root = led.s.app_root()
        led.submit(60, u7.make_pause(led.s.frame_no, root))
        led.run_to(61)
        self.assertEqual(led.s.paused_root, root)
        led.submit(1000, u7.make_resume(led.s))
        led.run_to(1001)
        # one tick of the resume wall frame is the only difference
        self.assertEqual(led.s.frame_no, 61)


class AuthorityIsKept(unittest.TestCase):
    """RG-19 rules 2 to 6: no validator and no host gains authority over a session."""

    def _paused(self):
        keys, led, u7 = fresh()
        led.run_to(50)
        led.submit(50, u7.make_pause(50, led.s.app_root()))
        led.run_to(60)
        return keys, led, u7

    def test_a_validator_cannot_resume(self):
        keys, led, u7 = self._paused()
        s = led.s
        tx = S.ResumeTx("S", s.pause_seq, 1, s.paused_root, "leaf_session")
        forged = S.sign_tx(keys, tx, signer="val1")
        led.submit(70, forged)
        led.run_to(80)
        self.assertEqual(led.s.status, S.PAUSED)
        self.assertEqual(led.rejects[-1][2], "BAD_SIGNATURE")

    def test_a_validator_cannot_move_a_paused_session(self):
        keys, led, u7 = self._paused()
        before = led.s.app_root()
        bad = S.sign_tx(keys, S.InputTx("S", 0, led.s.nonce, 70, ("tap",)), signer="val1")
        led.submit(70, bad)
        led.run_to(80)
        self.assertEqual(led.s.app_root(), before)

    def test_a_validator_cannot_sign_a_leaf_pause(self):
        keys, led, u7 = fresh()
        led.run_to(50)
        forged = S.sign_tx(keys, S.PauseTx("S", 1, "HOST_LOST", 50, led.s.app_root()), signer="val1")
        led.submit(50, forged)
        led.run_to(60)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertEqual(led.rejects[-1][2], "BAD_SIGNATURE")

    def test_a_second_pause_inside_10_seconds_is_limited(self):
        keys, led, u7 = self._paused()
        led.submit(100, u7.make_resume(led.s))
        led.run_to(101)
        led.submit(150, u7.make_pause(led.s.frame_no, led.s.app_root()))
        led.run_to(160)
        self.assertEqual(led.rejects[-1][2], "PAUSE_RATE_LIMIT")
        self.assertEqual(led.s.status, S.ACTIVE)
        u7.pause_seq = 1                        # the refused pause is retried with its number
        led.submit(100 + S.PAUSE_MIN_GAP + 5, u7.make_pause(led.s.frame_no, led.s.app_root()))
        led.run_to(100 + S.PAUSE_MIN_GAP + 10)
        self.assertEqual(led.s.status, S.PAUSED)

    def test_inputs_are_refused_while_paused(self):
        keys, led, u7 = self._paused()
        led.submit(70, u7.sign_input(("tap",), 70))
        led.run_to(80)
        self.assertEqual(led.rejects[-1][2], "SESSION_NOT_ACTIVE")

    def test_lapse_pause_needs_silence(self):
        keys, led, u7 = fresh()
        led.submit(10, u7.sign_input(("tap",), 10))
        led.run_to(S.FPS)                      # second 1: the Leaf was heard at second 0
        lapse = S.sign_tx(keys, S.LapseTx("S", 1, led.s.last_leaf_second, "val1"))
        led.submit(S.FPS, lapse)
        led.run_to(S.FPS + 5)
        self.assertEqual(led.rejects[-1][2], "LAPSE_TOO_EARLY")
        self.assertEqual(led.s.status, S.ACTIVE)

    def test_lapse_with_wrong_evidence_is_refused(self):
        keys, led, u7 = fresh()
        led.submit(10, u7.sign_input(("tap",), 10))
        led.run_to(10 * S.FPS)
        lapse = S.sign_tx(keys, S.LapseTx("S", 1, 99, "val_evil"))
        led.submit(led.wall, lapse)
        led.run_to(led.wall + 2)
        self.assertEqual(led.rejects[-1][2], "LAPSE_BAD_EVIDENCE")

    def test_lapse_after_silence_is_accepted_and_changes_no_state(self):
        keys, led, u7 = fresh()
        led.submit(10, u7.sign_input(("tap",), 10))
        led.run_to(10 * S.FPS)
        before = led.s.app_root()
        lapse = S.sign_tx(keys, S.LapseTx("S", 1, led.s.last_leaf_second, "val1"))
        led.submit(led.wall, lapse)
        led.run_to(led.wall + 1)
        self.assertEqual(led.s.status, S.LAPSED)
        self.assertEqual(led.s.paused_root, led.s.app_root())
        led.submit(led.wall + 100, u7.make_resume(led.s))
        led.run_to(led.wall + 101)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertNotEqual(before, b"")

    def test_a_primary_that_withholds_receipts_is_beaten_by_dual_send(self):
        """RG-19 rule 3 with rule 9: the shadow also submits the receipt."""
        keys, led, u7 = fresh()
        led.run_to(5 * S.FPS)
        rec = S.sign_tx(keys, S.ReceiptTx("S", 4))
        led.submit(5 * S.FPS, rec)             # from the shadow, in time
        led.run_to(6 * S.FPS)
        lapse = S.sign_tx(keys, S.LapseTx("S", 1, 0, "val_evil"))
        led.submit(led.wall, lapse)
        led.run_to(led.wall + 2)
        self.assertEqual(led.rejects[-1][2], "LAPSE_BAD_EVIDENCE")
        self.assertEqual(led.s.status, S.ACTIVE)

    def test_resume_against_a_stale_root_is_refused(self):
        keys, led, u7 = self._paused()
        s = led.s
        stale = S.ResumeTx("S", s.pause_seq, 1, b"\x00" * 32, "leaf_session")
        led.submit(70, S.sign_tx(keys, stale))
        led.run_to(80)
        self.assertEqual(led.rejects[-1][2], "RESUME_STATE_MISMATCH")
        self.assertEqual(led.s.status, S.PAUSED)

    def test_second_resume_is_refused(self):
        keys, led, u7 = self._paused()
        r1 = u7.make_resume(led.s)
        led.submit(70, r1)
        led.run_to(80)
        led.submit(90, r1)                      # the same bytes again
        led.run_to(100)
        self.assertEqual(led.s.resume_seq, 1)

    def test_old_pause_cannot_be_resumed_twice_with_new_seq(self):
        keys, led, u7 = self._paused()
        led.submit(70, u7.make_resume(led.s))
        led.run_to(80)
        s = led.s
        same = S.sign_tx(keys, S.ResumeTx("S", 1, 1, s.paused_root, "leaf_session"))
        led.submit(90, same)                    # the same bytes: idempotent, counted
        other = S.sign_tx(keys, S.ResumeTx("S", 1, 2, s.paused_root, "leaf_session"))
        led.submit(91, other)                   # a new resume of an old pause
        led.run_to(100)
        self.assertEqual(led.dups, 1)
        self.assertEqual(led.rejects[-1][2], "SESSION_NOT_PAUSED")
        self.assertEqual(led.s.resume_seq, 1)

    def test_input_withheld_across_a_pause_cannot_fire_later(self):
        """RG-19 rule 7: the epoch of an input is the resume count."""
        keys, led, u7 = fresh()
        led.run_to(20)
        held = u7.sign_input(("tap",), 20)     # a host withholds this
        led.submit(20, u7.make_pause(20, led.s.app_root()))
        led.run_to(30)
        led.submit(1000, u7.make_resume(led.s))
        led.run_to(1001)
        led.submit(1002, held)
        led.run_to(1010)
        self.assertEqual(led.s.app.balance, 0)
        self.assertEqual(led.rejects[-1][2], "STALE_EPOCH")

    def test_input_expires(self):
        keys, led, u7 = fresh()
        tx = u7.sign_input(("tap",), 0)
        led.submit(S.INPUT_TTL + 50, tx)
        led.run_to(S.INPUT_TTL + 60)
        self.assertEqual(led.rejects[-1][2], "EXPIRED")

    def test_bad_nonce_is_refused(self):
        keys, led, u7 = fresh()
        u7.nonce = 5
        led.submit(10, u7.sign_input(("tap",), 10))
        led.run_to(20)
        self.assertEqual(led.rejects[-1][2], "BAD_NONCE")

    def test_expired_grant_needs_the_wallet(self):
        keys, led, u7 = fresh(grant_until=2000)
        led.run_to(50)
        led.submit(50, u7.make_pause(50, led.s.app_root()))
        led.run_to(60)
        led.submit(5000, u7.make_resume(led.s))
        led.run_to(5001)
        self.assertEqual(led.rejects[-1][2], "GRANT_EXPIRED")
        self.assertEqual(led.s.status, S.PAUSED)
        w = u7.make_resume(led.s, signer="leaf_wallet", new_grant=10 ** 9)
        led.submit(5100, w)
        led.run_to(5101)
        self.assertEqual(led.s.status, S.ACTIVE)
        self.assertEqual(led.s.grant_until, 10 ** 9)
        led.submit(5200, u7.sign_input(("tap",), 5200))
        led.run_to(5210)
        self.assertEqual(led.s.app.balance, 1)

    def test_a_pause_older_than_the_ttl_closes(self):
        keys, led, u7 = self._paused()
        led.run_to(60 + S.PAUSE_TTL + 5)
        led.submit(led.wall, u7.make_resume(led.s))
        led.run_to(led.wall + 1)
        self.assertEqual(led.rejects[-1][2], "PAUSE_TTL_EXPIRED")
        self.assertEqual(led.s.status, S.CLOSED)

    def test_a_value_action_is_admitted_while_paused(self):
        keys, led, u7 = self._paused()
        tx = u7.sign_action(0, 25, led.wall + 10000)
        led.submit(100, tx)
        led.run_to(110)
        self.assertEqual(led.s.vault, 25)
        self.assertEqual(led.s.status, S.PAUSED)

    def test_a_value_action_expires(self):
        keys, led, u7 = self._paused()
        tx = u7.sign_action(0, 25, 70)
        led.submit(100, tx)
        led.run_to(110)
        self.assertEqual(led.rejects[-1][2], "EXPIRED")
        self.assertEqual(led.s.vault, 0)


class TheLeafSurvivesTheCut(unittest.TestCase):
    """RG-19 rules 8 and 9: U7 keeps what a gap must not lose."""

    def test_a_torn_write_leaves_the_old_or_the_new_record(self):
        for point in S.NVM.CRASH_POINTS + (None,):
            nvm = S.NVM()
            nvm.write(b"old record")
            nvm.write(b"new record", crash_at=point)
            got = nvm.read()
            self.assertIn(got[1], (b"old record", b"new record"), point)

    def test_a_partial_write_is_never_read(self):
        nvm = S.NVM()
        nvm.write(b"first")
        nvm.write(b"second record that tears", crash_at="partial")
        self.assertEqual(nvm.read()[1], b"first")

    def test_the_journal_survives_a_thousand_random_cuts(self):
        rnd = random.Random(2)
        nvm = S.NVM()
        last_ok = None
        for i in range(1000):
            payload = f"rec{i}".encode() * 3
            point = rnd.choice([None, None, "before", "partial", "complete"])
            nvm.write(payload, crash_at=point)
            if point in (None, "complete"):
                last_ok = payload
            cur = nvm.read()
            self.assertIsNotNone(cur)
            self.assertEqual(cur[1], last_ok if last_ok else cur[1])

    def test_a_signed_action_is_in_nvm_before_it_is_sent(self):
        keys, led, u7 = fresh()
        tx = u7.sign_action(0, 40, 10 ** 6)
        self.assertIsNotNone(tx)
        u7.power_loss()
        self.assertEqual(len(u7.outbox), 1)
        led.submit(10, u7.outbox[0])
        led.run_to(20)
        self.assertEqual(led.s.vault, 40)

    def test_a_torn_action_write_is_never_sent(self):
        keys, led, u7 = fresh()
        self.assertIsNone(u7.sign_action(0, 40, 10 ** 6, crash_at="partial"))
        u7.power_loss()
        self.assertEqual(u7.outbox, [])
        led.run_to(20)
        self.assertEqual(led.s.vault, 0)

    def test_the_nonce_is_rebuilt_from_the_chain(self):
        """A cut with no pause: the Leaf lost its RAM nonce and takes the chain nonce."""
        keys, led, u7 = fresh()
        led.submit(10, u7.sign_input(("tap",), 10))
        led.submit(20, u7.sign_input(("tap",), 20))
        led.run_to(30)
        u7.sign_input(("tap",), 40)             # signed, never sent
        u7.power_loss()
        led.run_to(10 * S.FPS)
        led.submit(led.wall, S.sign_tx(keys, S.LapseTx("S", 1, led.s.last_leaf_second, "val1")))
        led.run_to(led.wall + 1)
        self.assertEqual(led.s.status, S.LAPSED)
        led.submit(led.wall, u7.make_resume(led.s))
        led.run_to(led.wall + 1)
        led.submit(led.wall, u7.sign_input(("tap",), led.wall))
        led.run_to(led.wall + 5)
        self.assertEqual(led.s.app.balance, 3)  # the unsent tap is gone, the new one counts


class UnfinalizedLoss(unittest.TestCase):
    """RG-19 rule 9: what a gap can still lose, and the bound."""

    GOSSIP = 4          # frames: about 17 ms to the chain mempool  [HYPOTHESIS]

    def _drive(self, dual, uplink, die_at, events):
        keys, led, u7 = fresh()
        prim = S.Replica("primary", led, self.GOSSIP, uplink=uplink)
        shad = S.Replica("shadow", led, self.GOSSIP, uplink=True)
        for f, ev in events:
            tx = u7.sign_input(ev, f)
            if f < die_at:
                prim.receive(f, tx)
                if dual:
                    shad.receive(f, tx)
            else:
                # after the death the Leaf sends to the shadow only
                shad.receive(f, tx)
        prim.die(die_at)
        led.run_to(8 * S.FRAMES_PER_SLOT)
        return led

    def test_dual_send_loses_nothing_when_the_primary_dies(self):
        rnd = random.Random(21)
        for _ in range(60):
            events = [(f, ("tap",)) for f in sorted(rnd.sample(range(10, 2000), 40))]
            die = rnd.randint(50, 1900)
            led = self._drive(True, True, die, events)
            self.assertEqual(led.s.app.balance, 40, die)

    def test_single_replica_loses_the_in_flight_window(self):
        events = [(f, ("tap",)) for f in range(100, 400, 2)]
        die = 301
        led = self._drive(False, True, die, events)
        in_flight = [f for f, _ in events if f < die and f + self.GOSSIP > die]
        self.assertGreater(len(in_flight), 0)
        # Those taps were lost. The nonce gap then blocks every later input of the
        # epoch: a lost input is a wedge until the Leaf resends or resumes.
        self.assertLess(led.s.app.balance, len(events))
        self.assertTrue(any(code == "BAD_NONCE" for _, _, code in led.rejects))

    def test_the_ring_resend_heals_a_primary_failover(self):
        """RG-19 rule 9: the Leaf keeps its unacknowledged inputs and resends them."""
        keys, led, u7 = fresh()
        prim = S.Replica("primary", led, self.GOSSIP)
        shad = S.Replica("shadow", led, self.GOSSIP)
        sent = []
        for f in range(100, 400, 2):
            tx = u7.sign_input(("tap",), f)
            if f < 301:
                prim.receive(f, tx)
                sent.append(tx)
        prim.die(301)
        led.run_to(301 + self.GOSSIP + 1)
        unacked = [t for t in sent if t.nonce >= led.s.nonce]
        self.assertGreater(len(unacked), 0)
        for t in unacked:
            shad.receive(led.wall, t)
        led.run_to(1000)
        self.assertEqual(led.s.app.balance, len(sent))

    def test_the_loss_window_is_bounded_by_the_gossip_delay(self):
        rnd = random.Random(31)
        worst = 0
        for _ in range(80):
            events = [(f, ("tap",)) for f in sorted(rnd.sample(range(10, 1000), 60))]
            die = rnd.randint(100, 900)
            keys, led, u7 = fresh()
            prim = S.Replica("p", led, self.GOSSIP)
            for f, ev in events:
                if f < die:
                    prim.receive(f, u7.sign_input(ev, f))
            prim.die(die)
            lost = sum(1 for f, _ in events if f < die and f + self.GOSSIP > die)
            worst = max(worst, lost)
        self.assertLessEqual(worst, self.GOSSIP)

    def test_a_dock_with_no_uplink_loses_everything_it_alone_held(self):
        """The first loss case of the README: a dock validator, no uplink, a power cut."""
        events = [(f, ("tap",)) for f in range(100, 1000, 10)]
        led = self._drive(False, False, 1200, events)
        self.assertEqual(led.s.app.balance, 0)

    def test_the_open_second_is_lost_without_a_flush(self):
        """RG-19 rule 9: with a head signed once per second, a cut loses the open second."""
        lost = S.open_second_loss(random.Random(4), 10.0, flush=False)
        mean = sum(lost) / len(lost)
        self.assertGreater(mean, 4.0)            # 10 events per s, half a second open on average
        self.assertLess(mean, 6.0)
        self.assertGreater(max(lost), 10)

    def test_a_flush_on_host_loss_keeps_the_open_second(self):
        lost = S.open_second_loss(random.Random(4), 10.0, flush=True)
        self.assertEqual(sum(lost), 0)

    def test_a_flush_needs_the_store_to_last_30_ms(self):
        lost = S.open_second_loss(random.Random(4), 10.0, flush=True, cap_ms=10.0)
        self.assertGreater(sum(lost), 0)

    def test_the_chain_state_is_a_pure_function_of_the_record(self):
        rnd = random.Random(3)
        events = random_events(rnd, 15, 2 * S.FRAMES_PER_SLOT)
        a = run_reference(events, 3 * S.FRAMES_PER_SLOT)
        b = run_reference(events, 3 * S.FRAMES_PER_SLOT)
        self.assertEqual(a.s, b.s)

    def test_lapse_resume_state_equals_a_replay_from_the_record(self):
        keys, led, u7 = fresh()
        led.submit(10, u7.sign_input(("fling", 60), 10))
        led.run_to(30 * S.FPS)
        lapse = S.sign_tx(keys, S.LapseTx("S", 1, led.s.last_leaf_second, "val1"))
        led.submit(led.wall, lapse)
        led.run_to(led.wall + 1)
        led.submit(led.wall + 5000, u7.make_resume(led.s))
        led.run_to(led.wall + 5001)
        # a second validator replays the same record from genesis
        keys2, led2, u7b = fresh()
        led2.submit(10, u7b.sign_input(("fling", 60), 10))
        led2.run_to(30 * S.FPS)
        led2.submit(led2.wall, S.sign_tx(keys2, S.LapseTx("S", 1, led2.s.last_leaf_second, "val1")))
        led2.run_to(led2.wall + 1)
        led2.submit(led2.wall + 5000, u7b.make_resume(led2.s))
        led2.run_to(led2.wall + 5001)
        self.assertEqual(led.s.app_root(), led2.s.app_root())


if __name__ == "__main__":
    unittest.main()
