#!/usr/bin/env python3
"""Validate quarterly role-radar snapshots and technology baselines."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROLE_RADAR_DIR = ROOT / "data/role-radar"
BASELINE_PATH = ROOT / "data/technology-baselines.json"
REQUIRED_TECHNOLOGIES = {"MCP", "A2A", "OpenTelemetry GenAI", "OWASP Agentic Security"}
BASELINE_STATUSES = {"current_release", "stable_release", "evolving_specification", "current_guidance"}


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {display_path(path)}: {exc}")
        return None


def registered_source_ids(errors: list[str]) -> set[str]:
    payload = load_json(ROOT / "data/sources.json", errors)
    if not isinstance(payload, dict) or not isinstance(payload.get("sources"), list):
        return set()
    return {
        str(source.get("id"))
        for source in payload["sources"]
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }


def nonempty_strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def parse_date(value: object, label: str, errors: list[str]) -> date | None:
    try:
        parsed = date.fromisoformat(str(value))
    except ValueError:
        errors.append(f"invalid date for {label}: {value}")
        return None
    if parsed > date.today():
        errors.append(f"future date for {label}: {parsed.isoformat()}")
    return parsed


def validate_role_snapshot(path: Path, sources: set[str], errors: list[str]) -> str | None:
    payload = load_json(path, errors)
    relative = display_path(path)
    if not isinstance(payload, dict):
        return None
    if payload.get("schema_version") != "1.0":
        errors.append(f"role radar schema_version must be 1.0: {relative}")

    snapshot_id = payload.get("snapshot_id")
    if not isinstance(snapshot_id, str):
        errors.append(f"role radar snapshot_id is required: {relative}")
        return None
    if path.stem != snapshot_id:
        errors.append(f"role radar filename must match snapshot_id: {relative}")
    as_of = parse_date(payload.get("as_of"), f"{snapshot_id}.as_of", errors)
    if as_of is not None:
        expected = f"{as_of.year}-Q{((as_of.month - 1) // 3) + 1}"
        if snapshot_id != expected:
            errors.append(f"role radar quarter mismatch: {snapshot_id} should be {expected}")

    methodology = payload.get("methodology")
    if not isinstance(methodology, dict) or not nonempty_strings(methodology.get("limitations")):
        errors.append(f"role radar methodology requires limitations: {snapshot_id}")
    elif not isinstance(methodology.get("unit"), str) or not methodology["unit"].strip():
        errors.append(f"role radar methodology requires unit: {snapshot_id}")
    elif not isinstance(methodology.get("counting_rule"), str) or not methodology["counting_rule"].strip():
        errors.append(f"role radar methodology requires counting_rule: {snapshot_id}")

    observations = payload.get("observations")
    if not isinstance(observations, list) or not observations:
        errors.append(f"role radar requires observations: {snapshot_id}")
        return snapshot_id

    observation_ids: set[str] = set()
    for index, observation in enumerate(observations):
        label = f"{snapshot_id}.observations[{index}]"
        if not isinstance(observation, dict):
            errors.append(f"role radar observation must be an object: {label}")
            continue
        observation_id = observation.get("id")
        if not isinstance(observation_id, str) or not observation_id:
            errors.append(f"role radar observation id is required: {label}")
        elif observation_id in observation_ids:
            errors.append(f"duplicate role radar observation id: {observation_id}")
        else:
            observation_ids.add(observation_id)
        source_id = observation.get("source_id")
        if source_id not in sources:
            errors.append(f"unregistered role radar source: {source_id} ({label})")
        for field in ("employer", "role_family"):
            if not isinstance(observation.get(field), str) or not observation[field].strip():
                errors.append(f"role radar observation requires {field}: {label}")
        job_locations = observation.get("job_locations")
        if not isinstance(job_locations, list) or not job_locations:
            errors.append(f"role radar observation requires job_locations: {label}")
        else:
            location_regions: set[str] = set()
            for location_index, location in enumerate(job_locations):
                location_label = f"{label}.job_locations[{location_index}]"
                if not isinstance(location, dict):
                    errors.append(f"job location must be an object: {location_label}")
                    continue
                region = location.get("region")
                if not isinstance(region, str) or not region.strip():
                    errors.append(f"job location region is required: {location_label}")
                elif region in location_regions:
                    errors.append(f"duplicate job location region in {label}: {region}")
                else:
                    location_regions.add(region)
                if not nonempty_strings(location.get("locations")):
                    errors.append(f"job location requires locations: {location_label}")
        if not nonempty_strings(observation.get("archetypes")):
            errors.append(f"role radar observation requires archetypes: {label}")
        if not nonempty_strings(observation.get("signals")):
            errors.append(f"role radar observation requires signals: {label}")
        if not isinstance(observation.get("scope_note"), str) or not observation["scope_note"].strip():
            errors.append(f"role radar observation requires scope_note: {label}")

    geography_views = payload.get("geography_views")
    if not isinstance(geography_views, list) or len(geography_views) < 3:
        errors.append(f"role radar requires at least three geography views: {snapshot_id}")
        return snapshot_id
    regions: set[str] = set()
    for index, view in enumerate(geography_views):
        label = f"{snapshot_id}.geography_views[{index}]"
        if not isinstance(view, dict):
            errors.append(f"geography view must be an object: {label}")
            continue
        region = view.get("region")
        if not isinstance(region, str) or not region:
            errors.append(f"geography view region is required: {label}")
        elif region in regions:
            errors.append(f"duplicate geography region: {region}")
        else:
            regions.add(region)
        evidence_ids = view.get("evidence_ids")
        if not nonempty_strings(evidence_ids):
            errors.append(f"geography view requires evidence_ids: {label}")
        else:
            missing = set(evidence_ids) - observation_ids
            if missing:
                errors.append(f"unknown geography evidence ids in {label}: {sorted(missing)}")
        for field in ("observed_signals", "candidate_implications"):
            if not nonempty_strings(view.get(field)):
                errors.append(f"geography view requires {field}: {label}")
        if not isinstance(view.get("limitations"), str) or not view["limitations"].strip():
            errors.append(f"geography view requires limitations: {label}")
    return snapshot_id


def validate_technology_baselines(sources: set[str], errors: list[str]) -> int:
    payload = load_json(BASELINE_PATH, errors)
    if not isinstance(payload, dict):
        return 0
    if payload.get("schema_version") != "1.0":
        errors.append("technology-baselines.json schema_version must be 1.0")
    parse_date(payload.get("as_of"), "technology-baselines.as_of", errors)
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("technology-baselines.json requires entries")
        return 0

    technologies: set[str] = set()
    ids: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"technology-baselines.entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"technology baseline must be an object: {label}")
            continue
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            errors.append(f"technology baseline id is required: {label}")
        elif entry_id in ids:
            errors.append(f"duplicate technology baseline id: {entry_id}")
        else:
            ids.add(entry_id)
        technology = entry.get("technology")
        if not isinstance(technology, str) or not technology:
            errors.append(f"technology baseline name is required: {label}")
        elif technology in technologies:
            errors.append(f"duplicate technology baseline: {technology}")
        else:
            technologies.add(technology)
        if entry.get("status") not in BASELINE_STATUSES:
            errors.append(f"invalid technology baseline status: {entry.get('status')} ({label})")
        if not isinstance(entry.get("baseline"), str) or not entry["baseline"].strip():
            errors.append(f"technology baseline descriptor is required: {label}")
        source_ids = entry.get("source_ids")
        if not nonempty_strings(source_ids):
            errors.append(f"technology baseline requires source_ids: {label}")
        else:
            missing = set(source_ids) - sources
            if missing:
                errors.append(f"unregistered technology baseline sources in {label}: {sorted(missing)}")
        for field in ("changes", "production_implications", "watch_items"):
            if not nonempty_strings(entry.get(field)):
                errors.append(f"technology baseline requires {field}: {label}")
        change_log = entry.get("change_log")
        if not isinstance(change_log, list) or not change_log:
            errors.append(f"technology baseline requires change_log: {label}")
        else:
            previous_change_date: date | None = None
            for change_index, change in enumerate(change_log):
                change_label = f"{label}.change_log[{change_index}]"
                if not isinstance(change, dict):
                    errors.append(f"technology change must be an object: {change_label}")
                    continue
                change_date = parse_date(change.get("date"), f"{change_label}.date", errors)
                if change_date is not None and previous_change_date is not None and change_date < previous_change_date:
                    errors.append(f"technology change log must be chronological: {change_label}")
                if change_date is not None:
                    previous_change_date = change_date
                if not isinstance(change.get("kind"), str) or not change["kind"].strip():
                    errors.append(f"technology change kind is required: {change_label}")
                if not isinstance(change.get("summary"), str) or not change["summary"].strip():
                    errors.append(f"technology change summary is required: {change_label}")

    missing_technologies = REQUIRED_TECHNOLOGIES - technologies
    if missing_technologies:
        errors.append(f"missing required technology baselines: {sorted(missing_technologies)}")
    return len(entries)


def validate_all() -> tuple[list[str], int, int]:
    errors: list[str] = []
    sources = registered_source_ids(errors)
    snapshot_ids: set[str] = set()
    snapshot_paths = sorted(ROLE_RADAR_DIR.glob("*.json"))
    if not snapshot_paths:
        errors.append("no quarterly role-radar snapshots found")
    for path in snapshot_paths:
        snapshot_id = validate_role_snapshot(path, sources, errors)
        if snapshot_id in snapshot_ids:
            errors.append(f"duplicate role radar snapshot_id: {snapshot_id}")
        elif snapshot_id:
            snapshot_ids.add(snapshot_id)
    baseline_count = validate_technology_baselines(sources, errors)
    return errors, len(snapshot_ids), baseline_count


def main() -> int:
    errors, snapshot_count, baseline_count = validate_all()
    if errors:
        print("Research-data validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Research-data validation passed: {snapshot_count} quarterly snapshot(s), "
        f"{baseline_count} technology baseline(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
