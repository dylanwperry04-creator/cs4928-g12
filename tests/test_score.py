"""Checks for the scoring maths. Run: python3 -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from score import decide, mcc, per_class  # noqa: E402


class ScoreTests(unittest.TestCase):
    def test_perfect_predictions(self):
        truth = ["Obvious", "Task", "Not a smell", "Obvious"]
        self.assertAlmostEqual(mcc(truth, truth), 1.0)

    def test_constant_prediction_gives_zero_mcc(self):
        truth = ["Obvious", "Task", "Not a smell", "Obvious"]
        self.assertEqual(mcc(truth, ["Not a smell"] * 4), 0.0)

    def test_binary_mcc_matches_hand_calculation(self):
        # tp=2 tn=1 fp=1 fn=0 -> (2*1 - 1*0) / sqrt(3*2*2*1) = 0.5774
        truth = ["Task", "Task", "Not a smell", "Not a smell"]
        pred = ["Task", "Task", "Task", "Not a smell"]
        self.assertAlmostEqual(mcc(truth, pred), 0.5774, places=4)

    def test_per_class_counts(self):
        rows = {r["label"]: r for r in per_class(["Task", "Obvious"], ["Task", "Task"])}
        self.assertEqual(rows["Task"]["precision"], 0.5)
        self.assertEqual(rows["Task"]["recall"], 1.0)
        self.assertEqual(rows["Obvious"]["recall"], 0.0)

    def test_decision_rule(self):
        self.assertEqual(decide(0.70, 0.45, True), "REPRODUCED")
        self.assertEqual(decide(0.60, 0.45, True), "NOT REPRODUCED")
        self.assertEqual(decide(0.72, 0.30, True), "NOT REPRODUCED")
        self.assertEqual(decide(0.72, 0.51, False), "INCONCLUSIVE")


if __name__ == "__main__":
    unittest.main()
