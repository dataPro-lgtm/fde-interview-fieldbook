"""Boundary tests for role-targeting playbook data."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_role_playbooks


class RolePlaybookValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(validate_role_playbooks.MANIFEST.read_text(encoding="utf-8"))

    def write_manifest(self, payload: object) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="role-playbook-test-")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "role-playbooks.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def validate(self, payload: object) -> list[str]:
        errors, _ = validate_role_playbooks.validate_all(self.write_manifest(payload))
        return errors

    def test_current_repository_role_playbooks_are_valid(self) -> None:
        errors, count = validate_role_playbooks.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(count, 3)

    def test_observable_signal_source_must_be_registered(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"][0]["observable_signals"][0]["source_ids"] = ["missing-source"]
        errors = self.validate(payload)
        self.assertTrue(any("unregistered role-playbook sources" in error for error in errors))

    def test_guide_path_must_match_playbook_id(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"][0]["guide"] = "interview-kits/role-playbooks/README.md"
        errors = self.validate(payload)
        self.assertTrue(any("guide must match id" in error for error in errors))

    def test_all_required_playbooks_must_exist(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"] = [
            playbook for playbook in payload["playbooks"] if playbook["id"] != "regulated-ai-fde"
        ]
        errors = self.validate(payload)
        self.assertTrue(any("missing required role playbooks" in error for error in errors))

    def test_interview_hypotheses_cannot_be_empty(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"][0]["interview_hypotheses"] = []
        errors = self.validate(payload)
        self.assertTrue(any("interview hypotheses" in error for error in errors))

    def test_readiness_evidence_ids_must_be_unique(self) -> None:
        payload = copy.deepcopy(self.manifest)
        evidence = payload["playbooks"][0]["readiness_evidence"]
        evidence[1]["id"] = evidence[0]["id"]
        errors = self.validate(payload)
        self.assertTrue(any("duplicate readiness evidence id" in error for error in errors))

    def test_practice_assets_must_exist(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"][0]["practice_assets"][0] = "missing-practice-file.md"
        errors = self.validate(payload)
        self.assertTrue(any("practice_assets[0] does not exist" in error for error in errors))

    def test_explicit_limits_are_required(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"][0]["limits"] = []
        errors = self.validate(payload)
        self.assertTrue(any("explicit limits" in error for error in errors))

    def test_mock_loop_is_required(self) -> None:
        payload = copy.deepcopy(self.manifest)
        del payload["playbooks"][0]["mock_loop"]
        errors = self.validate(payload)
        self.assertTrue(any("missing fields" in error and "mock_loop" in error for error in errors))

    def test_mock_loop_duration_must_be_bounded(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"][0]["mock_loop"]["duration_minutes"] = 180
        errors = self.validate(payload)
        self.assertTrue(any("must be 60-90 minutes" in error for error in errors))

    def test_mock_loop_paths_must_match_playbook_id(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["playbooks"][0]["mock_loop"]["candidate_brief"] = payload["playbooks"][1][
            "mock_loop"
        ]["candidate_brief"]
        errors = self.validate(payload)
        self.assertTrue(any("candidate_brief must match id" in error for error in errors))

    def test_mock_loop_files_must_be_practice_assets(self) -> None:
        payload = copy.deepcopy(self.manifest)
        candidate_brief = payload["playbooks"][0]["mock_loop"]["candidate_brief"]
        payload["playbooks"][0]["practice_assets"].remove(candidate_brief)
        errors = self.validate(payload)
        self.assertTrue(any("must be registered as practice assets" in error for error in errors))

    def test_candidate_brief_must_not_expose_spoiler_sections(self) -> None:
        payload = copy.deepcopy(self.manifest)
        directory = tempfile.TemporaryDirectory(prefix="candidate-spoiler-test-")
        self.addCleanup(directory.cleanup)
        leaked_brief = Path(directory.name) / "candidate-brief.md"
        leaked_brief.write_text(
            "# Brief\n\n## 公开背景\n\n## 面试任务\n\n## 你必须交付\n\n## 私有证据\n",
            encoding="utf-8",
        )
        original_safe_file = validate_role_playbooks.safe_file

        def replace_candidate(relative: object, label: str, errors: list[str]) -> Path | None:
            if label.endswith(".candidate_brief"):
                return leaked_brief
            return original_safe_file(relative, label, errors)

        with patch.object(validate_role_playbooks, "safe_file", side_effect=replace_candidate):
            errors = self.validate(payload)
        self.assertTrue(any("exposes mock-loop spoiler" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
