#!/usr/bin/env python3
"""Validate the content repository without third-party dependencies."""

from __future__ import annotations

import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    ".github/ISSUE_TEMPLATE/claim-dispute.yml",
    ".github/workflows/external-link-health.yml",
    "ACCESSIBILITY.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CITATION.cff",
    "DISCLAIMER.md",
    "data/case-packs.json",
    "data/learning-paths.json",
    "data/role-playbooks.json",
    "data/role-radar/2026-Q3.json",
    "data/sources.json",
    "data/technology-baselines.json",
    "docs/en/interview-loop.md",
    "docs/en/guided-practice.md",
    "docs/en/job-targeting.md",
    "docs/en/portfolio-evidence.md",
    "docs/en/reading-map.md",
    "docs/en/system-design.md",
    "docs/research/claim-review-process.md",
    "docs/research/documentation-site-evaluation.md",
    "docs/research/release-validation-0.6.md",
    "docs/research/release-validation-0.7.md",
    "docs/research/role-radar/2026-Q3.md",
    "docs/research/release-validation-0.5.md",
    "docs/research/role-radar/README.md",
    "docs/research/technology-baseline-changelog.md",
    "docs/research/version-plan-0.6-to-1.0.md",
    "docs/zh-CN/00-start-here.md",
    "docs/zh-CN/06-production-ai.md",
    "docs/zh-CN/07-casebook.md",
    "docs/zh-CN/08-question-bank.md",
    "docs/zh-CN/12-answer-calibration.md",
    "docs/zh-CN/13-field-operating-playbook.md",
    "docs/zh-CN/14-job-targeting.md",
    "docs/zh-CN/15-guided-practice.md",
    "interview-kits/role-playbooks/README.md",
    "interview-kits/role-playbooks/ai-agent-fde.md",
    "interview-kits/role-playbooks/data-platform-fde.md",
    "interview-kits/role-playbooks/regulated-ai-fde.md",
    "interview-kits/role-playbooks/worked-example.md",
    "interview-kits/mock-loops/role-targeted/README.md",
    "interview-kits/mock-loops/role-targeted/pilot-protocol.md",
    "interview-kits/mock-loops/role-targeted/score-sheet.md",
    "interview-kits/rubrics/master-scorecard.md",
    "interview-kits/rubrics/reviewer-calibration.md",
    "interview-kits/cases/README.md",
    "interview-kits/cases/facilitation-standard.md",
    "interview-kits/worksheets/field-delivery-pack.md",
    "interview-kits/worksheets/job-targeting-pack.md",
    "interview-kits/worksheets/practice-journal.md",
    "scripts/check_external_links.py",
    "scripts/validate_learning_paths.py",
    "scripts/validate_mermaid.py",
    "scripts/validate_research_data.py",
    "scripts/validate_role_playbooks.py",
    "tests/test_maintenance_scripts.py",
    "tests/test_learning_paths.py",
    "tests/test_case_packs.py",
    "tests/test_research_data.py",
    "tests/test_role_playbooks.py",
}
FORBIDDEN_PUBLIC_EXTENSIONS = {
    ".7z",
    ".docx",
    ".pdf",
    ".ppt",
    ".pptx",
    ".rar",
    ".xls",
    ".xlsm",
    ".xlsx",
    ".zip",
}
MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
PRIVATE_PATH = re.compile("(?:/" + "Users/|[A-Za-z]:\\\\Users\\\\)")
REQUIRED_SOURCE_FIELDS = {
    "id",
    "publisher",
    "title",
    "url",
    "source_kind",
    "authority",
    "last_checked",
    "refresh_days",
    "topics",
    "note",
}


def validate_required(errors: list[str]) -> None:
    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")


def validate_forbidden_files(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_PUBLIC_EXTENSIONS:
            errors.append(f"proprietary/binary source file is forbidden: {path.relative_to(ROOT)}")


def github_markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    occurrences: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        heading = match.group(1)
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading)
        heading = html.unescape(heading).lower()
        heading = re.sub(r"[`*_~]", "", heading)
        base = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        occurrence = occurrences.get(base, 0)
        occurrences[base] = occurrence + 1
        anchors.add(base if occurrence == 0 else f"{base}-{occurrence}")
    return anchors


