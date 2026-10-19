"""Tests of the Core as a single point, the joint failure model and the link loss."""
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import corefail as C  # noqa: E402


class Load(unittest.TestCase):
    def test_one_skin_is_the_leaf_delta_row(self):
        self.assertAlmostEqual(C.core_power_w(1), C.P.W["live"], delta=0.05)

    def test_power_rises_with_n_and_extend_costs_more_than_mirror(self):
        for n in range(2, 7):
            self.assertGreater(C.core_power_w(n), C.core_power_w(n - 1))
            self.assertGreater(C.core_power_w(n, "extend"), C.core_power_w(n, "mirror"))

    def test_three_skins_share_a_store_in_under_half_the_time(self):
        one, _ = C.core_bridge_s(1, 0.9)
        three, _ = C.core_bridge_s(3, 0.9)
        self.assertLess(three, 0.6 * one)

    def test_the_b_cell_hold_does_not_depend_on_n(self):
        self.assertEqual(C.core_bridge_s(1, 0.9)[1], C.core_bridge_s(6, 0.9)[1])


class Joint(unittest.TestCase):
    def test_the_closed_form_matches_the_simulation(self):
        saved = dict(C.RATES)
        for n, design in ((2, "split"), (2, "leafs"), (3, "split")):
            try:
                for k in ("core_box", "skin_panel", "cable_link"):
                    C.RATES[k] = (saved[k][0] * 1500, saved[k][1])
                cf = C.unavailability(n, design, beta=0.0)["all_dark"]
            finally:
                C.RATES.update(saved)
            sim = C.simulate_all_dark(n, design, scale=1500, hours=1.0e5)
            self.assertAlmostEqual(sim / cf, 1.0, delta=0.15, msg=(n, design))

    def test_one_core_has_more_all_dark_time_than_n_leafs(self):
        for n in (2, 3, 4):
            self.assertGreater(C.unavailability(n, "split")["all_dark"],
                               C.unavailability(n, "leafs")["all_dark"])

    def test_the_dark_screen_minutes_are_nearly_equal(self):
        a, b = C.unavailability(3, "split"), C.unavailability(3, "leafs")
        self.assertAlmostEqual(a["mean_dark_screens"] / b["mean_dark_screens"], 1.0, delta=0.05)

    def test_n_equals_one_is_the_same_for_both(self):
        a, b = C.unavailability(1, "split"), C.unavailability(1, "leafs")
        self.assertAlmostEqual(a["all_dark"] / b["all_dark"], 1.0, delta=0.05)

    def test_a_common_cause_raises_the_leaf_floor(self):
        self.assertGreater(C.unavailability(3, "leafs", beta=0.05)["all_dark"],
                           C.unavailability(3, "leafs", beta=0.0)["all_dark"])

    def test_the_split_all_dark_time_does_not_fall_with_n(self):
        a, b = C.unavailability(2, "split")["all_dark"], C.unavailability(6, "split")["all_dark"]
        self.assertGreaterEqual(a, b * 0.999)
        self.assertGreater(b, 0.9 * C.u_of(*C.RATES["core_box"]))

    def test_the_60_ghz_link_makes_the_split_worse_in_dark_screens(self):
        cab = C.unavailability(3, "split", "cable")["mean_dark_screens"]
        mm = C.unavailability(3, "split", "mmwave")["mean_dark_screens"]
        self.assertGreater(mm, 5 * cab)

    def test_events_per_year_favour_the_split_for_core_failures(self):
        # one Core event darkens all Skins, so the Split has fewer events than N Leafs
        self.assertGreater(C.unavailability(6, "leafs")["events_per_h"],
                           C.unavailability(6, "split")["events_per_h"])

    def test_a_longer_gap_is_less_likely(self):
        self.assertGreater(C.gap_exceeds(60), C.gap_exceeds(600))
        self.assertGreater(C.gap_exceeds(600), C.gap_exceeds(6000))


class Cases(unittest.TestCase):
    def test_a_skin_link_loss_costs_one_screen_only(self):
        rows, fo = C.case_table(3)
        c2 = next(x for x in rows if x["case"].startswith("C2"))
        self.assertIn("other Skins", c2["cost"])
        self.assertEqual(c2["state"].split(";")[0], "none")

    def test_the_box_death_row_names_the_unfinalized_bound(self):
        rows, fo = C.case_table(3)
        c3 = next(x for x in rows if x["case"].startswith("C3"))
        self.assertIn("7 s", c3["state"])

    def test_the_validator_failure_is_a_few_frames(self):
        rows, fo = C.case_table(3)
        self.assertLessEqual(fo["w99"], 9)


