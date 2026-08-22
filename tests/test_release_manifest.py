"""Boundary tests for the deterministic v1.0 release-candidate manifest."""

from __future__ import annotations

import copy
import json
import unittest

from scripts import validate_release_manifest


class ReleaseManifestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(
            validate_release_manifest.MANIFEST.read_text(encoding="utf-8")
        )

    def test_current_release_manifest_is_valid(self) -> None:
        self.assertEqual(validate_release_manifest.validate_payload(self.manifest), [])

    def test_content_root_drift_is_rejected(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["content_contract"]["content_root_sha256"] = "0" * 64
        errors = validate_release_manifest.validate_payload(payload)
        self.assertTrue(any("content_contract" in error for error in errors))

    def test_inventory_drift_is_rejected(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["inventory"]["field_cases"] = 999
        errors = validate_release_manifest.validate_payload(payload)
        self.assertTrue(any("inventory" in error for error in errors))

    def test_external_gate_cannot_be_marked_complete_without_contract_change(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["external_gates"][0]["status"] = "complete"
        errors = validate_release_manifest.validate_payload(payload)
        self.assertTrue(any("external_gates" in error for error in errors))
        self.assertTrue(any("must remain not-run" in error for error in errors))

    def test_release_candidate_cannot_enable_promotion(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["promote_allowed"] = True
        errors = validate_release_manifest.validate_payload(payload)
        self.assertTrue(any("cannot allow stable promotion" in error for error in errors))

    def test_manifest_is_excluded_from_its_own_content_root(self) -> None:
        payload, errors = validate_release_manifest.build_manifest()
        self.assertEqual(errors, [])
        self.assertEqual(
            payload["content_contract"]["excluded_paths"],
            [validate_release_manifest.MANIFEST_RELATIVE],
        )

    def test_all_indexed_files_are_grouped_once(self) -> None:
        payload, errors = validate_release_manifest.build_manifest()
        self.assertEqual(errors, [])
        group_count = sum(
            group["file_count"] for group in payload["content_contract"]["groups"]
        )
        self.assertEqual(group_count, payload["content_contract"]["tracked_file_count"])

    def test_required_inventory_is_not_empty(self) -> None:
        payload, errors = validate_release_manifest.build_manifest()
        self.assertEqual(errors, [])
        inventory = payload["inventory"]
        for key in (
            "field_cases",
            "learning_sessions",
            "calibration_scenarios",
            "bilingual_core_pairs",
            "registered_sources",
        ):
            self.assertGreater(inventory[key], 0)


if __name__ == "__main__":
    unittest.main()
