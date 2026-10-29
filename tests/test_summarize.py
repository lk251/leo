"""Accounting invariants that prevent misleading experiment summaries."""

import importlib.util
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("summarize", ROOT / "scripts" / "summarize.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AccountingTests(unittest.TestCase):
    def setUp(self):
        self.manifest = MODULE.read_json((ROOT / "examples/synthetic/experiment.json").read_text())
        self.rows = [MODULE.read_json(line) for line in
                     (ROOT / "examples/synthetic/trials.jsonl").read_text().splitlines()]

    def first(self, rows=None):
        return MODULE.summarize(self.manifest, self.rows if rows is None else rows)["systems"][0]

    def test_failed_work_is_included_and_synthetic_label_survives(self):
        report = MODULE.summarize(self.manifest, self.rows)
        first = report["systems"][0]
        self.assertEqual(report["data_kind"], "synthetic")
        self.assertEqual(first["accepted_trials"], 2)
        self.assertEqual(first["known_cost_total"], 6)
        self.assertEqual(first["cost_per_accepted_trial"], 3)
        self.assertAlmostEqual(first["success_rate"], 2 / 3)

    def test_unknown_cost_blocks_ratio_even_when_unknown_trial_failed(self):
        self.rows[2]["cost"] = None
        first = self.first()
        self.assertFalse(first["cost_complete"])
        self.assertEqual(first["known_cost_trials"], 2)
        self.assertIsNone(first["cost_per_accepted_trial"])
        self.assertIn("unknown_costs", first["cost_per_accepted_trial_unavailable_reasons"])

    def test_missing_trial_cannot_improve_reported_success_rate_or_cost(self):
        first = self.first(self.rows[:2] + self.rows[3:])
        self.assertFalse(first["complete"])
        self.assertEqual(first["missing_trials"], [{"task_id": "synthetic-task-003", "replicate": 1}])
        self.assertIsNone(first["success_rate"])
        self.assertIsNone(first["cost_per_accepted_trial"])

    def test_zero_accepted_trials_is_not_zero_cost_per_success(self):
        for row in self.rows[:3]:
            row["outcome"] = "failed"
        first = self.first()
        self.assertEqual(first["success_rate"], 0)
        self.assertIsNone(first["cost_per_accepted_trial"])
        self.assertIn("zero_accepted_trials", first["cost_per_accepted_trial_unavailable_reasons"])

    def test_duplicate_or_unplanned_records_cannot_inflate_acceptance(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.first(self.rows + [deepcopy(self.rows[0])])
        self.rows[0]["task_id"] = "not-in-roster"
        with self.assertRaisesRegex(ValueError, "unexpected"):
            self.first()

    def test_critical_failure_cannot_be_accepted(self):
        self.rows[0]["critical_failure"] = True
        with self.assertRaisesRegex(ValueError, "critical failure"):
            self.first()

    def test_infra_errors_and_timeouts_keep_their_cost(self):
        self.rows[1]["outcome"] = "timeout"
        self.rows[2]["outcome"] = "infrastructure_error"
        first = self.first()
        self.assertEqual(first["cost_per_accepted_trial"], 6)
        self.assertEqual(first["outcome_counts"]["timeout"], 1)
        self.assertEqual(first["outcome_counts"]["infrastructure_error"], 1)

    def test_invalid_numeric_values_are_not_free_work(self):
        for value in (-1, float("nan"), float("inf"), True):
            with self.subTest(value=value):
                rows = deepcopy(self.rows)
                rows[0]["cost"] = value
                with self.assertRaises(ValueError):
                    self.first(rows)
        with self.assertRaises(ValueError):
            MODULE.read_json('{"cost": NaN}')

    def test_unknown_timing_is_labeled_with_coverage(self):
        self.rows[0]["wall_seconds"] = None
        first = self.first()
        self.assertEqual(first["wall_seconds"]["known_trials"], 2)
        self.assertEqual(first["wall_seconds"]["missing_or_unknown_trials"], 1)

    def test_duplicate_json_cost_fields_cannot_silently_override_cost(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON object key"):
            MODULE.read_json('{"cost": 12, "cost": 0}')

    def test_detached_report_preserves_selected_cohort(self):
        original = MODULE.summarize(self.manifest, self.rows)
        self.assertEqual(original["scheduled_trial_roster"], self.manifest["trials"])
        for trial in self.manifest["trials"]:
            trial["task_id"] = "other-cohort-" + trial["task_id"]
        for row in self.rows:
            row["task_id"] = "other-cohort-" + row["task_id"]
        changed = MODULE.summarize(self.manifest, self.rows)
        self.assertEqual(changed["systems"], original["systems"])
        self.assertNotEqual(changed["scheduled_trial_roster"], original["scheduled_trial_roster"])
        self.assertNotEqual(changed, original)

    def test_integral_float_replicates_match_integer_keys(self):
        for trial in self.manifest["trials"]:
            trial["replicate"] = 1.0
        self.rows[0]["replicate"] = 1.0
        report = MODULE.summarize(self.manifest, self.rows)
        self.assertTrue(report["complete"])
        self.assertTrue(all(type(trial["replicate"]) is int
                            for trial in report["scheduled_trial_roster"]))
        duplicate = deepcopy(self.rows[0])
        duplicate["replicate"] = 1
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.first(self.rows + [duplicate])
        for value in (True, 0, -1.0, 1.5, float("inf"), float("nan")):
            with self.subTest(value=value):
                rows = deepcopy(self.rows)
                rows[0]["replicate"] = value
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    self.first(rows)


if __name__ == "__main__":
    unittest.main()