class LinkLoss(unittest.TestCase):
    def setUp(self):
        self.r = random.Random(2)

    def test_a_cable_glitch_shows_the_rom_screen_on_any_store(self):
        for store in ("none", "seconds", "minutes"):
            x = C.link_loss(self.r, "cable", store, 10.0, "glitch")
            self.assertEqual(x["shows"], "the ROM screen")

    def test_a_pulled_cable_with_no_store_is_black(self):
        x = C.link_loss(self.r, "cable", "none", 10.0, "unplug")
        self.assertEqual(x["shows"], "black")
        self.assertIsNone(x["rom_ms"])

    def test_a_pulled_cable_with_a_store_shows_the_rom_screen(self):
        self.assertEqual(C.link_loss(self.r, "cable", "seconds", 10.0, "unplug")["shows"], "the ROM screen")
        self.assertEqual(C.link_loss(self.r, "cable", "minutes", 900.0, "unplug")["shows"],
                         "the ROM screen, then black")

    def test_the_rom_screen_is_up_in_about_15_ms(self):
        x = C.link_loss(self.r, "cable", "minutes", 1.0, "glitch")
        self.assertAlmostEqual(x["rom_ms"], 14.8, delta=0.5)

    def test_a_skin_never_shows_a_stale_frame(self):
        for tether in ("cable", "mmwave"):
            for store in ("none", "seconds", "minutes"):
                for kind in ("glitch", "unplug"):
                    if tether == "mmwave" and kind == "unplug":
                        continue
                    self.assertFalse(C.link_loss(self.r, tether, store, 5.0, kind)["stale_frame_shown"])

    def test_the_return_after_a_glitch_is_under_a_quarter_second(self):
        for tether in ("cable", "mmwave"):
            self.assertLess(C.link_loss(self.r, tether, "minutes", 1.0, "glitch")["back_ms"], 250.0)

    def test_an_unplug_costs_the_attach_time(self):
        a = C.link_loss(self.r, "cable", "none", 5.0, "unplug")["back_ms"]
        b = C.link_loss(self.r, "cable", "none", 5.0, "glitch")["back_ms"]
        self.assertGreater(a, b)

    def test_the_missed_frames_follow_the_outage(self):
        self.assertEqual(C.link_loss(self.r, "cable", "none", 2.0, "glitch")["missed_frames"], 480)


class Distance(unittest.TestCase):
    def test_c2_km_failover_is_inside_the_reprojection_limit(self):
        x = next(s for s in C.spof_by_class() if s["path"].startswith("C2 km"))
        self.assertLessEqual(x["warm99"] * C.R.FRAME_MS, 40.0)

    def test_c2_far_failover_is_outside_it(self):
        x = next(s for s in C.spof_by_class() if s["path"].startswith("C2 far"))
        self.assertGreater(x["warm50"] * C.R.FRAME_MS, 40.0)

    def test_a_cold_start_is_slower_far_than_at_km(self):
        rows = {s["path"][:6]: s for s in C.spof_by_class()}
        self.assertGreater(rows["C2 far"]["cold50"], rows["C2 km,"]["cold50"] * 2)

    def test_more_replicas_never_hurt(self):
        for lam in C.FLEETS.values():
            vals = [C.validator_unavailability(k, lam) for k in (1, 2, 3, 4)]
            self.assertEqual(vals, sorted(vals, reverse=True))

    def test_a_common_cause_sets_a_floor_under_the_replicas(self):
        lam = C.FLEETS["stress fleet of net/discovery"]
        u = C.u_of(lam, C.FLEET["crash_down_s"])
        self.assertGreater(C.validator_unavailability(4, lam), 0.9 * C.BETA * u)
        self.assertLess(C.validator_unavailability(2, lam), C.validator_unavailability(1, lam) / 10)

    def test_the_blast_radius_is_stated(self):
        self.assertGreaterEqual(C.N_USERS_PER_CORE, 10)


if __name__ == "__main__":
    unittest.main()
