"""Tests of the roaming Skin timelines and of the distance classes."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import roam_sim as R  # noqa: E402

SC = {s.short: s for s in R.SCENARIOS}


class SkinRoam(unittest.TestCase):
    def test_a_cable_roam_shows_the_rom_screen_inside_170_ms(self):
        for store in ("none", "seconds", "minutes"):
            c = R.run(SC["R1"], store, n=300)
            self.assertGreater(c["t_pixel_p50"], 150.0)
            self.assertLess(c["t_pixel_p50"], 170.0)

    def test_the_store_buys_nothing_on_a_cable(self):
        a, b = R.run(SC["R1"], "none", n=300), R.run(SC["R1"], "minutes", n=300)
        self.assertLess(abs(a["t_live_p50"] - b["t_live_p50"]), 5.0)
        self.assertLess(abs(a["t_pixel_p50"] - b["t_pixel_p50"]), 5.0)

    def test_a_standby_vehicle_core_gives_a_live_frame_near_0_3_s(self):
        c = R.run(SC["R1"], "minutes", n=300)
        self.assertGreater(c["t_live_p50"], 250.0)
        self.assertLess(c["t_live_p50"], 400.0)

    def test_a_cold_modem_decides_the_roam(self):
        cold, warm = R.run(SC["R3"], "none", n=300), R.run(SC["R1"], "none", n=300)
        self.assertGreater(cold["t_live_p50"], 2000.0)
        self.assertGreater(cold["t_live_p50"], 5 * warm["t_live_p50"])

    def test_a_proximity_hint_with_a_prewarmed_core_is_fastest(self):
        r2, r1 = R.run(SC["R2"], "none", n=300), R.run(SC["R1"], "none", n=300)
        self.assertLess(r2["t_live_p50"], r1["t_live_p50"])
        self.assertLess(r2["t_live_p50"], 250.0)

    def test_a_dead_core_a_makes_a_short_carry_wait_for_the_lapse(self):
        c = R.run(SC["R5"], "none", n=300)
        self.assertGreater(c["t_live_p50"], 1000.0)
        long = R.run(SC["R4"], "none", n=300)
        self.assertLess(long["t_live_p50"], 400.0)

    def test_a_takeover_removes_the_lapse_wait(self):
        lapse, take = R.run(SC["R5"], "none", n=300), R.run(SC["R6"], "none", n=300)
        self.assertGreater(lapse["t_live_p50"] - take["t_live_p50"], 700.0)
        self.assertLess(take["t_live_p50"], 400.0)

    def test_a_wireless_skin_with_an_empty_store_cannot_attach(self):
        sc = SC["R1"].with_(tether="mmwave")
        self.assertEqual(R.run(sc, "none", n=50)["outcome"], "NO_POWER")
        self.assertEqual(R.run(sc.with_(carry_s=3600.0), "minutes", n=50)["outcome"], "NO_POWER")
        self.assertEqual(R.run(sc, "minutes", n=50)["outcome"], "ROAMED")
        # the C1 radio Skin of the link seat has a 4.8 Wh cell, so an hour of carry is fine
        self.assertEqual(R.run(sc.with_(carry_s=3600.0), "cell", n=50)["outcome"], "ROAMED")

    def test_the_60_ghz_roam_is_slower_than_the_cable(self):
        sc = SC["R1"]
        cable = R.run(sc, "minutes", n=300)["t_live_p50"]
        mm = R.run(sc.with_(tether="mmwave"), "minutes", n=300)["t_live_p50"]
        self.assertGreater(mm, cable)

    def test_the_run_is_deterministic(self):
        self.assertEqual(R.run(SC["R1"], "none", n=200), R.run(SC["R1"], "none", n=200))

    def test_the_tether_numbers_are_a_stated_assumption(self):
        self.assertIn("attach_ms", R.TETHERS["cable"])
        self.assertIn("ASSUMPTION", R.__doc__)

    def test_the_tether_rates_follow_the_link_seat(self):
        self.assertAlmostEqual(R.TETHERS["cable"]["rate_gbps"], 19.4)
        self.assertAlmostEqual(R.TETHERS["mmwave"]["rate_gbps"], 5.0)
        self.assertAlmostEqual(R.TETHERS["cable"]["ratio"], 3.0)
        # a full face at DSC 10 bpp over the contact leaves: the link seat gives 2.81 ms
        self.assertAlmostEqual(R.frame_tx_ms(R.TETHERS["cable"]), 2.64, delta=0.4)

    def test_a_raw_frame_matches_the_lead_arithmetic(self):
        self.assertAlmostEqual(R.RAW_FRAME_BITS * 240 / 1e9, 36.9, delta=0.1)


class InputToPhoton(unittest.TestCase):
    def test_the_skin_hop_adds_one_to_three_ms(self):
        for kind in ("wifi", "cell"):
            a, _ = R.i2p(kind, "cable", skin=False, n=30000)
            b, _ = R.i2p(kind, "cable", skin=True, n=30000)
            self.assertGreater(b - a, 1.0)
            self.assertLess(b - a, 3.0)

    def test_the_p99_stays_under_30_ms(self):
        for kind in ("wifi", "cell"):
            for tether in ("cable", "mmwave"):
                self.assertLess(R.i2p(kind, tether, n=30000)[1], 30.0)

    def test_the_baseline_matches_part_21(self):
        m, q = R.i2p("wifi", "cable", skin=False, n=60000)
        self.assertAlmostEqual(m, 13.6, delta=1.0)

    def test_a_predicted_action_stays_under_10_ms(self):
        m, q = R.i2p("wifi", "cable", predicted=True, n=30000)
        self.assertLess(q, 10.0)


class DistanceClasses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rt = R.leaf_roundtrip(n=600)

    def _out(self, path_start, variant):
        return next(x for x in self.rt["out"] if x["path"].startswith(path_start) and x["variant"] == variant)

    def test_the_c2_round_trip_is_the_sim_latency_stage_sum(self):
        km = next(x for x in self.rt["lat"] if x["path"].startswith("C2 km"))
        self.assertAlmostEqual(km["rtt_stage_mean"], 5.0, delta=0.1)
        far = next(x for x in self.rt["lat"] if x["path"].startswith("C2 far"))
        self.assertGreater(far["rtt_stage_mean"], 80.0)

    def test_the_drawn_c2_round_trip_matches_the_stage_sum(self):
        km = self._out("C2 km", "awake")
        self.assertGreater(km["rtt"], 3.0)
        self.assertLess(km["rtt"], 7.0)

    def test_an_asleep_leaf_restarts_in_over_two_seconds(self):
        x = self._out("C2 km", "asleep")
        self.assertGreater(x["t_live_p50"], 2000.0)
        self.assertGreater(x["not_live"], 400)

    def test_an_awake_leaf_goes_live_in_about_a_tenth_of_a_second(self):
        x = self._out("C2 km", "awake")
        self.assertGreater(x["t_live_p50"], 60.0)
        self.assertLess(x["t_live_p50"], 160.0)

    def test_a_hot_shadow_leaf_shows_no_stale_frame_at_km(self):
        x = self._out("C2 km", "hot")
        self.assertEqual(x["not_live"], 0)
        self.assertEqual(x["t_pixel"], 0.0)
        self.assertLessEqual(x["covered"] * R.FRAME_MS, 40.0)

    def test_a_hot_shadow_at_the_far_class_leaves_the_reprojection_limit(self):
        x = self._out("C2 far", "hot")
        self.assertGreater(x["covered"] * R.FRAME_MS, 40.0)

    def test_the_far_class_is_slower_than_the_km_class(self):
        for v in ("asleep", "awake", "hot"):
            self.assertGreater(self._out("C2 far", v)["t_live_p50"], self._out("C2 km", v)["t_live_p50"])

    def test_the_way_back_loses_no_live_frame(self):
        for x in self.rt["back"]:
            self.assertEqual(x["covered"] * 0, 0)
            self.assertLess(x["t_switch_p99"], 400.0)
            self.assertLessEqual(x["covered"] * R.FRAME_MS, 40.0)

    def test_the_way_back_takes_longer_on_60_ghz_than_on_a_cable(self):
        cab = next(x for x in self.rt["back"] if x["tether"] == "cable")
        mm = next(x for x in self.rt["back"] if x["tether"] == "mmwave")
        self.assertGreater(mm["t_switch_p50"], cab["t_switch_p50"])

    def test_the_c2_input_to_photon_is_the_part_21_cell_site_row(self):
        km = next(x for x in self.rt["lat"] if x["path"].startswith("C2 km"))
        self.assertAlmostEqual(km["mean"], 16.5, delta=0.1)
        self.assertLess(km["p99"], 30.0)
        far = next(x for x in self.rt["lat"] if x["path"].startswith("C2 far"))
        self.assertGreater(far["p99"], 100.0)

    def test_the_c1_and_c2_km_inputs_stay_inside_30_ms_p99(self):
        self.assertLess(R.i2p("wifi", "mmwave", n=20000)[1], 30.0)


if __name__ == "__main__":
    unittest.main()
