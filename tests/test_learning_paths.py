"""Boundary tests for guided-practice learning paths."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_learning_paths


class LearningPathValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(
            validate_learning_paths.MANIFEST.read_text(encoding="utf-8")
        )

    def write_manifest(self, payload: object) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="learning-path-test-")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "learning-paths.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def validate(self, payload: object) -> list[str]:
        errors, _, _ = validate_learning_paths.validate_all(
            self.write_manifest(payload)
        )
        return errors

    def test_current_repository_learning_paths_are_valid(self) -> None:
        errors, path_count, session_count = validate_learning_paths.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(path_count, 3)
        self.assertEqual(session_count, 29)

    def test_all_required_paths_must_exist(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["paths"] = [
            path
            for path in payload["paths"]
            if path["id"] != "interview-in-7-days"
        ]
        errors = self.validate(payload)
        self.assertTrue(any("missing required learning paths" in error for error in errors))

    def test_path_ids_must_be_unique(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["paths"][1]["id"] = payload["paths"][0]["id"]
        errors = self.validate(payload)
        self.assertTrue(any("duplicate learning path id" in error for error in errors))

    def test_time_budget_must_match_path_contract(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["paths"][0]["time_budget_days"] = 30
        errors = self.validate(payload)
        self.assertTrue(any("time budget must match" in error for error in errors))

    def test_session_order_must_be_contiguous(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["paths"][0]["sessions"][1]["order"] = 8
        errors = self.validate(payload)
        self.assertTrue(any("session order must be contiguous" in error for error in errors))

    def test_session_input_must_exist(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["paths"][0]["sessions"][0]["inputs"][0] = "missing-guide.md"
        errors = self.validate(payload)
        self.assertTrue(any("inputs[0] does not exist" in error for error in errors))

    def test_session_needs_two_completion_checks(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["paths"][0]["sessions"][0]["completion_checks"] = ["One check"]
        errors = self.validate(payload)
        self.assertTrue(any("at least two completion checks" in error for error in errors))

    def test_path_needs_minimum_sessions(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["paths"][0]["sessions"] = payload["paths"][0]["sessions"][:2]
        errors = self.validate(payload)
        self.assertTrue(any("at least 7 sessions" in error for error in errors))

    def test_future_as_of_date_is_rejected(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["as_of"] = "2099-01-01"
        errors = self.validate(payload)
        self.assertTrue(any("as_of is in the future" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
