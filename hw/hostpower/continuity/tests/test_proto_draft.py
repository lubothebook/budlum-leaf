"""Tests of the RG-19 proto draft against the conventions of proto/VERSIONING.md.

The draft is merged into leaf.proto in memory. Nothing in proto/ is edited.
"""
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.dont_write_bytecode = True
import protodraft as D  # noqa: E402
import protolite as pl  # noqa: E402  read only, through protodraft's path

BASE = pl.parse(D.LEAF)
MERGED = D.merged_schema()
NEW_MSGS = ["PendingAction", "SessionPause", "SessionPauseAck", "LapseNotice",
            "SessionResume", "ResumeAck", "PowerNotice"]
NEW_ENUMS = ["PowerState", "PauseReason", "HostClass", "PendingKind", "ResumeSigner"]


class Conventions(unittest.TestCase):
    def test_the_merge_adds_only(self):
        for m in BASE.messages:
            self.assertIn(m, MERGED.messages)
            self.assertEqual([(f.name, f.number, f.type_name) for f in BASE.messages[m]
                              if m != "LeafMessage"],
                             [(f.name, f.number, f.type_name) for f in MERGED.messages[m]
                              if m != "LeafMessage"], m)
        for e in BASE.enums:
            for k, v in BASE.enums[e].items():
                self.assertEqual(MERGED.enums[e][k], v, (e, k))

    def test_new_names_exist(self):
        for m in NEW_MSGS:
            self.assertIn(m, MERGED.messages)
            self.assertNotIn(m, BASE.messages)
        for e in NEW_ENUMS:
            self.assertIn(e, MERGED.enums)
            self.assertNotIn(e, BASE.enums)

    def test_enum_zero_values_are_unspecified(self):
        for e in NEW_ENUMS:
            vals = MERGED.enums[e]
            zero = [k for k, v in vals.items() if v == 0]
            self.assertEqual(len(zero), 1)
            self.assertTrue(zero[0].endswith("_UNSPECIFIED"), e)

    def test_enum_values_are_prefixed_with_the_enum_name(self):
        for e in NEW_ENUMS:
            prefix = re.sub(r"(?<!^)(?=[A-Z])", "_", e).upper() + "_"
            for k in MERGED.enums[e]:
                self.assertTrue(k.startswith(prefix), (e, k))

    def test_error_codes_do_not_collide(self):
        base = set(BASE.enums["ErrorCode"].values())
        new = {k: v for k, v in MERGED.enums["ErrorCode"].items() if v not in base}
        self.assertEqual(len(new), 10)
        self.assertTrue(all(1000 <= v <= 1009 for v in new.values()))
        self.assertEqual(len(set(MERGED.enums["ErrorCode"].values())),
                         len(MERGED.enums["ErrorCode"]))

    def test_new_bodies_use_unused_oneof_numbers(self):
        base_nums = {f.number for f in BASE.messages["LeafMessage"]}
        new = [f for f in MERGED.messages["LeafMessage"] if f.number not in base_nums]
        self.assertEqual(sorted(f.number for f in new), [33, 34, 35, 36, 37, 38])
        for f in new:
            self.assertEqual(f.oneof, "body")

    def test_field_numbers_are_unique_and_signatures_come_last(self):
        for m in NEW_MSGS:
            nums = [f.number for f in MERGED.messages[m]]
            self.assertEqual(len(nums), len(set(nums)), m)
            last = MERGED.messages[m][-1]
            if any(f.type_name == "Signature" for f in MERGED.messages[m]):
                self.assertEqual(last.type_name, "Signature", m)

    def test_the_draft_does_not_touch_hardware_parsed_messages(self):
        hw = ["SliceHeader", "Slice", "FrameCommit", "LayerUpdate", "Layer",
              "GlyphAtlasUpdate", "SpeculativeFrameSet", "InputBatch"]
        for m in hw:
            self.assertEqual([(f.name, f.number) for f in BASE.messages[m]],
                             [(f.name, f.number) for f in MERGED.messages[m]], m)


class RoundTrip(unittest.TestCase):
    def test_every_new_body_round_trips_canonically(self):
        for name, n, ok in D.sizes(MERGED):
            self.assertTrue(ok, name)
            self.assertGreater(n, 0)

    def test_a_non_canonical_pause_is_rejected(self):
        obj = {"session_pause": D.samples()["session_pause"]}
        raw = bytearray(pl.encode(MERGED, "LeafMessage", obj))
        # a padded varint at the front of the body is a non-minimal encoding
        bad = bytes([raw[0] | 0x80, 0x00]) + bytes(raw[1:])
        with self.assertRaises(Exception):
            pl.decode(MERGED, "LeafMessage", bad, strict=True)

    def test_the_pause_is_small_next_to_the_resume_cost(self):
        sizes = {n: s for n, s, _ in D.sizes(MERGED)}
        self.assertLess(sizes["session_pause"], 3000)
        self.assertLess(sizes["power_notice"], 64)

    def test_hello_already_carries_the_resume_hook(self):
        names = [f.name for f in BASE.messages["Hello"]]
        self.assertIn("resume_session_id", names)
        self.assertIn("last_frame_shown", names)


if __name__ == "__main__":
    unittest.main()
