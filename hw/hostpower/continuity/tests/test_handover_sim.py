"""Tests of the host A to host B timelines and of the dock pair analysis."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import powersm as P  # noqa: E402
import handover_sim as H  # noqa: E402
import dockpair as D  # noqa: E402

S1, S2, S3 = H.SCENARIOS


def cell(tier, sc, gap=None, n=800):
    return H.run_cell(tier, sc, sc.gap_s if gap is None else gap, n=n)


class Outcomes(unittest.TestCase):
    def test_a_short_gap_is_seamless_in_every_tier(self):
        for t in (P.BARE0, P.BARE, P.BUFFER, P.FULL):
            c = cell(t, S3)
            self.assertEqual(c["outcome"], "LIVE", t.name)
            self.assertEqual(c["t_live_p50"], 0.0)

    def test_the_two_docks_scenario_is_inside_the_bare_ride_through(self):
        self.assertLess(S3.gap_s, P.tier_times(P.BARE)["live_s"])

    def test_bare_fails_the_walk_to_the_vehicle_on_the_capacitor(self):
        self.assertGreater(S1.gap_s, P.tier_times(P.BARE)["live_s"])
        c = cell(P.BARE0, S1)
        self.assertEqual(c["outcome"], "RESUME_CLEAN")

    def test_bare_with_the_b_cell_holds_the_walk_with_a_dark_face(self):
        c = cell(P.BARE, S1)
        self.assertEqual(c["outcome"], "HOLD")
        self.assertGreater(c["dark_before_s"], 60)
        self.assertLess(c["t_live_p99"], 1000.0)

    def test_a_smaller_bare_store_goes_dark_in_the_dock_move(self):
        """The power-path team finds 5 J does not fit. A 1.2 J store cannot span 1.5 s."""
        c = cell(P.BARE_S, S3)
        self.assertEqual(c["outcome"], "HOLD")
        self.assertGreater(c["dark_before_s"], 0.5)
        self.assertLess(c["t_live_p99"], 400.0)

    def test_buffer_and_full_never_go_dark_on_the_walk(self):
        for t in (P.BUFFER, P.FULL):
            c = cell(t, S1)
            self.assertEqual(c["outcome"], "LIVE")
            self.assertEqual(c["dark_before_s"], 0.0)

    def test_the_cold_restart_shows_the_safe_screen_at_host_pass_plus_23_ms(self):
        c = cell(P.BARE0, S1)
        # the host handshake of S1 is a PD contract, about 350 ms, plus the 23 ms of bootsm
        self.assertGreater(c["t_pixel_p50"], 300.0)
        self.assertLess(c["t_pixel_p50"], 450.0)

    def test_the_cold_modem_decides_the_restart_time(self):
        cold = H.run_cell(P.BARE0, H.Scen("c", "C", 3600, "qi", "cell", "cell_cold", 600.0, False, 1.0), 3600, n=500)
        warm = H.run_cell(P.BARE0, H.Scen("w", "W", 3600, "qi", "cell", "cell_warm", 600.0, False, 1.0), 3600, n=500)
        wifi = H.run_cell(P.BARE0, H.Scen("f", "F", 3600, "dock", "room", "wifi", 2000.0, False, 1.0), 3600, n=500)
        self.assertGreater(cold["t_live_p50"], 2000.0)
        self.assertLess(warm["t_live_p50"], 700.0)
        self.assertLess(wifi["t_live_p50"], 400.0)

    def test_the_restart_loses_no_state_only_live_frames(self):
        c = cell(P.BARE0, S1)
        self.assertGreater(c["frames_p50"], 100)        # frames shown not live
        self.assertGreater(c["share"]["RESUME_CLEAN"], 0.8)
        self.assertEqual(c["unseen"], 0 if c["outcome"] == "RESUME_CLEAN" and c["share"].get("RESUME_LAPSE", 0) == 0 else c["unseen"])

    def test_a_hold_has_almost_no_stale_frames(self):
        c = cell(P.BARE, S2)
        self.assertLessEqual(c["frames_p99"], 3)

    def test_long_gaps_end_in_a_stated_refusal(self):
        g = cell(P.FULL, S1, gap=2 * 86400.0)
        self.assertEqual(g["outcome"], "STATED_GRANT")
        a = cell(P.FULL, S1, gap=30 * 86400.0)
        self.assertEqual(a["outcome"], "STATED_ANCHOR")

    def test_a_missing_link_at_the_pause_makes_a_lapse_resume(self):
        sc = H.Scen("x", "X", 3600, "qi", "cell", "cell_cold", 600.0, False, 0.0)
        c = H.run_cell(P.BARE, sc, 3600, n=300)
        self.assertEqual(c["outcome"], "RESUME_LAPSE")
        self.assertEqual(c["unseen"], 240)

    def test_the_outcome_never_improves_as_the_gap_grows(self):
        rank = {"LIVE": 0, "HOLD": 1, "RESUME_CLEAN": 2, "RESUME_LAPSE": 2,
                "STATED_GRANT": 3, "STATED_ANCHOR": 4}
        for t in (P.BARE0, P.BARE, P.BUFFER, P.FULL):
            last = 0
            for g in H.GAPS:
                o = H.run_cell(t, S1, g, n=200)["outcome"]
                self.assertGreaterEqual(rank[o], last, (t.name, g, o))
                last = rank[o]

    def test_the_run_is_deterministic(self):
        a = H.run_cell(P.BARE0, S1, 75.0, n=300)
        b = H.run_cell(P.BARE0, S1, 75.0, n=300)
        self.assertEqual(a, b)

    def test_the_host_handshake_is_the_largest_term_of_a_hold(self):
        c = cell(P.BARE, S1)
        self.assertGreater(c["t_pixel_p50"], 0.8 * H.HOST_AUTH_MS["pd"])

    def test_the_planned_share_comes_from_net_discovery(self):
        self.assertGreater(H.P_PLANNED, 0.8)
        self.assertLess(H.P_PLANNED, 1.0 + 1e-9)
        self.assertGreater(H.FAILOVER_FRAMES_A, H.FAILOVER_FRAMES_C)


class Condition4(unittest.TestCase):
    def test_the_inequality_per_tier(self):
        rows = {r["tier"]: r for r in H.cond4_rows()}
        # BRIEF Section 5: E_buffer >= P_peak x t_handover
        self.assertLess(rows["Bare"]["t_peak_s"], 1.0)
        self.assertGreater(rows["Buffer"]["t_peak_s"], 300.0)
        self.assertGreater(rows["Full"]["t_peak_s"], 30 * 60.0)

    def test_bare_cannot_cover_the_two_docks_move_at_the_peak(self):
        self.assertLess(P.tier_times(P.BARE)["peak_s"], S3.gap_s)

    def test_buffer_range_matches_the_brief(self):
        lo = P.tier_times(P.BUFFER_LO)["peak_s"]
        hi = P.tier_times(P.BUFFER_HI)["peak_s"]
        self.assertLess(lo, hi)
        self.assertGreater(lo, 100.0)


class DockPair(unittest.TestCase):
    def test_the_pack_carries_a_validator_dock_for_half_an_hour(self):
        m = D.pack_minutes(True)
        self.assertGreater(m, 15)
        self.assertLess(m, 60)

    def test_a_plain_dock_lasts_longer_than_the_pair(self):
        self.assertGreater(D.pack_minutes(False), 3 * D.pack_minutes(True))

    def test_the_pair_makes_the_joint_loss_more_frequent(self):
        jr = D.joint_rates()
        self.assertGreater(jr["ratio"], 10.0)

    def test_the_shadow_takeover_is_a_few_frames(self):
        rows, fo = D.cases()
        self.assertLessEqual(fo["warm99"], 9)
        self.assertLess(fo["cold99"], 1000.0)

    def test_one_case_is_a_stated_loss(self):
        rows, fo = D.cases()
        losses = [r for r in rows if r["verdict"].startswith("LOSS")]
        self.assertEqual(len(losses), 1)
        self.assertIn("F2", losses[0]["case"])

    def test_every_other_case_holds(self):
        rows, fo = D.cases()
        for r in rows:
            if not r["verdict"].startswith("LOSS"):
                self.assertTrue(r["verdict"].startswith("holds"), r)


if __name__ == "__main__":
    unittest.main()
