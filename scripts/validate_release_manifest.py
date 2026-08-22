#!/usr/bin/env python3
"""Build or validate the deterministic v1.0 release-candidate manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/release-manifest.json"
MANIFEST_RELATIVE = "data/release-manifest.json"
VERSION_FILE = ROOT / "VERSION"
RELEASE_VERSION = "1.0.0-rc.1"
RELEASE_DATE = "2026-08-22"
EXTERNAL_GATES = [
    {
        "id": "independent-guided-path",
        "status": "not-run",
        "evidence_required": "A non-author reader completes one registered path without author repair and leaves a privacy-safe artifact record.",
    },
    {
        "id": "independent-case-facilitation",
        "status": "not-run",
        "evidence_required": "A non-author facilitator runs every promoted case and records blocking instructions or evidence-release ambiguity.",
    },
    {
        "id": "independent-reviewer-calibration",
        "status": "not-run",
        "evidence_required": "Two independent reviewers blind-score the same answers, adjudicate disagreement, and record resulting material changes.",
    },
    {
        "id": "bilingual-independent-use",
        "status": "not-run",
        "evidence_required": "Chinese-first and English-first non-author readers independently locate and complete equivalent core practice routes.",
    },
]
VALIDATORS = [
    {"id": "repository", "command": "python3 scripts/validate_repo.py", "network": False},
    {"id": "cases", "command": "python3 scripts/validate_case_packs.py", "network": False},
    {"id": "research", "command": "python3 scripts/validate_research_data.py", "network": False},
    {"id": "roles", "command": "python3 scripts/validate_role_playbooks.py", "network": False},
    {"id": "learning", "command": "python3 scripts/validate_learning_paths.py", "network": False},
    {"id": "calibration", "command": "python3 scripts/validate_calibration.py", "network": False},
    {"id": "parity-archive", "command": "python3 scripts/validate_parity_archive.py", "network": False},
    {"id": "unit-tests", "command": "python3 -m unittest discover -s tests -v", "network": False},
    {"id": "python-compile", "command": "python3 -m py_compile scripts/*.py tests/*.py", "network": False},
    {"id": "markdownlint-pinned", "command": "npx --yes markdownlint-cli2@0.18.1 \"**/*.md\" \"#node_modules\"", "network": True},
    {"id": "markdownlint-current", "command": "npx --yes markdownlint-cli2@0.23.2 \"**/*.md\" \"#node_modules\"", "network": True},
    {"id": "mermaid-render", "command": "python3 scripts/validate_mermaid.py --all --no-browser-sandbox", "network": True},
    {"id": "external-links", "command": "python3 scripts/check_external_links.py --timeout 12 --workers 6", "network": True},
    {"id": "diff-whitespace", "command": "git diff --check", "network": False},
]
CLAIM_BOUNDARIES = [
    "A1 proves repository contracts and regression checks, not learner effectiveness.",
    "Synthetic cases and calibration scenarios are not production experience or external review.",
    "No interview pass rate, employment outcome, salary gain, or employer-internal process is claimed.",
    "Stable release promotion remains closed while any external gate is not-run.",
]


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
        return None


def indexed_paths(errors: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"cannot list indexed release files: {exc}")
        return []
    paths = sorted(
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item and item.decode("utf-8") != MANIFEST_RELATIVE
    )
    if len(paths) != len(set(paths)):
        errors.append("git index returned duplicate release paths")
    return paths


def group_name(relative: str) -> str:
    if "/" not in relative:
        return "root"
    first = relative.split("/", 1)[0]
    if first in {".github", "data", "docs", "interview-kits", "scripts", "tests"}:
        return first
    return "other"


def group_content(paths: list[str], errors: list[str]) -> tuple[list[dict[str, object]], int]:
    grouped: dict[str, list[str]] = {}
    total_bytes = 0
    for relative in paths:
        path = (ROOT / relative).resolve()
        try:
            path.relative_to(ROOT)
        except ValueError:
            errors.append(f"indexed path escapes repository: {relative}")
            continue
        if path.is_symlink() or not path.is_file():
            errors.append(f"indexed release path must be a regular file: {relative}")
            continue
        grouped.setdefault(group_name(relative), []).append(relative)

    groups: list[dict[str, object]] = []
    for name in sorted(grouped):
        digest = hashlib.sha256()
        byte_count = 0
        for relative in sorted(grouped[name]):
            content = (ROOT / relative).read_bytes()
            file_digest = hashlib.sha256(content).hexdigest()
            size = len(content)
            byte_count += size
            digest.update(f"{relative}\0{size}\0{file_digest}\n".encode("utf-8"))
        total_bytes += byte_count
        groups.append(
            {
                "name": name,
                "file_count": len(grouped[name]),
                "byte_count": byte_count,
                "sha256": digest.hexdigest(),
            }
        )
    return groups, total_bytes


def content_root(groups: list[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for group in groups:
        digest.update(
            (
                f"{group['name']}\0{group['file_count']}\0{group['byte_count']}\0"
                f"{group['sha256']}\n"
            ).encode("utf-8")
        )
    return digest.hexdigest()


def read_list(path: str, key: str, errors: list[str]) -> list[object]:
    payload = load_json(ROOT / path, errors)
    if not isinstance(payload, dict) or not isinstance(payload.get(key), list):
        errors.append(f"{path} must contain a {key} list")
        return []
    return payload[key]


def build_inventory(paths: list[str], errors: list[str]) -> dict[str, int]:
    cases = read_list("data/case-packs.json", "cases", errors)
    learning_paths = read_list("data/learning-paths.json", "paths", errors)
    scenarios = read_list("data/calibration-scenarios.json", "scenarios", errors)
    pairs = read_list("data/content-parity.json", "core_pairs", errors)
    sources = read_list("data/sources.json", "sources", errors)
    roles = read_list("data/role-playbooks.json", "playbooks", errors)
    archive_entries = read_list("data/source-archives/2026.json", "entries", errors)
    case_files = sum(
        4 + len(case.get("artifacts", []))
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("artifacts"), list)
    )
    sessions = sum(
        len(path.get("sessions", []))
        for path in learning_paths
        if isinstance(path, dict) and isinstance(path.get("sessions"), list)
    )
    ratings = sum(
        len(scenario.get("expected_ratings", []))
        for scenario in scenarios
        if isinstance(scenario, dict) and isinstance(scenario.get("expected_ratings"), list)
    )
    return {
        "tracked_files_excluding_manifest": len(paths),
        "markdown_files": sum(relative.endswith(".md") for relative in paths),
        "registered_sources": len(sources),
        "archived_source_records": len(archive_entries),
        "field_cases": len(cases),
        "registered_case_files": case_files,
        "role_playbooks": len(roles),
        "learning_paths": len(learning_paths),
        "learning_sessions": sessions,
        "calibration_scenarios": len(scenarios),
        "calibration_dimension_ratings": ratings,
        "bilingual_core_pairs": len(pairs),
    }


def build_manifest() -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    try:
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError as exc:
        errors.append(f"cannot read VERSION: {exc}")
        version = ""
    if version != RELEASE_VERSION:
        errors.append(f"VERSION must be {RELEASE_VERSION}, found {version}")
    paths = indexed_paths(errors)
    if MANIFEST_RELATIVE in paths:
        errors.append("release manifest must be excluded from its own content root")
    groups, total_bytes = group_content(paths, errors)
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "version": RELEASE_VERSION,
        "release_date": RELEASE_DATE,
        "status": "release-candidate",
        "evidence_level": "A1",
        "promote_allowed": False,
        "scope": "Reproducible content and automation candidate; external human-effect and independent-use gates remain open.",
        "content_contract": {
            "selection": "Every file in the Git index except data/release-manifest.json itself.",
            "excluded_paths": [MANIFEST_RELATIVE],
            "tracked_file_count": len(paths),
            "total_bytes": total_bytes,
            "content_root_sha256": content_root(groups),
            "groups": groups,
        },
        "inventory": build_inventory(paths, errors),
        "validators": VALIDATORS,
        "external_gates": EXTERNAL_GATES,
        "claim_boundaries": CLAIM_BOUNDARIES,
    }
    return payload, errors


def validate_payload(payload: object) -> list[str]:
    expected, errors = build_manifest()
    if not isinstance(payload, dict):
        return errors + ["release manifest must be a JSON object"]
    for field in expected:
        if payload.get(field) != expected[field]:
            errors.append(f"release manifest differs from current release at: {field}")
    unexpected = set(payload) - set(expected)
    if unexpected:
        errors.append(f"release manifest has unexpected fields: {sorted(unexpected)}")
    gates = payload.get("external_gates")
    if isinstance(gates, list):
        for gate in gates:
            if not isinstance(gate, dict) or gate.get("status") != "not-run":
                errors.append("release candidate external gates must remain not-run without real evidence")
    if payload.get("promote_allowed") is not False:
        errors.append("release candidate cannot allow stable promotion while external gates are open")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print or validate the deterministic v1.0 release-candidate manifest."
    )
    parser.add_argument("--check", action="store_true", help="compare the committed manifest to current indexed content")
    args = parser.parse_args()

    if args.check:
        load_errors: list[str] = []
        payload = load_json(MANIFEST, load_errors)
        errors = load_errors + validate_payload(payload)
        if errors:
            print("Release-manifest validation failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        expected, _ = build_manifest()
        contract = expected["content_contract"]
        inventory = expected["inventory"]
        print(
            "Release-manifest validation passed: "
            f"{contract['tracked_file_count']} indexed files, "
            f"{inventory['field_cases']} cases, "
            f"{inventory['bilingual_core_pairs']} bilingual pairs, "
            f"content root {contract['content_root_sha256']}."
        )
        return 0

    payload, errors = build_manifest()
    if errors:
        print("Release-manifest build failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
