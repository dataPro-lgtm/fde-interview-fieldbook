#!/usr/bin/env python3
"""Validate synthetic reviewer-calibration scenarios and evidence anchors."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/calibration-scenarios.json"
REQUIRED_SCENARIO_IDS = {
    "premature-agent-solution",
    "agent-terms-without-state",
    "bounded-thin-slice",
    "field-to-product-leverage",
    "coding-not-observed",
    "fixed-version-regression",
    "unsafe-refund-retry",
    "adoption-experiment-boundary",
}
ALLOWED_DIMENSIONS = {
    "discovery",
    "value-adoption",
    "coding-delivery",
    "data-system",
    "ai-engineering",
    "evaluation-operations",
    "security-governance",
    "communication-productization",
}
ALLOWED_RATINGS = {"1", "2", "3", "4", "N/O"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_DISAGREEMENTS = {
    "no-observation-as-low",
    "term-density",
    "role-level",
    "risk-underweight",
    "product-leverage-overreach",
    "evidence-inference",
}
SCENARIO_FIELDS = {
    "id",
    "title",
    "synthetic",
    "target_dimensions",
    "prompt",
    "transcript",
    "expected_ratings",
    "veto",
    "adjudication",
    "practice_assets",
}
TRANSCRIPT_FIELDS = {"speaker", "text"}
RATING_FIELDS = {
    "dimension",
    "rating",
    "confidence",
    "evidence_quotes",
    "rationale",
    "next_probe",
}
ADJUDICATION_FIELDS = {
    "disagreement_types",
    "common_misread",
    "questions",
    "do_not_infer",
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
        errors.append(f"invalid JSON in {path.name}: {exc}")
        return None


def safe_file(relative: object, label: str, errors: list[str]) -> None:
    if not nonempty_string(relative):
        errors.append(f"{label} must be a non-empty repository path")
        return
    path = (ROOT / str(relative)).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        errors.append(f"{label} escapes repository: {relative}")
        return
    if not path.is_file():
        errors.append(f"{label} does not exist: {relative}")


def validate_transcript(value: object, label: str, errors: list[str]) -> str:
    if not isinstance(value, list) or len(value) < 2:
        errors.append(f"{label} needs at least two transcript turns")
        return ""
    texts: list[str] = []
    for index, turn in enumerate(value):
        turn_label = f"{label}[{index}]"
        if not isinstance(turn, dict) or set(turn) != TRANSCRIPT_FIELDS:
            errors.append(f"{turn_label} must contain {sorted(TRANSCRIPT_FIELDS)}")
            continue
        if turn["speaker"] not in {"candidate", "interviewer"}:
            errors.append(f"invalid transcript speaker in {turn_label}: {turn['speaker']}")
        if not nonempty_string(turn["text"]):
            errors.append(f"transcript text is required: {turn_label}")
        else:
            texts.append(turn["text"])
    return "\n".join(texts)


def validate_expected_ratings(
    value: object,
    target_dimensions: set[str],
    transcript_text: str,
    label: str,
    errors: list[str],
) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{label} requires expected ratings")
        return []
    dimensions: list[str] = []
    ratings: list[str] = []
    for index, rating in enumerate(value):
        rating_label = f"{label}[{index}]"
        if not isinstance(rating, dict) or set(rating) != RATING_FIELDS:
            errors.append(f"{rating_label} must contain {sorted(RATING_FIELDS)}")
            continue
        dimension = rating["dimension"]
        score = rating["rating"]
        confidence = rating["confidence"]
        if dimension not in ALLOWED_DIMENSIONS:
            errors.append(f"unsupported rating dimension in {rating_label}: {dimension}")
        dimensions.append(dimension)
        if score not in ALLOWED_RATINGS:
            errors.append(f"unsupported expected rating in {rating_label}: {score}")
        ratings.append(score)
        if confidence not in ALLOWED_CONFIDENCE:
            errors.append(f"unsupported confidence in {rating_label}: {confidence}")
        for field in ("rationale", "next_probe"):
            if not nonempty_string(rating[field]):
                errors.append(f"{field} is required: {rating_label}")
        quotes = rating["evidence_quotes"]
        if score == "N/O":
            if quotes != []:
                errors.append(f"N/O rating must not invent evidence quotes: {rating_label}")
        elif not nonempty_strings(quotes):
            errors.append(f"numeric rating requires evidence quotes: {rating_label}")
        else:
            for quote in quotes:
                if quote not in transcript_text:
                    errors.append(f"evidence quote is not present in transcript: {rating_label} -> {quote}")

    if len(dimensions) != len(set(dimensions)):
        errors.append(f"expected rating dimensions must be unique: {label}")
    if set(dimensions) != target_dimensions:
        errors.append(
            f"expected ratings must exactly cover target dimensions: {label} -> {dimensions}"
        )
    return ratings


def validate_adjudication(value: object, label: str, errors: list[str]) -> None:
    if not isinstance(value, dict) or set(value) != ADJUDICATION_FIELDS:
        errors.append(f"{label} must contain {sorted(ADJUDICATION_FIELDS)}")
        return
    types = value["disagreement_types"]
    if not nonempty_strings(types):
        errors.append(f"{label}.disagreement_types requires at least one entry")
    else:
        if len(types) != len(set(types)):
            errors.append(f"{label}.disagreement_types must be unique")
        unknown = set(types) - ALLOWED_DISAGREEMENTS
        if unknown:
            errors.append(f"unsupported disagreement types in {label}: {sorted(unknown)}")
    if not nonempty_strings(value["questions"], minimum=2):
        errors.append(f"{label}.questions requires at least two entries")
    for field in ("common_misread", "do_not_infer"):
        if not nonempty_string(value[field]):
            errors.append(f"{label}.{field} is required")


def validate_scenario(scenario: object, ids: set[str], errors: list[str]) -> int:
    if not isinstance(scenario, dict):
        errors.append("calibration scenario must be an object")
        return 0
    missing = SCENARIO_FIELDS - scenario.keys()
    if missing:
        errors.append(f"calibration scenario missing fields: {sorted(missing)}")
        return 0

    scenario_id = scenario["id"]
    if not isinstance(scenario_id, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", scenario_id
    ):
        errors.append(f"invalid calibration scenario id: {scenario_id}")
        return 0
    if scenario_id in ids:
        errors.append(f"duplicate calibration scenario id: {scenario_id}")
    ids.add(scenario_id)
    label = f"calibration-scenarios.{scenario_id}"

    if not nonempty_string(scenario["title"]):
        errors.append(f"scenario title is required: {scenario_id}")
    if scenario["synthetic"] is not True:
        errors.append(f"calibration scenario must be explicitly synthetic: {scenario_id}")
    if not nonempty_string(scenario["prompt"]):
        errors.append(f"scenario prompt is required: {scenario_id}")

    dimensions = scenario["target_dimensions"]
    if not nonempty_strings(dimensions) or len(dimensions) > 3:
        errors.append(f"scenario needs one to three target dimensions: {scenario_id}")
        target_dimensions: set[str] = set()
    else:
        target_dimensions = set(dimensions)
        if len(dimensions) != len(target_dimensions):
            errors.append(f"target dimensions must be unique: {scenario_id}")
        unknown = target_dimensions - ALLOWED_DIMENSIONS
        if unknown:
            errors.append(f"unsupported target dimensions in {scenario_id}: {sorted(unknown)}")

    transcript_text = validate_transcript(scenario["transcript"], f"{label}.transcript", errors)
    ratings = validate_expected_ratings(
        scenario["expected_ratings"],
        target_dimensions,
        transcript_text,
        f"{label}.expected_ratings",
        errors,
    )

    veto = scenario["veto"]
    if not isinstance(veto, bool):
        errors.append(f"scenario veto must be boolean: {scenario_id}")
    elif veto and "1" not in ratings:
        errors.append(f"veto scenario requires at least one rating of 1: {scenario_id}")

    validate_adjudication(scenario["adjudication"], f"{label}.adjudication", errors)

    assets = scenario["practice_assets"]
    if not nonempty_strings(assets):
        errors.append(f"scenario requires practice assets: {scenario_id}")
    else:
        if len(assets) != len(set(assets)):
            errors.append(f"scenario practice assets must be unique: {scenario_id}")
        for index, relative in enumerate(assets):
            safe_file(relative, f"{label}.practice_assets[{index}]", errors)
    return len(ratings)


def validate_all(manifest_path: Path = MANIFEST) -> tuple[list[str], int, int]:
    errors: list[str] = []
    payload = load_json(manifest_path, errors)
    if not isinstance(payload, dict):
        return errors, 0, 0
    if payload.get("schema_version") != "1.0":
        errors.append("calibration-scenarios.json schema_version must be 1.0")
    try:
        as_of = date.fromisoformat(str(payload.get("as_of")))
        if as_of > date.today():
            errors.append(f"calibration-scenarios.json as_of is in the future: {as_of.isoformat()}")
    except ValueError:
        errors.append(f"invalid calibration-scenarios.json as_of date: {payload.get('as_of')}")
    if not nonempty_string(payload.get("scope_note")):
        errors.append("calibration-scenarios.json requires a scope_note")

    scenarios = payload.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("calibration-scenarios.json requires a non-empty scenarios list")
        return errors, 0, 0

    ids: set[str] = set()
    rating_count = 0
    for scenario in scenarios:
        rating_count += validate_scenario(scenario, ids, errors)
    missing = REQUIRED_SCENARIO_IDS - ids
    if missing:
        errors.append(f"missing required calibration scenarios: {sorted(missing)}")
    return errors, len(scenarios), rating_count


def main() -> int:
    errors, scenario_count, rating_count = validate_all()
    if errors:
        print("Calibration-scenario validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Calibration-scenario validation passed: {scenario_count} synthetic scenarios, "
        f"{rating_count} evidence-anchored dimension ratings."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
