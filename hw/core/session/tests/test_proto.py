"""Tests of the RG-19A drafts against the conventions of proto/VERSIONING.md."""
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import skinproto as SP  # noqa: E402

pl = SP.pl
BASE = pl.parse(SP.D.LEAF)
CONT = SP.D.merged_schema()
MERGED = SP.merged_schema()
LINK = SP.link_schema()
NEW_MSGS = ["ViewRef", "PairingRecord", "WriterGrant", "WriterTakeOver", "SkinLinkLost"]
NEW_ENUMS = ["ViewMode", "SkinClass", "CoreDistance", "SkinLinkKind"]


class Conventions(unittest.TestCase):
    def test_the_merge_only_adds(self):
        for m in CONT.messages:
            if m in ("LeafMessage", "SessionPause", "SessionResume"):
                continue
            self.assertEqual([(f.name, f.number) for f in CONT.messages[m]],
                             [(f.name, f.number) for f in MERGED.messages[m]], m)
        for m in ("SessionPause", "SessionResume"):
            old = {(f.name, f.number, f.type_name) for f in CONT.messages[m]}
            new = {(f.name, f.number, f.type_name) for f in MERGED.messages[m]}
            self.assertTrue(old <= new, m)

    def test_new_fields_have_numbers_above_15_and_are_free(self):
        for m in ("SessionPause", "SessionResume"):
            old = {f.number for f in CONT.messages[m]}
            added = [f for f in MERGED.messages[m] if f.number not in old]
            self.assertTrue(added)
            for f in added:
                self.assertGreater(f.number, 12 if m == "SessionResume" else 15)
            nums = [f.number for f in MERGED.messages[m]]
            self.assertEqual(len(nums), len(set(nums)))

    def test_new_names_exist_and_are_new(self):
        for m in NEW_MSGS:
            self.assertIn(m, MERGED.messages)
            self.assertNotIn(m, CONT.messages)
        for e in NEW_ENUMS:
            self.assertIn(e, MERGED.enums)
            self.assertNotIn(e, CONT.enums)

    def test_enum_zero_values_and_prefixes(self):
        for e in NEW_ENUMS:
            zero = [k for k, v in MERGED.enums[e].items() if v == 0]
            self.assertEqual(len(zero), 1)
            self.assertTrue(zero[0].endswith("_UNSPECIFIED"))
            prefix = re.sub(r"(?<!^)(?=[A-Z])", "_", e).upper() + "_"
            for k in MERGED.enums[e]:
                self.assertTrue(k.startswith(prefix), (e, k))

    def test_the_core_distance_values_are_c0_c1_c2(self):
        self.assertEqual({k: v for k, v in MERGED.enums["CoreDistance"].items() if v},
                         {"CORE_DISTANCE_C0": 1, "CORE_DISTANCE_C1": 2, "CORE_DISTANCE_C2": 3})

    def test_error_codes_do_not_collide(self):
        vals = list(MERGED.enums["ErrorCode"].values())
        self.assertEqual(len(vals), len(set(vals)))
        new = [v for v in vals if v not in CONT.enums["ErrorCode"].values()]
        self.assertEqual(sorted(new), [1100, 1101, 1102, 1103, 1104])

    def test_new_bodies_use_free_oneof_numbers(self):
        old = {f.number for f in CONT.messages["LeafMessage"]}
        new = sorted(f.number for f in MERGED.messages["LeafMessage"] if f.number not in old)
        self.assertEqual(new, [39, 40, 41])

    def test_the_pause_reason_gets_one_value(self):
        self.assertEqual(MERGED.enums["PauseReason"]["PAUSE_REASON_VIEWS_LOST"], 5)
        self.assertNotIn("PAUSE_REASON_VIEWS_LOST", CONT.enums["PauseReason"])

    def test_hardware_parsed_messages_are_untouched(self):
        for m in ("SliceHeader", "Slice", "FrameCommit", "InputBatch", "LayerUpdate"):
            self.assertEqual([(f.name, f.number) for f in BASE.messages[m]],
                             [(f.name, f.number) for f in MERGED.messages[m]], m)

    def test_the_skin_never_signs_on_the_link(self):
        for m, fields in LINK.messages.items():
            self.assertFalse(any(f.type_name == "Signature" for f in fields), m)
            self.assertFalse(any("sign" in f.name for f in fields), m)

    def test_every_link_message_has_a_tag_at_field_15(self):
        for m in ("SkinAttach", "SkinAttachAck", "ViewBind", "ViewUnbind", "SkinEvent"):
            self.assertEqual(LINK.messages[m][-1].name, "tag")
            self.assertEqual(LINK.messages[m][-1].number, 15)

    def test_the_link_package_is_separate(self):
        self.assertEqual(LINK.package, "budlum.skin.v1")
        self.assertEqual(MERGED.package, "budlum.leaf.v1")

    def test_the_link_enums_are_prefixed(self):
        for e, vals in LINK.enums.items():
            prefix = re.sub(r"(?<!^)(?=[A-Z])", "_", e).upper() + "_"
            self.assertTrue(all(k.startswith(prefix) for k in vals), e)
            self.assertIn(prefix + "UNSPECIFIED", vals)


class RoundTrip(unittest.TestCase):
    def test_every_message_round_trips_canonically(self):
        for name, n, ok in SP.sizes():
            self.assertTrue(ok, name)

    def test_a_skin_event_is_small(self):
        sizes = {n: b for n, b, _ in SP.sizes()}
        self.assertLess(sizes["SkinEvent (Skin link)"], 48)

    def test_the_pause_with_two_views_stays_under_3_kB(self):
        sizes = {n: b for n, b, _ in SP.sizes()}
        self.assertLess(sizes["session_pause"], 3100)

    def test_the_takeover_is_a_session_key_signature(self):
        sizes = {n: b for n, b, _ in SP.sizes()}
        self.assertLess(sizes["writer_take_over"], 2700)


if __name__ == "__main__":
    unittest.main()
