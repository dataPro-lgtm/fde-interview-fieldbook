#!/usr/bin/env python3
"""Validate the content repository without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CITATION.cff",
    "DISCLAIMER.md",
    "data/sources.json",
    "docs/zh-CN/00-start-here.md",
    "docs/zh-CN/06-production-ai.md",
    "docs/zh-CN/07-casebook.md",
    "docs/zh-CN/08-question-bank.md",
    "interview-kits/rubrics/master-scorecard.md",
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


def validate_markdown_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local_part = unquote(target.split("#", 1)[0])
            if not local_part:
                continue
            resolved = (path.parent / local_part).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"link escapes repository: {path.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken local link: {path.relative_to(ROOT)} -> {target}")


def validate_text_hygiene(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() not in {".cff", ".json", ".md", ".py", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if text and not text.endswith("\n"):
            errors.append(f"text file must end with a newline: {relative}")
        if any(line.endswith((" ", "\t")) for line in text.splitlines()):
            errors.append(f"trailing whitespace: {relative}")
        if PRIVATE_PATH.search(text):
            errors.append(f"private absolute path is forbidden: {relative}")


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
