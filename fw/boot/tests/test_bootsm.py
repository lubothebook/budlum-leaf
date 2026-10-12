"""Tests of the boot state machine: the times and the never-a-brick law."""
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import bootsm as B  # noqa: E402


class Times(unittest.TestCase):
    def test_nominal_targets(self):
        r = B.boot()
        self.assertEqual(r.final, "SESSION")
        self.assertLessEqual(r.t_safe, 60.0)
        self.assertLessEqual(r.t_link, 150.0)
        self.assertLessEqual(r.t_session, 300.0)

    def test_step1_signature_inside_20ms(self):
        r = B.boot()
        t_verify = [t for t, s, _ in r.trace if s == "VERIFY"][0]
        self.assertLessEqual(t_verify, 20.0)

    def test_wifi_only_link_inside_150ms(self):
        r = B.boot(["U5_A", "U5_B"])
        self.assertEqual(r.final, "SESSION_STATED")
        self.assertLessEqual(r.t_link, 150.0)

    def test_cold_modem_alone_is_slow_and_says_so(self):
        r = B.boot(["U2A_A", "U2A_B", "U5_COLD"])
        self.assertGreater(r.t_link, 150.0)
        self.assertIn("U2A refused: firmware not attested, held off", r.lines)

    def test_u7_slot_b_still_inside_60ms(self):
        r = B.boot(["U7_A"])
        self.assertLessEqual(r.t_safe, 60.0)
        self.assertTrue(any("slot B" in x for x in r.lines))


class Outcomes(unittest.TestCase):
    def test_se_fault(self):
        r = B.boot(["U7_A", "U7_B"])
        self.assertEqual(r.final, "SE_FAULT")
        self.assertEqual(r.surface, "rear")
        self.assertFalse(r.wallet)
        self.assertEqual(r.powered, [])

    def test_seat_refused_rear_only(self):
        for f in ("PAD_B", "PAD_Q1"):
            r = B.boot([f])
            self.assertEqual(r.final, "REAR_ONLY")
            self.assertEqual(r.powered, [])

    def test_one_quadrant_refused(self):
        r = B.boot(["PAD_Q2"])
        self.assertEqual(r.powered, ["Q1", "Q3", "Q4"])
        self.assertEqual(r.final, "SESSION_STATED")

    def test_diagonal_reached_round_the_other_side(self):
        r = B.boot(["PAD_Q2", "PAD_Q3"])
        self.assertEqual(r.powered, ["Q1"])        # Q4 has no path left
        r = B.boot(["PAD_Q3"])
        self.assertIn("Q4", r.powered)

    def test_u1_dead_gives_led(self):
        r = B.boot(["U1_HW"])
        self.assertEqual(r.final, "LED_CODE")
        self.assertEqual(r.surface, "led")

    def test_decoder_both_slots(self):
        r = B.boot(["U6_A", "U6_B"])
        self.assertEqual(r.final, "RECOVERY")
        self.assertIn("U6", r.quarantined)

    def test_decoder_slot_a_falls_to_b(self):
        r = B.boot(["U6_A"])
        self.assertEqual(r.slot, "B")
        self.assertEqual(r.final, "SESSION_STATED")

    def test_noncritical_stays_on_a(self):
        r = B.boot(["U3_A"])
        self.assertEqual(r.slot, "A")
        self.assertEqual(r.quarantined, ["U3"])

    def test_trial_reverts_on_any_fault(self):
        r = B.boot(["U3_A"], trial=True)
        self.assertTrue(r.reverted)
        self.assertEqual(r.slot, "B")
        self.assertTrue(any("floors unchanged" in x for x in r.lines))

    def test_stated_refusals(self):
        self.assertEqual(B.boot(["ANCHOR"]).final, "ANCHOR_STATED")
        self.assertEqual(B.boot(["STREAM_KEY"]).final, "STREAM_REFUSED")
        self.assertEqual(B.boot(["REVOKED"]).final, "UPDATE_REQUIRED")

    def test_unknown_fault_rejected(self):
        with self.assertRaises(ValueError):
            B.boot(["NOPE"])


class Law(unittest.TestCase):
    def test_exhaustive_sweep(self):
        n, bad = B.sweep()
        self.assertEqual(n, 2 ** 16)
        self.assertEqual(bad, [])

    def test_random_sets_of_all_faults(self):
        rng = random.Random(21)
        for _ in range(20000):
            fs = [x for x in B.FAULTS if rng.random() < 0.15]
            for trial in (False, True):
                r = B.boot(fs, trial=trial)
                self.assertEqual(B.check_law(r, fs), [], (fs, trial))


class Budgets(unittest.TestCase):
    def test_boot_nor_fits_two_slots_in_16_MiB(self):
        b = B.budgets()
        self.assertLessEqual(b["boot_nor_two_slots_MiB"], 16.0)


if __name__ == "__main__":
    unittest.main()
