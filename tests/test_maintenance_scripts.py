"""Boundary tests for repository maintenance scripts."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts import check_external_links, validate_mermaid


class ExternalLinkSafetyTests(unittest.TestCase):
    def test_normalize_removes_fragment_and_preserves_query(self) -> None:
        normalized = check_external_links.normalize_url("https://example.com/docs?q=1#section")
        self.assertEqual(normalized, "https://example.com/docs?q=1")

    def test_rejects_non_https_before_request(self) -> None:
        error = check_external_links.target_error("http://example.com/")
        self.assertIn("HTTPS", error or "")

    def test_rejects_loopback_before_request(self) -> None:
        error = check_external_links.target_error("https://127.0.0.1/")
        self.assertIn("non-public", error or "")

    def test_rejects_non_standard_port_before_request(self) -> None:
        error = check_external_links.target_error("https://example.com:8443/")
        self.assertIn("non-standard", error or "")

    def test_confirmed_not_found_is_hard_failure(self) -> None:
        result = check_external_links.classify_http("https://example.com/missing", 404, "GET")
        self.assertEqual(result.result, "FAIL")

    def test_rate_limit_is_soft_failure(self) -> None:
        result = check_external_links.classify_http("https://example.com/limited", 429, "GET")
        self.assertEqual(result.result, "SOFT")


class MermaidExtractionTests(unittest.TestCase):
    def write_fixture(self, text: str) -> Path:
        temporary = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            prefix="mermaid-test-",
            dir=validate_mermaid.ROOT,
            encoding="utf-8",
            delete=False,
        )
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        with temporary:
            temporary.write(text)
        return Path(temporary.name)

    def test_extracts_multiple_blocks_with_source_lines(self) -> None:
        fixture = self.write_fixture(
            "# Test\n\n```mermaid\nflowchart TD\nA --> B\n```\n\n"
            "```mermaid\nsequenceDiagram\nA->>B: hello\n```\n"
        )
        blocks = validate_mermaid.extract_blocks(fixture)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].line, 3)
        self.assertEqual(blocks[1].line, 8)

    def test_rejects_empty_block(self) -> None:
        fixture = self.write_fixture("# Test\n\n```mermaid\n```\n")
        with self.assertRaisesRegex(ValueError, "empty Mermaid block"):
            validate_mermaid.extract_blocks(fixture)

    def test_rejects_unterminated_block(self) -> None:
        fixture = self.write_fixture("# Test\n\n```mermaid\nflowchart TD\nA --> B\n")
        with self.assertRaisesRegex(ValueError, "unterminated Mermaid block"):
            validate_mermaid.extract_blocks(fixture)

    @patch.object(validate_mermaid.subprocess, "run")
    def test_validator_change_selects_all_markdown(self, run: Mock) -> None:
        run.return_value = Mock(
            returncode=0,
            stdout="scripts/validate_mermaid.py\n",
            stderr="",
        )
        selected = validate_mermaid.changed_markdown("base-sha")
        self.assertGreater(len(selected), 20)
        self.assertIn(validate_mermaid.ROOT / "README.md", selected)

    @patch.object(validate_mermaid.subprocess, "run")
    def test_non_markdown_changes_are_ignored(self, run: Mock) -> None:
        run.return_value = Mock(
            returncode=0,
            stdout="README.md\nscripts/check_external_links.py\n",
            stderr="",
        )
        selected = validate_mermaid.changed_markdown("base-sha")
        self.assertEqual(selected, [validate_mermaid.ROOT / "README.md"])


if __name__ == "__main__":
    unittest.main()
