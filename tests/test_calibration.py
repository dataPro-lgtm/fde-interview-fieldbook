"""Boundary tests for calibration scenarios and disagreement summaries."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts import summarize_calibration, validate_calibration


class CalibrationScenarioValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(validate_calibration.MANIFEST.read_text(encoding="utf-8"))

    def write_manifest(self, payload: object) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="calibration-scenario-test-")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "calibration-scenarios.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def validate(self, payload: object) -> list[str]:
        errors, _, _ = validate_calibration.validate_all(self.write_manifest(payload))
        return errors

    def test_current_synthetic_scenarios_are_valid(self) -> None:
        errors, scenario_count, rating_count = validate_calibration.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(scenario_count, 8)
        self.assertEqual(rating_count, 13)

    def test_required_scenario_cannot_disappear(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["scenarios"] = payload["scenarios"][1:]
        errors = self.validate(payload)
        self.assertTrue(any("missing required calibration scenarios" in error for error in errors))

    def test_scenarios_must_be_labeled_synthetic(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["scenarios"][0]["synthetic"] = False
        errors = self.validate(payload)
        self.assertTrue(any("explicitly synthetic" in error for error in errors))

    def test_numeric_evidence_quote_must_exist_in_transcript(self) -> None:
        payload = copy.deepcopy(self.manifest)
        rating = payload["scenarios"][0]["expected_ratings"][0]
        rating["evidence_quotes"] = ["A quote that was never said"]
        errors = self.validate(payload)
        self.assertTrue(any("not present in transcript" in error for error in errors))

    def test_not_observed_rating_has_no_invented_quote(self) -> None:
        payload = copy.deepcopy(self.manifest)
        scenario = next(item for item in payload["scenarios"] if item["id"] == "coding-not-observed")
        scenario["expected_ratings"][0]["evidence_quotes"] = ["Invented"]
        errors = self.validate(payload)
        self.assertTrue(any("N/O rating must not invent" in error for error in errors))

    def test_veto_requires_a_rating_of_one(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["scenarios"][0]["expected_ratings"][0]["rating"] = "2"
        errors = self.validate(payload)
        self.assertTrue(any("veto scenario requires" in error for error in errors))

    def test_expected_ratings_cover_target_dimensions(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["scenarios"][1]["expected_ratings"] = payload["scenarios"][1]["expected_ratings"][:1]
        errors = self.validate(payload)
        self.assertTrue(any("exactly cover target dimensions" in error for error in errors))

    def test_practice_asset_must_exist(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["scenarios"][0]["practice_assets"][0] = "missing-calibration-asset.md"
        errors = self.validate(payload)
        self.assertTrue(any("practice_assets[0] does not exist" in error for error in errors))


class CalibrationSummaryTests(unittest.TestCase):
    def rating(
        self,
        scenario: str,
        reviewer: str,
        dimension: str,
        rating: str,
    ) -> dict[str, str]:
        return {
            "scenario_id": scenario,
            "reviewer_id": reviewer,
            "dimension": dimension,
            "rating": rating,
            "confidence": "medium",
            "evidence": "Synthetic evidence excerpt",
        }

    def test_summary_separates_numeric_and_not_observed_conflicts(self) -> None:
        payload = {
            "schema_version": "1.0",
            "ratings": [
                self.rating("s1", "a", "discovery", "3"),
                self.rating("s1", "b", "discovery", "4"),
                self.rating("s1", "a", "coding", "N/O"),
                self.rating("s1", "b", "coding", "2"),
            ],
        }
        errors, summary = summarize_calibration.summarize(payload)
        self.assertEqual(errors, [])
        self.assertEqual(summary["rating_pairs"], 2)
        self.assertEqual(summary["numeric_pairs"], 1)
        self.assertEqual(summary["within_one_numeric_pairs"], 1)
        self.assertEqual(summary["mean_absolute_numeric_gap"], 1.0)
        self.assertEqual(summary["no_observation_conflicts"], 1)

    def test_summary_flags_veto_risk_disagreement(self) -> None:
        payload = {
            "schema_version": "1.0",
            "ratings": [
                self.rating("s1", "a", "security", "1"),
                self.rating("s1", "b", "security", "4"),
            ],
        }
        errors, summary = summarize_calibration.summarize(payload)
        self.assertEqual(errors, [])
        self.assertEqual(summary["veto_risk_conflicts"], 1)

    def test_duplicate_reviewer_dimension_is_rejected(self) -> None:
        duplicate = self.rating("s1", "a", "security", "2")
        payload = {
            "schema_version": "1.0",
            "ratings": [duplicate, dict(duplicate)],
        }
        errors, _ = summarize_calibration.summarize(payload)
        self.assertTrue(any("duplicate reviewer rating" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
