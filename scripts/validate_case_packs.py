#!/usr/bin/env python3
"""Validate the published case-pack contract without third-party packages."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections.abc import Iterable
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/case-packs.json"
CASE_FIELDS = {
    "id",
    "title",
    "duration_minutes",
    "difficulty",
    "risk_domains",
    "field_skills",
    "release_gates",
    "human_validation",
    "candidate_brief",
    "interviewer_brief",
    "rubric",
    "debrief",
    "artifacts",
}
REQUIRED_CASE_IDS = {
    "data-platform-migration",
    "air-gapped-ai-deployment",
    "production-incident",
    "agent-tool-side-effect",
    "knowledge-sync-lifecycle",
    "durable-agent-streaming",
    "evaluation-regression",
    "cross-border-ai-deployment",
    "adoption-rescue",
    "connector-productization",
}
ALLOWED_DIFFICULTIES = {"intermediate", "advanced"}
ALLOWED_RISK_DOMAINS = {
    "adoption",
    "agent-side-effects",
    "cross-border",
    "data-lifecycle",
    "durable-execution",
    "evaluation",
    "incident-response",
    "migration",
    "productization",
    "security",
}
REQUIRED_RISK_COVERAGE = ALLOWED_RISK_DOMAINS
ALLOWED_FIELD_SKILLS = {"Frame", "Inspect", "Engineer", "Launch", "Distill"}
HUMAN_VALIDATION_FIELDS = {"status", "independent_runs", "note"}
ALLOWED_HUMAN_STATUSES = {"not-run", "independent-run", "multi-run"}
SPOILER_TOKENS = ("interviewer-brief", "debrief.md", "rubric.md", "artifacts/")
REQUIRED_HEADINGS = {
    "candidate_brief": ("## 公开背景", "## 你的任务", "## 交付物"),
    "interviewer_brief": ("## 运行流程", "## 证据释放", "## 追问", "## 评分"),
    "rubric": ("## 评分", "## 一票否决"),
    "debrief": ("## 关键判断", "## 参考推演", "## 常见失败"),
}


def nonempty_strings(value: object, minimum: int = 1) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.name}: {exc}")
        return None


def validate_unique_allowed_strings(
    value: object,
    label: str,
    allowed: set[str],
    minimum: int,
    errors: list[str],
) -> set[str]:
    if not nonempty_strings(value, minimum=minimum):
        errors.append(f"{label} needs at least {minimum} entries")
        return set()
    items = list(value) if isinstance(value, Iterable) else []
    if len(items) != len(set(items)):
        errors.append(f"{label} entries must be unique")
    unknown = set(items) - allowed
    if unknown:
        errors.append(f"{label} contains unsupported entries: {sorted(unknown)}")
    return set(items)


def validate_human_validation(value: object, case_id: str, errors: list[str]) -> None:
    label = f"human validation for {case_id}"
    if not isinstance(value, dict) or set(value) != HUMAN_VALIDATION_FIELDS:
        errors.append(f"{label} must contain {sorted(HUMAN_VALIDATION_FIELDS)}")
        return
    status = value["status"]
    runs = value["independent_runs"]
    note = value["note"]
    if status not in ALLOWED_HUMAN_STATUSES:
        errors.append(f"invalid human validation status for {case_id}: {status}")
    if not isinstance(runs, int) or isinstance(runs, bool) or runs < 0:
        errors.append(f"independent_runs must be a non-negative integer: {case_id}")
        return
    if status == "not-run" and runs != 0:
        errors.append(f"not-run human validation must have zero runs: {case_id}")
    if status == "independent-run" and runs < 1:
        errors.append(f"independent-run status requires at least one run: {case_id}")
    if status == "multi-run" and runs < 3:
        errors.append(f"multi-run status requires at least three runs: {case_id}")
    if not isinstance(note, str) or not note.strip():
        errors.append(f"human validation note is required: {case_id}")


def safe_path(relative: str, errors: list[str]) -> Path | None:
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        errors.append(f"case path escapes repository: {relative}")
        return None
    if not path.is_file():
        errors.append(f"case file does not exist: {relative}")
        return None
    return path


def validate_csv(path: Path, errors: list[str]) -> None:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 2:
        errors.append(f"case CSV needs a header and data row: {path.relative_to(ROOT)}")
        return
    width = len(rows[0])
    if width < 2 or any(len(row) != width for row in rows):
        errors.append(f"case CSV is not rectangular: {path.relative_to(ROOT)}")


def validate_markdown_role(role: str, path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for heading in REQUIRED_HEADINGS[role]:
        if heading not in text:
            errors.append(f"{role} missing heading '{heading}': {path.relative_to(ROOT)}")
    if role == "candidate_brief":
        lowered = text.lower()
        for token in SPOILER_TOKENS:
            if token in lowered:
                errors.append(f"candidate brief links to spoiler material: {path.relative_to(ROOT)}")


def validate_case_location(path: Path, case_root: Path, case_id: str, errors: list[str]) -> None:
    try:
        path.relative_to(case_root.resolve())
    except ValueError:
        errors.append(f"case references a file outside its own directory: {case_id} -> {path.relative_to(ROOT)}")


def validate_case(
    case: object,
    ids: set[str],
    observed_risks: set[str],
    errors: list[str],
) -> int:
    if not isinstance(case, dict):
        errors.append("case entry is not an object")
        return 0
    missing = CASE_FIELDS - case.keys()
    if missing:
        errors.append(f"case entry missing fields: {sorted(missing)}")
        return 0

    case_id = case["id"]
    if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", case_id):
        errors.append(f"invalid case id: {case_id}")
        return 0
    if case_id in ids:
        errors.append(f"duplicate case id: {case_id}")
    ids.add(case_id)

    duration = case["duration_minutes"]
    if not isinstance(duration, int) or not 45 <= duration <= 120:
        errors.append(f"case duration must be 45-120 minutes: {case_id}")

    difficulty = case["difficulty"]
    if difficulty not in ALLOWED_DIFFICULTIES:
        errors.append(f"invalid case difficulty: {case_id} -> {difficulty}")

    risks = validate_unique_allowed_strings(
        case["risk_domains"],
        f"risk_domains for {case_id}",
        ALLOWED_RISK_DOMAINS,
        2,
        errors,
    )
    observed_risks.update(risks)
    validate_unique_allowed_strings(
        case["field_skills"],
        f"field_skills for {case_id}",
        ALLOWED_FIELD_SKILLS,
        3,
        errors,
    )
    if not nonempty_strings(case["release_gates"], minimum=2):
        errors.append(f"release_gates need at least two entries: {case_id}")
    elif len(case["release_gates"]) != len(set(case["release_gates"])):
        errors.append(f"release_gates must be unique: {case_id}")
    validate_human_validation(case["human_validation"], case_id, errors)

    case_root = ROOT / "interview-kits/cases" / case_id
    if not (case_root / "README.md").is_file():
        errors.append(f"case is missing README.md: {case_id}")

    referenced: set[str] = set()
    for role in ("candidate_brief", "interviewer_brief", "rubric", "debrief"):
        relative = case[role]
        if not isinstance(relative, str):
            errors.append(f"{role} path must be a string: {case_id}")
            continue
        referenced.add(relative)
        path = safe_path(relative, errors)
        if path is not None:
            validate_case_location(path, case_root, case_id, errors)
            validate_markdown_role(role, path, errors)

    artifacts = case["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) < 3:
        errors.append(f"case needs at least three staged artifacts: {case_id}")
        return len(referenced)

    rounds: set[int] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) != {"round", "path"}:
            errors.append(f"invalid artifact entry: {case_id}")
            continue
        round_number = artifact["round"]
        relative = artifact["path"]
        if not isinstance(round_number, int) or round_number < 1:
            errors.append(f"artifact round must be a positive integer: {case_id}")
        else:
            rounds.add(round_number)
        if not isinstance(relative, str):
            errors.append(f"artifact path must be a string: {case_id}")
            continue
        if relative in referenced:
            errors.append(f"duplicate case path in manifest: {relative}")
        referenced.add(relative)
        path = safe_path(relative, errors)
        if path is None:
            continue
        validate_case_location(path, case_root, case_id, errors)
        if path.suffix.lower() == ".csv":
            validate_csv(path, errors)
        elif path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid case JSON {path.relative_to(ROOT)}: {exc}")

    if rounds != set(range(1, max(rounds, default=0) + 1)):
        errors.append(f"artifact rounds must be contiguous from 1: {case_id}")

    expected = referenced | {(case_root / "README.md").relative_to(ROOT).as_posix()}
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in case_root.rglob("*")
        if path.is_file() and not path.name.startswith(".")
    }
    for relative in sorted(actual - expected):
        errors.append(f"case file is not registered in manifest: {relative}")
    for relative in sorted(expected - actual):
        errors.append(f"registered case file is outside case package: {case_id} -> {relative}")
    return len(referenced)


def validate_all(manifest_path: Path = MANIFEST) -> tuple[list[str], int, int]:
    errors: list[str] = []
    payload = load_json(manifest_path, errors)
    if not isinstance(payload, dict):
        return errors, 0, 0

    if payload.get("schema_version") != "2.0":
        errors.append("case-packs.json schema_version must be 2.0")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("case-packs.json must contain a non-empty cases list")
        cases = []

    ids: set[str] = set()
    observed_risks: set[str] = set()
    file_count = 0
    for case in cases:
        file_count += validate_case(case, ids, observed_risks, errors)

    missing_cases = REQUIRED_CASE_IDS - ids
    if missing_cases:
        errors.append(f"missing required case packs: {sorted(missing_cases)}")
    missing_risks = REQUIRED_RISK_COVERAGE - observed_risks
    if missing_risks:
        errors.append(f"case portfolio missing risk coverage: {sorted(missing_risks)}")

    case_root = ROOT / "interview-kits/cases"
    case_directories = {
        path.name
        for path in case_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    for case_id in sorted(case_directories - ids):
        errors.append(f"case directory is not registered in manifest: {case_id}")

    return errors, len(cases), file_count


def main() -> int:
    errors, case_count, file_count = validate_all()

    if errors:
        print("Case-pack validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Case-pack validation passed: {case_count} cases, {file_count} referenced files, "
        f"{len(REQUIRED_RISK_COVERAGE)} risk domains covered."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
