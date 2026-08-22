#!/usr/bin/env python3
"""Summarize anonymous reviewer disagreement without third-party packages."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path


ALLOWED_RATINGS = {"1", "2", "3", "4", "N/O"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
RATING_FIELDS = {
    "scenario_id",
    "reviewer_id",
    "dimension",
    "rating",
    "confidence",
    "evidence",
}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def summarize(payload: object) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    empty_summary: dict[str, object] = {
        "rating_pairs": 0,
        "exact_agreement_pairs": 0,
        "numeric_pairs": 0,
        "within_one_numeric_pairs": 0,
        "mean_absolute_numeric_gap": None,
        "no_observation_conflicts": 0,
        "veto_risk_conflicts": 0,
        "groups_without_two_reviewers": 0,
    }
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0":
        errors.append("calibration run schema_version must be 1.0")
        return errors, empty_summary
    ratings = payload.get("ratings")
    if not isinstance(ratings, list) or not ratings:
        errors.append("calibration run requires a non-empty ratings list")
        return errors, empty_summary

    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    seen: set[tuple[str, str, str]] = set()
    for index, rating in enumerate(ratings):
        label = f"ratings[{index}]"
        if not isinstance(rating, dict) or set(rating) != RATING_FIELDS:
            errors.append(f"{label} must contain {sorted(RATING_FIELDS)}")
            continue
        if not all(nonempty(rating[field]) for field in ("scenario_id", "reviewer_id", "dimension", "evidence")):
            errors.append(f"{label} requires scenario, reviewer, dimension, and evidence")
            continue
        if rating["rating"] not in ALLOWED_RATINGS:
            errors.append(f"unsupported rating in {label}: {rating['rating']}")
            continue
        if rating["confidence"] not in ALLOWED_CONFIDENCE:
            errors.append(f"unsupported confidence in {label}: {rating['confidence']}")
            continue
        unique_key = (rating["scenario_id"], rating["dimension"], rating["reviewer_id"])
        if unique_key in seen:
            errors.append(f"duplicate reviewer rating: {unique_key}")
            continue
        seen.add(unique_key)
        grouped.setdefault((rating["scenario_id"], rating["dimension"]), []).append(rating)

    if errors:
        return errors, empty_summary

    pair_count = 0
    exact_count = 0
    numeric_count = 0
    within_one_count = 0
    distance_total = 0
    no_observation_conflicts = 0
    veto_conflicts = 0
    groups_without_two = 0

    for group in grouped.values():
        if len(group) < 2:
            groups_without_two += 1
            continue
        for left, right in itertools.combinations(group, 2):
            pair_count += 1
            left_rating = left["rating"]
            right_rating = right["rating"]
            if left_rating == right_rating:
                exact_count += 1
            if "N/O" in {left_rating, right_rating}:
                if left_rating != right_rating:
                    no_observation_conflicts += 1
                continue
            left_number = int(left_rating)
            right_number = int(right_rating)
            gap = abs(left_number - right_number)
            numeric_count += 1
            distance_total += gap
            if gap <= 1:
                within_one_count += 1
            if min(left_number, right_number) == 1 and max(left_number, right_number) >= 3:
                veto_conflicts += 1

    summary = {
        "rating_pairs": pair_count,
        "exact_agreement_pairs": exact_count,
        "numeric_pairs": numeric_count,
        "within_one_numeric_pairs": within_one_count,
        "mean_absolute_numeric_gap": (
            round(distance_total / numeric_count, 3) if numeric_count else None
        ),
        "no_observation_conflicts": no_observation_conflicts,
        "veto_risk_conflicts": veto_conflicts,
        "groups_without_two_reviewers": groups_without_two,
    }
    return errors, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Privacy-safe calibration-run JSON")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Calibration summary failed: {exc}", file=sys.stderr)
        return 1
    errors, summary = summarize(payload)
    if errors:
        print("Calibration summary failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for key, value in summary.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
