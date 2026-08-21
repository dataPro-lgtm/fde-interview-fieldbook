"""Boundary tests for versioned research data."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_research_data


class ResearchDataValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.snapshot = json.loads(
            (validate_research_data.ROLE_RADAR_DIR / "2026-Q3.json").read_text(encoding="utf-8")
        )
        self.baselines = json.loads(validate_research_data.BASELINE_PATH.read_text(encoding="utf-8"))
        self.sources = {
            source["id"]
            for source in json.loads(
                (validate_research_data.ROOT / "data/sources.json").read_text(encoding="utf-8")
            )["sources"]
        }

    def write_json(self, payload: object, filename: str) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="research-data-test-")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / filename
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_current_repository_research_data_is_valid(self) -> None:
        errors, snapshot_count, baseline_count = validate_research_data.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(snapshot_count, 1)
        self.assertEqual(baseline_count, 4)

    def test_snapshot_quarter_must_match_as_of_date(self) -> None:
        payload = copy.deepcopy(self.snapshot)
        payload["as_of"] = "2026-04-01"
        errors: list[str] = []
        validate_research_data.validate_role_snapshot(
            self.write_json(payload, "2026-Q3.json"), self.sources, errors
        )
        self.assertTrue(any("quarter mismatch" in error for error in errors))

    def test_geography_evidence_must_reference_an_observation(self) -> None:
        payload = copy.deepcopy(self.snapshot)
        payload["geography_views"][0]["evidence_ids"] = ["missing-observation"]
        errors: list[str] = []
        validate_research_data.validate_role_snapshot(
            self.write_json(payload, "2026-Q3.json"), self.sources, errors
        )
        self.assertTrue(any("unknown geography evidence" in error for error in errors))

    def test_geography_view_requires_an_explicit_limit(self) -> None:
        payload = copy.deepcopy(self.snapshot)
        payload["geography_views"][0]["limitations"] = ""
        errors: list[str] = []
        validate_research_data.validate_role_snapshot(
            self.write_json(payload, "2026-Q3.json"), self.sources, errors
        )
        self.assertTrue(any("requires limitations" in error for error in errors))

    def test_role_observation_source_must_be_registered(self) -> None:
        payload = copy.deepcopy(self.snapshot)
        payload["observations"][0]["source_id"] = "unregistered-source"
        errors: list[str] = []
        validate_research_data.validate_role_snapshot(
            self.write_json(payload, "2026-Q3.json"), self.sources, errors
        )
        self.assertTrue(any("unregistered role radar source" in error for error in errors))

    def test_job_location_requires_region_and_locations(self) -> None:
        payload = copy.deepcopy(self.snapshot)
        payload["observations"][0]["job_locations"][0]["locations"] = []
        errors: list[str] = []
        validate_research_data.validate_role_snapshot(
            self.write_json(payload, "2026-Q3.json"), self.sources, errors
        )
        self.assertTrue(any("job location requires locations" in error for error in errors))

    def test_all_required_technology_baselines_must_exist(self) -> None:
        payload = copy.deepcopy(self.baselines)
        payload["entries"] = [
            entry for entry in payload["entries"] if entry["technology"] != "A2A"
        ]
        errors: list[str] = []
        with patch.object(validate_research_data, "BASELINE_PATH", self.write_json(payload, "baselines.json")):
            validate_research_data.validate_technology_baselines(self.sources, errors)
        self.assertTrue(any("missing required technology baselines" in error for error in errors))

    def test_technology_baseline_source_must_be_registered(self) -> None:
        payload = copy.deepcopy(self.baselines)
        payload["entries"][0]["source_ids"] = ["unregistered-source"]
        errors: list[str] = []
        with patch.object(validate_research_data, "BASELINE_PATH", self.write_json(payload, "baselines.json")):
            validate_research_data.validate_technology_baselines(self.sources, errors)
        self.assertTrue(any("unregistered technology baseline sources" in error for error in errors))

    def test_technology_baseline_requires_a_descriptor(self) -> None:
        payload = copy.deepcopy(self.baselines)
        payload["entries"][0]["baseline"] = ""
        errors: list[str] = []
        with patch.object(validate_research_data, "BASELINE_PATH", self.write_json(payload, "baselines.json")):
            validate_research_data.validate_technology_baselines(self.sources, errors)
        self.assertTrue(any("baseline descriptor is required" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
