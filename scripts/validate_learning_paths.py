#!/usr/bin/env python3
"""Validate guided-practice learning paths without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/learning-paths.json"
REQUIRED_PATHS = {
    "interview-in-7-days": {"days": 7, "minimum_sessions": 7},
    "role-targeting-14-days": {"days": 14, "minimum_sessions": 10},
    "field-ready-30-days": {"days": 30, "minimum_sessions": 12},
}
PATH_FIELDS = {
    "id",
    "title",
    "title_zh",
    "audience",
    "time_budget_days",
    "entry_evidence",
    "sessions",
    "exit_evidence",
    "limits",
}
SESSION_FIELDS = {
    "order",
    "title",
    "goal",
    "inputs",
    "output",
    "completion_checks",
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


def safe_input(relative: object, label: str, errors: list[str]) -> None:
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


def validate_session(
    session: object,
    path_id: str,
    index: int,
    errors: list[str],
) -> int | None:
    label = f"learning-paths.{path_id}.sessions[{index}]"
    if not isinstance(session, dict):
        errors.append(f"session must be an object: {label}")
        return None
    missing = SESSION_FIELDS - session.keys()
    if missing:
        errors.append(f"session missing fields in {label}: {sorted(missing)}")
        return None

    order = session["order"]
    if not isinstance(order, int) or isinstance(order, bool) or order < 1:
        errors.append(f"session order must be a positive integer: {label}")
        order = None

    for field in ("title", "goal", "output"):
        if not nonempty_string(session[field]):
            errors.append(f"session {field} is required: {label}")

    inputs = session["inputs"]
    if not nonempty_strings(inputs):
        errors.append(f"session inputs require at least one path: {label}")
    else:
        if len(inputs) != len(set(inputs)):
            errors.append(f"session inputs must be unique: {label}")
        for input_index, relative in enumerate(inputs):
            safe_input(relative, f"{label}.inputs[{input_index}]", errors)

    checks = session["completion_checks"]
    if not nonempty_strings(checks, minimum=2):
        errors.append(f"session needs at least two completion checks: {label}")
    elif len(checks) != len(set(checks)):
        errors.append(f"session completion checks must be unique: {label}")

    return order


def validate_path(path: object, path_ids: set[str], errors: list[str]) -> None:
    if not isinstance(path, dict):
        errors.append("learning path entry must be an object")
        return
    missing = PATH_FIELDS - path.keys()
    if missing:
        errors.append(f"learning path missing fields: {sorted(missing)}")
        return

    path_id = path["id"]
    if not isinstance(path_id, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", path_id
    ):
        errors.append(f"invalid learning path id: {path_id}")
        return
    if path_id in path_ids:
        errors.append(f"duplicate learning path id: {path_id}")
    path_ids.add(path_id)
    label = f"learning-paths.{path_id}"

    for field in ("title", "title_zh", "audience"):
        if not nonempty_string(path[field]):
            errors.append(f"learning path {field} is required: {path_id}")

    expected = REQUIRED_PATHS.get(path_id)
    days = path["time_budget_days"]
    if not isinstance(days, int) or isinstance(days, bool) or days < 1:
        errors.append(f"learning path time_budget_days must be positive: {path_id}")
    elif expected and days != expected["days"]:
        errors.append(
            f"learning path time budget must match its contract: {path_id} -> {days}"
        )

    for field, minimum in (("entry_evidence", 2), ("exit_evidence", 2), ("limits", 3)):
        if not nonempty_strings(path[field], minimum=minimum):
            errors.append(
                f"learning path {field} needs at least {minimum} entries: {path_id}"
            )

    sessions = path["sessions"]
    minimum_sessions = expected["minimum_sessions"] if expected else 3
    if not isinstance(sessions, list) or len(sessions) < minimum_sessions:
        errors.append(
            f"learning path needs at least {minimum_sessions} sessions: {path_id}"
        )
        return

    orders: list[int] = []
    for index, session in enumerate(sessions):
        order = validate_session(session, path_id, index, errors)
        if order is not None:
            orders.append(order)
    expected_orders = list(range(1, len(sessions) + 1))
    if orders != expected_orders:
        errors.append(
            f"learning path session order must be contiguous and listed in order: "
            f"{path_id} -> {orders}"
        )


def validate_all(manifest_path: Path = MANIFEST) -> tuple[list[str], int, int]:
    errors: list[str] = []
    payload = load_json(manifest_path, errors)
    if not isinstance(payload, dict):
        return errors, 0, 0
    if payload.get("schema_version") != "1.0":
        errors.append("learning-paths.json schema_version must be 1.0")
    try:
        as_of = date.fromisoformat(str(payload.get("as_of")))
        if as_of > date.today():
            errors.append(f"learning-paths.json as_of is in the future: {as_of.isoformat()}")
    except ValueError:
        errors.append(f"invalid learning-paths.json as_of date: {payload.get('as_of')}")
    if not nonempty_string(payload.get("scope_note")):
        errors.append("learning-paths.json requires a scope_note")

    paths = payload.get("paths")
    if not isinstance(paths, list) or not paths:
        errors.append("learning-paths.json requires a non-empty paths list")
        return errors, 0, 0

    path_ids: set[str] = set()
    for path in paths:
        validate_path(path, path_ids, errors)

    missing_paths = set(REQUIRED_PATHS) - path_ids
    if missing_paths:
        errors.append(f"missing required learning paths: {sorted(missing_paths)}")

    session_count = sum(
        len(path.get("sessions", []))
        for path in paths
        if isinstance(path, dict) and isinstance(path.get("sessions"), list)
    )
    return errors, len(paths), session_count


def main() -> int:
    errors, path_count, session_count = validate_all()
    if errors:
        print("Learning-path validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Learning-path validation passed: {path_count} paths, "
        f"{session_count} ordered sessions with completion evidence."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
