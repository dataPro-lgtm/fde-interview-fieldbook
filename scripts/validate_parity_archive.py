#!/usr/bin/env python3
"""Validate bilingual learner-outcome parity and source-ledger archives."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARITY_MANIFEST = ROOT / "data/content-parity.json"
SOURCE_ARCHIVE = ROOT / "data/source-archives/2026.json"
SOURCE_LEDGER = ROOT / "data/sources.json"
REQUIRED_PAIR_IDS = {
    "start-here",
    "role-map",
    "interview-loop",
    "discovery",
    "coding-data-delivery",
    "system-design",
    "production-ai",
    "case-practice",
    "question-bank",
    "behavioral-field-leadership",
    "study-plans",
    "portfolio-evidence",
    "answer-calibration",
    "field-operating-playbook",
    "job-targeting",
    "guided-practice",
}
ALLOWED_STATUSES = {"full", "condensed", "planned"}
PAIR_FIELDS = {
    "id",
    "zh_path",
    "en_path",
    "status",
    "scope_note",
    "learner_outcomes",
    "practice_assets",
}
ARCHIVE_FIELDS = {
    "schema_version",
    "year",
    "captured_at",
    "snapshot_path",
    "ledger_sha256",
    "record_count",
    "scope",
    "excluded_fields",
    "entries",
}
ARCHIVE_ENTRY_FIELDS = {
    "id",
    "publisher",
    "title",
    "url",
    "source_kind",
    "authority",
    "last_checked",
}
FORBIDDEN_ARCHIVE_KEYS = {
    "page_body",
    "body",
    "html",
    "quoted_passage",
    "access_token",
    "access_tokens",
    "credential",
    "credentials",
}


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_strings(value: object, minimum: int = 1) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(nonempty_string(item) for item in value)
    )


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
        return None


def safe_file(relative: object, label: str, errors: list[str]) -> Path | None:
    if not nonempty_string(relative):
        errors.append(f"{label} must be a non-empty repository path")
        return None
    path = (ROOT / str(relative)).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        errors.append(f"{label} escapes repository: {relative}")
        return None
    if not path.is_file():
        errors.append(f"{label} does not exist: {relative}")
        return None
    return path


def validate_pair(
    pair: object,
    ids: set[str],
    zh_paths: set[str],
    en_paths: set[str],
    errors: list[str],
) -> None:
    if not isinstance(pair, dict) or set(pair) != PAIR_FIELDS:
        errors.append(f"content parity pair must contain {sorted(PAIR_FIELDS)}")
        return
    pair_id = pair["id"]
    if not isinstance(pair_id, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", pair_id
    ):
        errors.append(f"invalid content parity id: {pair_id}")
        return
    if pair_id in ids:
        errors.append(f"duplicate content parity id: {pair_id}")
    ids.add(pair_id)
    label = f"content-parity.{pair_id}"

    status = pair["status"]
    if status not in ALLOWED_STATUSES:
        errors.append(f"unsupported parity status in {label}: {status}")
    if status != "full":
        errors.append(f"v0.9 core pair must have full learner-outcome parity: {pair_id}")
    if not nonempty_string(pair["scope_note"]):
        errors.append(f"scope_note is required: {label}")
    if not nonempty_strings(pair["learner_outcomes"], minimum=3):
        errors.append(f"at least three learner outcomes are required: {label}")
    elif len(pair["learner_outcomes"]) != len(set(pair["learner_outcomes"])):
        errors.append(f"learner outcomes must be unique: {label}")

    for language, seen in (("zh", zh_paths), ("en", en_paths)):
        relative = pair[f"{language}_path"]
        path = safe_file(relative, f"{label}.{language}_path", errors)
        if isinstance(relative, str):
            if relative in seen:
                errors.append(f"duplicate {language} parity path: {relative}")
            seen.add(relative)
            expected_prefix = f"docs/{'zh-CN' if language == 'zh' else 'en'}/"
            if not relative.startswith(expected_prefix):
                errors.append(f"{language} parity path must start with {expected_prefix}: {relative}")
        if language == "en" and status == "full" and path is not None:
            text = path.read_text(encoding="utf-8")
            if len(text) < 2500:
                errors.append(f"full English parity chapter is too thin: {relative}")
            if len(re.findall(r"^##\s+", text, flags=re.MULTILINE)) < 3:
                errors.append(f"full English parity chapter needs at least three H2 sections: {relative}")

    assets = pair["practice_assets"]
    if not nonempty_strings(assets):
        errors.append(f"practice assets are required: {label}")
    else:
        if len(assets) != len(set(assets)):
            errors.append(f"practice assets must be unique: {label}")
        for index, asset in enumerate(assets):
            safe_file(asset, f"{label}.practice_assets[{index}]", errors)


def validate_parity(path: Path, errors: list[str]) -> int:
    payload = load_json(path, errors)
    if not isinstance(payload, dict):
        return 0
    if payload.get("schema_version") != "1.0":
        errors.append("content-parity.json schema_version must be 1.0")
    try:
        as_of = date.fromisoformat(str(payload.get("as_of")))
        if as_of > date.today():
            errors.append(f"content-parity.json as_of is in the future: {as_of.isoformat()}")
    except ValueError:
        errors.append(f"invalid content-parity.json as_of date: {payload.get('as_of')}")
    if not nonempty_string(payload.get("parity_definition")):
        errors.append("content-parity.json requires a parity_definition")
    if set(payload.get("allowed_statuses", [])) != ALLOWED_STATUSES:
        errors.append("content-parity.json allowed_statuses do not match validator contract")

    pairs = payload.get("core_pairs")
    if not isinstance(pairs, list) or not pairs:
        errors.append("content-parity.json requires a non-empty core_pairs list")
        return 0
    ids: set[str] = set()
    zh_paths: set[str] = set()
    en_paths: set[str] = set()
    for pair in pairs:
        validate_pair(pair, ids, zh_paths, en_paths, errors)

    missing_ids = REQUIRED_PAIR_IDS - ids
    extra_ids = ids - REQUIRED_PAIR_IDS
    if missing_ids:
        errors.append(f"missing required content parity pairs: {sorted(missing_ids)}")
    if extra_ids:
        errors.append(f"unexpected core content parity pairs: {sorted(extra_ids)}")

    published_zh = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs/zh-CN").glob("[0-9][0-9]-*.md")
    }
    missing_zh = published_zh - zh_paths
    extra_zh = zh_paths - published_zh
    if missing_zh:
        errors.append(f"unregistered Chinese core chapters: {sorted(missing_zh)}")
    if extra_zh:
        errors.append(f"parity manifest registers non-core Chinese paths: {sorted(extra_zh)}")
    return len(pairs)


def find_forbidden_keys(value: object, prefix: str = "archive") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            current = f"{prefix}.{key}"
            if key.lower() in FORBIDDEN_ARCHIVE_KEYS:
                found.append(current)
            found.extend(find_forbidden_keys(child, current))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_forbidden_keys(child, f"{prefix}[{index}]"))
    return found


def source_projection(source: object) -> dict[str, object] | None:
    if not isinstance(source, dict):
        return None
    return {field: source.get(field) for field in ARCHIVE_ENTRY_FIELDS}


def validate_archive(archive_path: Path, ledger_path: Path, errors: list[str]) -> int:
    archive = load_json(archive_path, errors)
    ledger = load_json(ledger_path, errors)
    if not isinstance(archive, dict) or not isinstance(ledger, dict):
        return 0
    if set(archive) != ARCHIVE_FIELDS:
        errors.append(f"source archive must contain exactly {sorted(ARCHIVE_FIELDS)}")
        return 0
    if archive["schema_version"] != "1.0":
        errors.append("source archive schema_version must be 1.0")
    if archive["year"] != 2026:
        errors.append("2026 source archive year must be 2026")
    try:
        captured = date.fromisoformat(str(archive["captured_at"]))
        if captured.year != archive["year"]:
            errors.append("source archive captured_at must match archive year")
        if captured > date.today():
            errors.append("source archive captured_at cannot be in the future")
    except ValueError:
        errors.append(f"invalid source archive captured_at: {archive['captured_at']}")
    if archive["snapshot_path"] != "data/sources.json":
        errors.append("source archive snapshot_path must be data/sources.json")
    if not nonempty_string(archive["scope"]):
        errors.append("source archive requires a scope statement")
    if not FORBIDDEN_ARCHIVE_KEYS.intersection(set(archive["excluded_fields"])):
        errors.append("source archive must explicitly exclude restricted body or credential fields")

    forbidden = find_forbidden_keys(archive)
    if forbidden:
        errors.append(f"source archive contains forbidden content keys: {sorted(forbidden)}")

    actual_digest = hashlib.sha256(ledger_path.read_bytes()).hexdigest()
    expected_digest = archive["ledger_sha256"]
    if not isinstance(expected_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_digest):
        errors.append("source archive ledger_sha256 must be a lowercase SHA-256 digest")
    elif expected_digest != actual_digest:
        errors.append(
            f"source archive digest does not match data/sources.json: {expected_digest} != {actual_digest}"
        )

    sources = ledger.get("sources")
    entries = archive["entries"]
    if not isinstance(sources, list) or not isinstance(entries, list):
        errors.append("source ledger and archive entries must be lists")
        return 0
    if archive["record_count"] != len(entries):
        errors.append("source archive record_count does not match entries")
    if len(entries) != len(sources):
        errors.append("source archive entry count does not match source ledger")

    archive_by_id: dict[object, object] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != ARCHIVE_ENTRY_FIELDS:
            errors.append(
                f"source archive entry {index} must contain exactly {sorted(ARCHIVE_ENTRY_FIELDS)}"
            )
            continue
        entry_id = entry["id"]
        if entry_id in archive_by_id:
            errors.append(f"duplicate source archive id: {entry_id}")
        archive_by_id[entry_id] = entry
        for field in ARCHIVE_ENTRY_FIELDS:
            if not nonempty_string(entry[field]):
                errors.append(f"source archive entry requires {field}: {entry_id}")

    ledger_by_id: dict[object, object] = {}
    for source in sources:
        projection = source_projection(source)
        if projection is None:
            errors.append("source ledger entry must be an object")
            continue
        source_id = projection["id"]
        if source_id in ledger_by_id:
            errors.append(f"duplicate source ledger id: {source_id}")
        ledger_by_id[source_id] = projection

    if set(archive_by_id) != set(ledger_by_id):
        errors.append("source archive ids do not exactly match source ledger ids")
    else:
        for source_id, projection in ledger_by_id.items():
            if archive_by_id[source_id] != projection:
                errors.append(f"source archive metadata differs from ledger: {source_id}")
    return len(entries)


def validate_all(
    parity_path: Path = PARITY_MANIFEST,
    archive_path: Path = SOURCE_ARCHIVE,
    ledger_path: Path = SOURCE_LEDGER,
) -> tuple[list[str], int, int]:
    errors: list[str] = []
    pair_count = validate_parity(parity_path, errors)
    archive_count = validate_archive(archive_path, ledger_path, errors)
    return errors, pair_count, archive_count


def main() -> int:
    errors, pair_count, archive_count = validate_all()
    if errors:
        print("Parity and source-archive validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Parity and source-archive validation passed: {pair_count} full learner-outcome "
        f"pairs, {archive_count} archived source metadata records."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