def validate_markdown_links(errors: list[str]) -> None:
    anchor_cache: dict[Path, set[str]] = {}
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            local_target, separator, raw_fragment = target.partition("#")
            local_part = unquote(local_target)
            fragment = unquote(raw_fragment).lower()
            resolved = path.resolve() if not local_part else (path.parent / local_part).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"link escapes repository: {path.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link: {path.relative_to(ROOT)} -> {target}")
                continue
            if separator and fragment and resolved.suffix.lower() == ".md":
                anchors = anchor_cache.setdefault(resolved, github_markdown_anchors(resolved))
                if fragment not in anchors:
                    errors.append(f"broken local anchor: {path.relative_to(ROOT)} -> {target}")


def validate_text_hygiene(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() not in {".cff", ".csv", ".json", ".md", ".py", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if text and not text.endswith("\n"):
            errors.append(f"text file must end with a newline: {relative}")
        lines = text.splitlines()
        markdown_hard_break = path.suffix.lower() == ".md"
        invalid_trailing = any(
            line.endswith("\t")
            or (
                len(line) - len(line.rstrip(" ")) > 0
                and not (markdown_hard_break and len(line) - len(line.rstrip(" ")) == 2)
            )
            for line in lines
        )
        if invalid_trailing:
            errors.append(f"trailing whitespace: {relative}")
        if PRIVATE_PATH.search(text):
            errors.append(f"private absolute path is forbidden: {relative}")


def validate_markdown_structure(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        h1_count = sum(line.startswith("# ") for line in text.splitlines())
        if h1_count != 1:
            errors.append(f"Markdown file must contain exactly one H1: {relative} (found {h1_count})")
        if text.count("<details>") != text.count("</details>"):
            errors.append(f"unbalanced details blocks: {relative}")
        if text.count("```") % 2:
            errors.append(f"unbalanced fenced code blocks: {relative}")


def validate_sources(errors: list[str]) -> None:
    source_path = ROOT / "data/sources.json"
    try:
        payload = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid sources.json: {exc}")
        return

    if payload.get("schema_version") != "1.0":
        errors.append("sources.json schema_version must be 1.0")
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources.json must contain a non-empty sources list")
        return

    ids: set[str] = set()
    urls: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"source #{index} is not an object")
            continue
        missing = REQUIRED_SOURCE_FIELDS - source.keys()
        if missing:
            errors.append(f"source #{index} missing fields: {sorted(missing)}")
            continue
        source_id = source["id"]
        if source_id in ids:
            errors.append(f"duplicate source id: {source_id}")
        ids.add(source_id)
        source_url = str(source["url"])
        if source_url in urls:
            errors.append(f"duplicate source URL: {source_url}")
        urls.add(source_url)
        if not source_url.startswith("https://"):
            errors.append(f"source URL must use https: {source_id}")
        if source["authority"] not in {"official", "corroborated", "community"}:
            errors.append(f"invalid source authority: {source_id}")
        if not isinstance(source["topics"], list) or not source["topics"]:
            errors.append(f"source topics must be a non-empty list: {source_id}")
        try:
            checked = date.fromisoformat(source["last_checked"])
            if checked > date.today():
                errors.append(f"source last_checked is in the future: {source_id}")
        except (TypeError, ValueError):
            errors.append(f"invalid source last_checked date: {source_id}")
        if not isinstance(source["refresh_days"], int) or source["refresh_days"] <= 0:
            errors.append(f"source refresh_days must be a positive integer: {source_id}")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_forbidden_files(errors)
    validate_markdown_links(errors)
    validate_text_hygiene(errors)
    validate_markdown_structure(errors)
    validate_sources(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    markdown_count = sum(1 for _ in ROOT.rglob("*.md"))
    source_count = len(json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"])
    print(f"Repository validation passed: {markdown_count} Markdown files, {source_count} registered sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
