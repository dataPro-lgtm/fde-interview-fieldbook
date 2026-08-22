"""Boundary tests for bilingual parity and source-ledger archives."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts import validate_parity_archive


class ParityArchiveValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parity = json.loads(
            validate_parity_archive.PARITY_MANIFEST.read_text(encoding="utf-8")
        )
        self.archive = json.loads(
            validate_parity_archive.SOURCE_ARCHIVE.read_text(encoding="utf-8")
        )

    def write_json(self, name: str, payload: object) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="parity-archive-test-")
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def validate_parity(self, payload: object) -> list[str]:
        errors: list[str] = []
        validate_parity_archive.validate_parity(
            self.write_json("content-parity.json", payload), errors
        )
        return errors

    def validate_archive(self, payload: object) -> list[str]:
        errors: list[str] = []
        validate_parity_archive.validate_archive(
            self.write_json("2026.json", payload),
            validate_parity_archive.SOURCE_LEDGER,
            errors,
        )
        return errors

    def test_current_parity_and_archive_are_valid(self) -> None:
        errors, pair_count, source_count = validate_parity_archive.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(pair_count, 16)
        self.assertEqual(source_count, 17)

    def test_required_pair_cannot_disappear(self) -> None:
        payload = copy.deepcopy(self.parity)
        payload["core_pairs"] = payload["core_pairs"][1:]
        errors = self.validate_parity(payload)
        self.assertTrue(any("missing required content parity pairs" in error for error in errors))

    def test_full_pair_requires_three_outcomes(self) -> None:
        payload = copy.deepcopy(self.parity)
        payload["core_pairs"][0]["learner_outcomes"] = ["one", "two"]
        errors = self.validate_parity(payload)
        self.assertTrue(any("at least three learner outcomes" in error for error in errors))

    def test_duplicate_english_path_is_rejected(self) -> None:
        payload = copy.deepcopy(self.parity)
        payload["core_pairs"][1]["en_path"] = payload["core_pairs"][0]["en_path"]
        errors = self.validate_parity(payload)
        self.assertTrue(any("duplicate en parity path" in error for error in errors))

    def test_practice_asset_must_exist(self) -> None:
        payload = copy.deepcopy(self.parity)
        payload["core_pairs"][0]["practice_assets"] = ["missing-practice-asset.md"]
        errors = self.validate_parity(payload)
        self.assertTrue(any("practice_assets[0] does not exist" in error for error in errors))

    def test_core_status_cannot_hide_condensed_material(self) -> None:
        payload = copy.deepcopy(self.parity)
        payload["core_pairs"][0]["status"] = "condensed"
        errors = self.validate_parity(payload)
        self.assertTrue(any("must have full learner-outcome parity" in error for error in errors))

    def test_archive_hash_must_match_source_ledger(self) -> None:
        payload = copy.deepcopy(self.archive)
        payload["ledger_sha256"] = "0" * 64
        errors = self.validate_archive(payload)
        self.assertTrue(any("digest does not match" in error for error in errors))

    def test_archive_metadata_must_match_source_ledger(self) -> None:
        payload = copy.deepcopy(self.archive)
        payload["entries"][0]["title"] = "Invented archived title"
        errors = self.validate_archive(payload)
        self.assertTrue(any("metadata differs from ledger" in error for error in errors))

    def test_archive_rejects_page_body(self) -> None:
        payload = copy.deepcopy(self.archive)
        payload["page_body"] = "Copied page content"
        errors = self.validate_archive(payload)
        self.assertTrue(any("must contain exactly" in error for error in errors))

    def test_archive_count_must_match_entries(self) -> None:
        payload = copy.deepcopy(self.archive)
        payload["record_count"] = 999
        errors = self.validate_archive(payload)
        self.assertTrue(any("record_count does not match" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
