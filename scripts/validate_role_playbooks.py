#!/usr/bin/env python3
"""Validate role-targeting playbooks and their evidence contract."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/role-playbooks.json"
PLAYBOOK_DIR = ROOT / "interview-kits/role-playbooks"
REQUIRED_PLAYBOOK_IDS = {"ai-agent-fde", "data-platform-fde", "regulated-ai-fde"}
PLAYBOOK_FIELDS = {
    "id",
    "title",
    "guide",
    "mock_loop",
    "observable_signals",
    "interview_hypotheses",
    "readiness_evidence",
    "practice_assets",
    "limits",
}
SIGNAL_FIELDS = {"id", "summary", "source_ids", "candidate_proof"}
EVIDENCE_FIELDS = {"id", "claim", "accepted_artifacts", "boundary"}
MOCK_LOOP_FIELDS = {"duration_minutes", "candidate_brief", "interviewer_guide"}
MOCK_REQUIRED_HEADINGS = {
    "candidate_brief": ("## 公开背景", "## 面试任务", "## 你必须交付"),
    "interviewer_guide": ("## 运行流程", "## 私有证据", "## 评分"),
}
CANDIDATE_SPOILER_TOKENS = ("interviewer-guide", "## 私有证据", "## 事故注入")


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


def registered_source_ids(errors: list[str]) -> set[str]:
    payload = load_json(ROOT / "data/sources.json", errors)
    if not isinstance(payload, dict) or not isinstance(payload.get("sources"), list):
        return set()
    return {
        source["id"]
        for source in payload["sources"]
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }


def safe_file(relative: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(relative, str) or not relative.strip():
        errors.append(f"{label} must be a non-empty path")
        return None
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        errors.append(f"{label} escapes repository: {relative}")
        return None
    if not path.is_file():
        errors.append(f"{label} does not exist: {relative}")
        return None
    return path


def validate_signal(
    signal: object,
    label: str,
    known_sources: set[str],
    signal_ids: set[str],
    errors: list[str],
) -> None:
    if not isinstance(signal, dict):
        errors.append(f"observable signal must be an object: {label}")
        return
    missing = SIGNAL_FIELDS - signal.keys()
    if missing:
        errors.append(f"observable signal missing fields in {label}: {sorted(missing)}")
        return
    signal_id = signal["id"]
    if not isinstance(signal_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", signal_id):
        errors.append(f"invalid observable signal id in {label}: {signal_id}")
    elif signal_id in signal_ids:
        errors.append(f"duplicate observable signal id in {label}: {signal_id}")
    else:
        signal_ids.add(signal_id)
    if not isinstance(signal["summary"], str) or not signal["summary"].strip():
        errors.append(f"observable signal summary is required: {label}")
    if not nonempty_strings(signal["source_ids"]):
        errors.append(f"observable signal source_ids are required: {label}")
    else:
        unknown = set(signal["source_ids"]) - known_sources
        if unknown:
            errors.append(f"unregistered role-playbook sources in {label}: {sorted(unknown)}")
    if not nonempty_strings(signal["candidate_proof"], minimum=2):
        errors.append(f"observable signal needs at least two candidate proofs: {label}")


def validate_evidence(
    evidence: object,
    label: str,
    evidence_ids: set[str],
    errors: list[str],
) -> None:
    if not isinstance(evidence, dict):
        errors.append(f"readiness evidence must be an object: {label}")
        return
    missing = EVIDENCE_FIELDS - evidence.keys()
    if missing:
        errors.append(f"readiness evidence missing fields in {label}: {sorted(missing)}")
        return
    evidence_id = evidence["id"]
    if not isinstance(evidence_id, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", evidence_id
    ):
        errors.append(f"invalid readiness evidence id in {label}: {evidence_id}")
    elif evidence_id in evidence_ids:
        errors.append(f"duplicate readiness evidence id in {label}: {evidence_id}")
    else:
        evidence_ids.add(evidence_id)
    for field in ("claim", "boundary"):
        if not isinstance(evidence[field], str) or not evidence[field].strip():
            errors.append(f"readiness evidence {field} is required: {label}")
    if not nonempty_strings(evidence["accepted_artifacts"], minimum=2):
        errors.append(f"readiness evidence needs at least two accepted artifacts: {label}")


def validate_mock_loop(
    mock_loop: object,
    playbook_id: str,
    mock_paths: set[str],
    errors: list[str],
) -> set[str]:
    label = f"role-playbooks.{playbook_id}.mock_loop"
    if not isinstance(mock_loop, dict):
        errors.append(f"role playbook mock_loop must be an object: {playbook_id}")
        return set()
    missing = MOCK_LOOP_FIELDS - mock_loop.keys()
    if missing:
        errors.append(f"role playbook mock_loop missing fields in {label}: {sorted(missing)}")
        return set()

    duration = mock_loop["duration_minutes"]
    if not isinstance(duration, int) or not 60 <= duration <= 90:
        errors.append(f"role playbook mock loop must be 60-90 minutes: {playbook_id}")

    registered_paths: set[str] = set()
    for role in ("candidate_brief", "interviewer_guide"):
        relative = mock_loop[role]
        expected = f"interview-kits/mock-loops/role-targeted/{playbook_id}/{role.replace('_', '-')}.md"
        if relative != expected:
            errors.append(f"role playbook {role} must match id: {playbook_id} -> {relative}")
        path = safe_file(relative, f"{label}.{role}", errors)
        if not isinstance(relative, str):
            continue
        if relative in mock_paths:
            errors.append(f"duplicate role playbook mock-loop path: {relative}")
        mock_paths.add(relative)
        registered_paths.add(relative)
        if path is None:
            continue
        text = path.read_text(encoding="utf-8")
        for heading in MOCK_REQUIRED_HEADINGS[role]:
            if heading not in text:
                errors.append(f"{role} missing heading '{heading}': {relative}")
        if role == "candidate_brief":
            lowered = text.lower()
            for token in CANDIDATE_SPOILER_TOKENS:
                if token.lower() in lowered:
                    errors.append(f"candidate brief exposes mock-loop spoiler '{token}': {relative}")
    return registered_paths


def validate_playbook(
    playbook: object,
    known_sources: set[str],
    playbook_ids: set[str],
    guide_paths: set[str],
    mock_paths: set[str],
    errors: list[str],
) -> None:
    if not isinstance(playbook, dict):
        errors.append("role playbook entry must be an object")
        return
    missing = PLAYBOOK_FIELDS - playbook.keys()
    if missing:
        errors.append(f"role playbook entry missing fields: {sorted(missing)}")
        return

    playbook_id = playbook["id"]
    if not isinstance(playbook_id, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", playbook_id
    ):
        errors.append(f"invalid role playbook id: {playbook_id}")
        return
    if playbook_id in playbook_ids:
        errors.append(f"duplicate role playbook id: {playbook_id}")
    playbook_ids.add(playbook_id)
    label = f"role-playbooks.{playbook_id}"

    if not isinstance(playbook["title"], str) or not playbook["title"].strip():
        errors.append(f"role playbook title is required: {playbook_id}")

    guide = playbook["guide"]
    guide_path = safe_file(guide, f"{label}.guide", errors)
    if isinstance(guide, str):
        if guide in guide_paths:
            errors.append(f"duplicate role playbook guide: {guide}")
        guide_paths.add(guide)
        expected = f"interview-kits/role-playbooks/{playbook_id}.md"
        if guide != expected:
            errors.append(f"role playbook guide must match id: {playbook_id} -> {guide}")
    if guide_path is not None and guide_path.parent != PLAYBOOK_DIR.resolve():
        errors.append(f"role playbook guide must be inside role-playbooks directory: {guide}")

    mock_assets = validate_mock_loop(playbook["mock_loop"], playbook_id, mock_paths, errors)

    signals = playbook["observable_signals"]
    if not isinstance(signals, list) or len(signals) < 4:
        errors.append(f"role playbook needs at least four observable signals: {playbook_id}")
    else:
        signal_ids: set[str] = set()
        for index, signal in enumerate(signals):
            validate_signal(signal, f"{label}.observable_signals[{index}]", known_sources, signal_ids, errors)

    if not nonempty_strings(playbook["interview_hypotheses"], minimum=3):
        errors.append(f"role playbook needs at least three interview hypotheses: {playbook_id}")

    evidence = playbook["readiness_evidence"]
    if not isinstance(evidence, list) or len(evidence) < 5:
        errors.append(f"role playbook needs at least five readiness evidence entries: {playbook_id}")
    else:
        evidence_ids: set[str] = set()
        for index, item in enumerate(evidence):
            validate_evidence(item, f"{label}.readiness_evidence[{index}]", evidence_ids, errors)

    assets = playbook["practice_assets"]
    if not nonempty_strings(assets, minimum=4):
        errors.append(f"role playbook needs at least four practice assets: {playbook_id}")
    else:
        if len(assets) != len(set(assets)):
            errors.append(f"role playbook practice assets must be unique: {playbook_id}")
        missing_mock_assets = mock_assets - set(assets)
        if missing_mock_assets:
            errors.append(
                f"role playbook mock-loop files must be registered as practice assets: "
                f"{playbook_id} -> {sorted(missing_mock_assets)}"
            )
        for index, asset in enumerate(assets):
            safe_file(asset, f"{label}.practice_assets[{index}]", errors)

    if not nonempty_strings(playbook["limits"], minimum=3):
        errors.append(f"role playbook needs at least three explicit limits: {playbook_id}")


def validate_all(manifest_path: Path = MANIFEST) -> tuple[list[str], int]:
    errors: list[str] = []
    payload = load_json(manifest_path, errors)
    if not isinstance(payload, dict):
        return errors, 0
    if payload.get("schema_version") != "1.0":
        errors.append("role-playbooks.json schema_version must be 1.0")
    try:
        as_of = date.fromisoformat(str(payload.get("as_of")))
        if as_of > date.today():
            errors.append(f"role-playbooks.json as_of is in the future: {as_of.isoformat()}")
    except ValueError:
        errors.append(f"invalid role-playbooks.json as_of date: {payload.get('as_of')}")
    if not isinstance(payload.get("scope_note"), str) or not payload["scope_note"].strip():
        errors.append("role-playbooks.json requires a scope_note")

    playbooks = payload.get("playbooks")
    if not isinstance(playbooks, list) or not playbooks:
        errors.append("role-playbooks.json requires a non-empty playbooks list")
        return errors, 0

    known_sources = registered_source_ids(errors)
    playbook_ids: set[str] = set()
    guide_paths: set[str] = set()
    mock_paths: set[str] = set()
    for playbook in playbooks:
        validate_playbook(playbook, known_sources, playbook_ids, guide_paths, mock_paths, errors)

    missing = REQUIRED_PLAYBOOK_IDS - playbook_ids
    if missing:
        errors.append(f"missing required role playbooks: {sorted(missing)}")

    published_guides = {
        path.stem
        for path in PLAYBOOK_DIR.glob("*.md")
        if path.name not in {"README.md", "worked-example.md"}
    }
    unregistered = published_guides - playbook_ids
    if unregistered:
        errors.append(f"unregistered role playbook guides: {sorted(unregistered)}")

    return errors, len(playbooks)


def main() -> int:
    errors, playbook_count = validate_all()
    if errors:
        print("Role-playbook validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Role-playbook validation passed: {playbook_count} playbooks with sourced signals, "
        "spoiler-separated mock loops, and practice assets."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
