"""Tests of the Zero-CPU declaration in chips.json."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import zero_cpu as Z  # noqa: E402
import leaffw as L    # noqa: E402


class Declaration(unittest.TestCase):
    def setUp(self):
        self.chips = Z.load()

    def test_no_part_fails(self):
        for c in self.chips:
            self.assertNotEqual(Z.verdict(c)[0], "FAIL", c["id"])

    def test_only_the_euicc_is_open(self):
        opened = [c["id"] for c in self.chips if Z.verdict(c)[0] == "OPEN"]
        self.assertEqual(opened, ["EUICC"])

    def test_no_part_takes_instructions_from_the_network(self):
        for c in self.chips:
            self.assertFalse(c["instruction_input"], c["id"])
            self.assertFalse(c["loads_user_code"], c["id"])
            self.assertFalse(c["app_visible_os"], c["id"])

    def test_every_updatable_part_is_in_the_demo_manifest_or_sealed(self):
        demo = {c for c, *_ in L.DEMO_CHIPS}
        for c in self.chips:
            if c["updatable"] and c["id"] not in ("CAM", "PORT"):
                self.assertIn(c["id"], demo, c["id"])

    def test_methods_match_the_tool(self):
        for c in self.chips:
            if c["measure"] != "none":
                self.assertIn(c["measure"], L.MEASURE_METHODS)

    def test_an_interpreter_is_caught(self):
        c = dict(self.chips[0], interpreter=True, open=[])
        self.assertEqual(Z.verdict(c)[0], "FAIL")

    def test_a_foreign_signer_is_caught(self):
        c = dict(self.chips[0], signers=["vendor", "app-store"], open=[])
        self.assertEqual(Z.verdict(c)[0], "FAIL")

    def test_an_ungated_radio_is_caught(self):
        c = [x for x in self.chips if x["id"] == "U2A"][0]
        c = dict(c, gate="none", open=[])
        self.assertEqual(Z.verdict(c)[0], "FAIL")


if __name__ == "__main__":
    unittest.main()
