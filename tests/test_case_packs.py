"""Boundary tests for production Field Case Lab manifests."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_case_packs


class CasePackValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(
            validate_case_packs.MANIFEST.read_text(encoding="utf-8")
        )

    def write_manifest(self, payload: object) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="case-pack-test-")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "case-packs.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def validate(self, payload: object) -> list[str]:
        errors, _, _ = validate_case_packs.validate_all(self.write_manifest(payload))
        return errors

    def test_current_repository_case_portfolio_is_valid(self) -> None:
        errors, case_count, file_count = validate_case_packs.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(case_count, 10)
        self.assertEqual(file_count, 72)

    def test_all_required_cases_must_exist(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["cases"] = [
            case
            for case in payload["cases"]
            if case["id"] != "agent-tool-side-effect"
        ]
        errors = self.validate(payload)
        self.assertTrue(any("missing required case packs" in error for error in errors))

    def test_case_risk_domains_must_be_supported(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["cases"][0]["risk_domains"][0] = "generic-ai"
        errors = self.validate(payload)
        self.assertTrue(any("unsupported entries" in error for error in errors))

    def test_case_risk_domains_must_be_unique(self) -> None:
        payload = copy.deepcopy(self.manifest)
        risks = payload["cases"][0]["risk_domains"]
        risks[1] = risks[0]
        errors = self.validate(payload)
        self.assertTrue(any("risk_domains" in error and "unique" in error for error in errors))

    def test_field_skills_need_three_distinct_entries(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["cases"][0]["field_skills"] = ["Frame", "Frame"]
        errors = self.validate(payload)
        self.assertTrue(any("field_skills" in error for error in errors))

    def test_release_gates_need_two_entries(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["cases"][0]["release_gates"] = ["One gate"]
        errors = self.validate(payload)
        self.assertTrue(any("release_gates need at least two" in error for error in errors))

    def test_not_run_status_requires_zero_runs(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["cases"][0]["human_validation"]["independent_runs"] = 1
        errors = self.validate(payload)
        self.assertTrue(any("not-run human validation" in error for error in errors))

    def test_multi_run_status_requires_three_runs(self) -> None:
        payload = copy.deepcopy(self.manifest)
        validation = payload["cases"][0]["human_validation"]
        validation["status"] = "multi-run"
        validation["independent_runs"] = 2
        errors = self.validate(payload)
        self.assertTrue(any("at least three runs" in error for error in errors))

    def test_invalid_difficulty_is_rejected(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["cases"][0]["difficulty"] = "expert-only"
        errors = self.validate(payload)
        self.assertTrue(any("invalid case difficulty" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
