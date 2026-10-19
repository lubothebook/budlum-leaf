"""Tests of the host-power states, their laws and their energy times."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import powersm as P  # noqa: E402


def lost(tier, link_up=True):
    sm = P.PowerSM.hosted(tier, link_up=link_up)
    sm.on("HOST_LOST")
    return sm


class Tables(unittest.TestCase):
    def test_every_state_is_described(self):
        for s in P.ALL_STATES:
            info = P.STATE_INFO[s]
            for k in ("entry", "alive", "face", "rear", "source"):
                self.assertTrue(info[k], (s, k))

    def test_the_new_states_sit_beside_bootsm(self):
        for s in ("HOST", "BRIDGE", "ISLAND", "SUSPENDED", "RESUMING"):
            self.assertIn(s, P.ALL_STATES)
        self.assertEqual(P.bootsm.boot().final, "SESSION")

    def test_bootsm_times_are_read_not_copied(self):
        b = P.boot_times("both")
        r = P.bootsm.boot()
        self.assertAlmostEqual(b["t_safe"], r.t_safe)
        self.assertAlmostEqual(b["t_session"], r.t_session)
        self.assertLessEqual(b["t_safe"], 60.0)

    def test_a_cold_modem_costs_two_seconds(self):
        cold = P.boot_times("cell_cold")
        warm = P.boot_times("cell_warm")
        self.assertGreater(cold["t_link"], 1900)
        self.assertLess(warm["t_link"], 150)

    def test_the_rear_glance_beats_the_face(self):
        b = P.boot_times("both")
        self.assertLessEqual(b["t_rear"], b["t_safe"])

    def test_tier_times_match_the_energy_numbers(self):
        bare = P.tier_times(P.BARE)
        self.assertAlmostEqual(bare["live_s"], 5.0 / P.W["live"], places=1)
        self.assertAlmostEqual(bare["hold_s"], (P.BARE.b_j - P.B_FLOOR_J) / P.W["hold"], delta=1.0)
        self.assertLess(P.tier_times(P.BARE)["peak_s"], 1.0)

    def test_brief_condition_4_for_the_buffer_range(self):
        # E_buffer >= P_peak x t_handover, with the 0.3 to 1.5 Wh of the BRIEF
        lo = P.tier_times(P.BUFFER_LO)["peak_s"]
        hi = P.tier_times(P.BUFFER_HI)["peak_s"]
        self.assertAlmostEqual(lo, 0.3 * 3600 * 0.96 / 8.7, delta=8.0)
        self.assertAlmostEqual(hi, 1.5 * 3600 * 0.96 / 8.7, delta=8.0)

    def test_bare0_has_no_hold_phase(self):
        self.assertEqual(P.tier_times(P.BARE0)["hold_s"], 0.0)

    def test_the_pause_costs_far_less_than_its_reserve(self):
        need = 0.025 * 0.3 + 0.005 * 1.5 + 0.020 * 0.1     # sign, send, commit
        self.assertLess(need * 10, P.E_PAUSE_J)

    def test_the_transition_table_names_only_known_states(self):
        for src, ev, dst, note in P.TRANSITIONS:
            self.assertIn(src, P.ALL_STATES)
            for d in dst.replace(" or ", ",").split(","):
                d = d.strip()
                self.assertTrue(d in P.ALL_STATES or d == "the previous state", d)


class BridgeAndHost(unittest.TestCase):
    def test_host_lost_goes_to_bridge_with_a_live_session(self):
        sm = lost(P.BUFFER)
        self.assertEqual(sm.state, "BRIDGE")
        self.assertEqual(sm.session, "LIVE")
        self.assertEqual(P.check_laws(sm), [])

    def test_a_short_gap_never_stops_the_session(self):
        sm = lost(P.BUFFER)
        sm.advance(300)
        sm.on("HOST_SEEN")
        self.assertEqual(sm.state, "HOST_AUTH")
        self.assertEqual(sm.session, "LIVE")
        sm.on("HANDSHAKE_PASS")
        self.assertEqual(sm.state, "HOST")
        self.assertEqual(sm.session, "LIVE")
        self.assertEqual([x for x in sm.log if "PAUSING" in str(x)], [])

    def test_host_pads_stay_dead_until_the_pass(self):
        sm = lost(P.BUFFER)
        sm.on("HOST_SEEN")
        self.assertFalse(sm.host_pad_live)
        sm.on("HANDSHAKE_PASS")
        self.assertTrue(sm.host_pad_live)

    def test_a_refused_host_changes_nothing_and_is_counted(self):
        sm = lost(P.BUFFER)
        e = sm.e_body
        sm.on("HOST_SEEN")
        sm.on("HANDSHAKE_FAIL")
        self.assertEqual(sm.state, "BRIDGE")
        self.assertFalse(sm.host_pad_live)
        self.assertEqual(sm.refused_hosts, 1)
        self.assertLessEqual(sm.e_body, e)

    def test_the_host_never_holds_authority(self):
        sm = lost(P.FULL)
        for ev in ("HOST_SEEN", "HANDSHAKE_PASS", "HOST_LOST"):
            sm.on(ev)
            self.assertEqual(sm.authority_holder, "U7")

    def test_the_host_refills_the_store(self):
        sm = lost(P.BUFFER)
        sm.advance(600)
        low = sm.e_body
        sm.on("HOST_SEEN")
        sm.on("HANDSHAKE_PASS")
        sm.advance(300)
        self.assertGreater(sm.e_body, low)
        self.assertLessEqual(sm.e_body, P.BUFFER.body_j + 1e-6)

    def test_bridge_changes_from_live_to_hold_for_bare(self):
        sm = lost(P.BARE)
        sm.advance(5)
        self.assertEqual(sm.state, "BRIDGE")
        w, src = sm.drain()
        self.assertEqual(src, "bcell")
        self.assertAlmostEqual(w, P.W["hold"])

    def test_make_before_break_with_a_late_host(self):
        sm = lost(P.BARE)
        sm.advance(900)                      # still on the B cell
        sm.on("HOST_SEEN")
        sm.advance(0.3)
        sm.on("HANDSHAKE_PASS")
        self.assertEqual(sm.state, "HOST")
        self.assertEqual(sm.session, "LIVE")


class PauseAndResume(unittest.TestCase):
    def test_the_store_at_its_floor_pauses_cleanly(self):
        sm = lost(P.BARE)
        sm.advance(2000)
        self.assertEqual(sm.state, "SUSPENDED")
        self.assertEqual(sm.session, "PAUSED")

    def test_no_link_means_a_lapse_pause(self):
        sm = lost(P.BARE, link_up=False)
        sm.advance(2000)
        self.assertEqual(sm.session, "PAUSED_LAPSE")
        self.assertEqual(sm.state, "SUSPENDED")

    def test_bare0_pauses_from_the_capacitor_and_goes_dark(self):
        sm = lost(P.BARE0)
        sm.advance(10)
        self.assertEqual(sm.state, "DEAD")
        self.assertEqual(sm.session, "PAUSED")
        self.assertEqual(P.check_laws(sm), [])

    def test_resume_from_suspended_runs_the_boot_path(self):
        sm = lost(P.BARE)
        sm.advance(2000)
        sm.on("HOST_SEEN")
        sm.on("HANDSHAKE_PASS")
        self.assertEqual(sm.state, "RESUMING")
        self.assertEqual(sm.session, "PAUSED")
        sm.on("RESUME_OK")
        self.assertEqual(sm.state, "HOST")
        self.assertEqual(sm.session, "LIVE")

    def test_resume_from_dead_works_too(self):
        sm = lost(P.BARE0)
        sm.advance(10)
        sm.on("HOST_SEEN")
        sm.on("HANDSHAKE_PASS")
        sm.on("RESUME_OK")
        self.assertEqual((sm.state, sm.session), ("HOST", "LIVE"))

    def test_a_refused_resume_is_stated_and_recoverable(self):
        sm = lost(P.BARE)
        sm.advance(2000)
        sm.on("HOST_SEEN")
        sm.on("HANDSHAKE_PASS")
        sm.on("RESUME_REFUSED", reason="grant expired")
        self.assertEqual(sm.state, "RESUME_STATED")
        self.assertEqual(sm.session, "PAUSED")
        face, rear = sm.surface()
        self.assertNotEqual(face, "dark")
        sm.on("USER_REGRANT")
        self.assertEqual(sm.state, "RESUMING")

    def test_losing_the_host_in_resuming_keeps_the_pause(self):
        sm = lost(P.BARE)
        sm.advance(2000)
        sm.on("HOST_SEEN")
        sm.on("HANDSHAKE_PASS")
        sm.on("HOST_LOST")
        self.assertEqual(sm.state, "SUSPENDED")
        self.assertEqual(sm.session, "PAUSED")

    def test_a_touch_shows_the_rear_glance_and_costs_energy(self):
        sm = lost(P.BARE)
        sm.advance(2000)
        e = sm.e_b
        sm.on("TOUCH")
        self.assertEqual(sm.state, "SUSPENDED")
        self.assertAlmostEqual(e - sm.e_b, P.GLANCE_J)

    def test_the_b_cell_empties_into_dead_and_the_pause_stays(self):
        sm = lost(P.BARE)
        sm.advance(1.0e5)
        self.assertEqual(sm.state, "DEAD")
        self.assertEqual(sm.session, "PAUSED")

    def test_a_pause_while_a_host_handshake_runs_goes_back_to_the_handshake(self):
        sm = lost(P.BARE)
        sm.advance(960)
        sm.on("HOST_SEEN")
        sm.advance(60)                      # the store runs out while the host is checked
        self.assertEqual(sm.state, "HOST_AUTH")
        self.assertEqual(sm.session, "PAUSED")
        sm.on("HANDSHAKE_PASS")
        self.assertEqual(sm.state, "RESUMING")

    def test_a_flat_b_cell_pauses_into_dead(self):
        sm = P.PowerSM.hosted(P.BARE)
        sm.e_b = 0.0
        sm.on("HOST_LOST")
        sm.advance(10)
        self.assertEqual(sm.state, "DEAD")
        self.assertEqual(sm.session, "PAUSED")


class IslandTier(unittest.TestCase):
    def test_full_tier_moves_from_bridge_to_island(self):
        sm = lost(P.FULL)
        sm.advance(601)
        self.assertEqual(sm.state, "ISLAND")
        self.assertEqual(sm.session, "LIVE")

    def test_buffer_tier_never_becomes_an_island(self):
        sm = lost(P.BUFFER)
        sm.advance(601)
        self.assertEqual(sm.state, "BRIDGE")

    def test_island_steps_down_and_ends_in_a_pause(self):
        sm = lost(P.FULL)
        seen = set()
        for _ in range(400):
            sm.advance(60)
            seen.add(sm.drain()[0])
            if sm.state == "SUSPENDED":
                break
        self.assertEqual(sm.state, "SUSPENDED")
        self.assertEqual(sm.session, "PAUSED")
        self.assertGreaterEqual(len(seen), 3)

    def test_island_life_is_hours(self):
        pr = P.bridge_profile(P.FULL)
        self.assertGreater(pr["bridge_s"] / 3600, 4.0)

    def test_user_can_choose_the_island_on_full_only(self):
        sm = lost(P.FULL)
        self.assertTrue(sm.on("USER_ISLAND"))
        sm2 = lost(P.BUFFER)
        self.assertFalse(sm2.on("USER_ISLAND"))

    def test_a_host_found_on_an_island_resumes_nothing(self):
        sm = lost(P.FULL)
        sm.advance(3000)
        sm.on("HOST_SEEN")
        sm.on("HANDSHAKE_PASS")
        self.assertEqual((sm.state, sm.session), ("HOST", "LIVE"))


class Laws(unittest.TestCase):
    def test_the_laws_catch_a_live_pad_before_the_pass(self):
        sm = lost(P.BUFFER)
        sm.host_present, sm.host_pad_live, sm.host_pass = True, True, False
        self.assertTrue(any(x.startswith("P1") for x in P.check_laws(sm)))

    def test_the_laws_catch_a_host_with_authority(self):
        sm = lost(P.BUFFER)
        sm.authority_holder = "dock"
        self.assertTrue(any(x.startswith("P2") for x in P.check_laws(sm)))

    def test_the_laws_catch_a_session_in_two_places(self):
        sm = lost(P.BUFFER)
        sm.session = "PAUSED"
        self.assertTrue(any(x.startswith("P3") for x in P.check_laws(sm)))

    def test_fuzz_event_sequences_break_no_law(self):
        steps, viol = P.fuzz(n_seq=1500, n_ev=40, seed=7)
        self.assertGreater(steps, 30000)
        self.assertEqual(viol, [])

    def test_fuzz_with_another_seed(self):
        steps, viol = P.fuzz(n_seq=800, n_ev=60, seed=99)
        self.assertEqual(viol, [])

    def test_energy_never_goes_negative_over_a_day(self):
        for tier in (P.BARE0, P.BARE, P.BUFFER, P.FULL):
            sm = lost(tier)
            for _ in range(48):
                sm.advance(1800)
                self.assertGreaterEqual(sm.e_body, 0.0)
                self.assertGreaterEqual(sm.e_b, 0.0)
                self.assertEqual(P.check_laws(sm), [])

    def test_every_wake_shows_a_surface_inside_60_ms_of_the_pass(self):
        # RESUMING lists the safe screen at 23 ms of bootsm. The host pass comes first.
        self.assertLessEqual(P.boot_times("both")["t_safe"], 60.0)
        face, rear = P.STATE_INFO["RESUMING"]["face"], P.STATE_INFO["RESUMING"]["rear"]
        self.assertTrue(face and rear)


if __name__ == "__main__":
    unittest.main()
