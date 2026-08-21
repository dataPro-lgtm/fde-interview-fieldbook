#!/usr/bin/env python3
"""Report sources whose verification date exceeds the allowed age."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-age",
        type=int,
        help="override each source's refresh_days value",
    )
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(), help="override current date")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    stale: list[tuple[int, dict[str, object]]] = []
    for source in payload["sources"]:
        checked = date.fromisoformat(str(source["last_checked"]))
        age = (args.as_of - checked).days
        maximum_age = args.max_age if args.max_age is not None else int(source["refresh_days"])
        if age > maximum_age:
            stale.append((age, source))

    print("# Source freshness report")
    print()
    print(f"As of: {args.as_of.isoformat()}")
    maximum_age_label = f"{args.max_age} days (override)" if args.max_age is not None else "per-source policy"
    print(f"Maximum age: {maximum_age_label}")
    print(f"Registered sources: {len(payload['sources'])}")
    print(f"Stale sources: {len(stale)}")
    print()

    if stale:
        print("| Age | Policy | Publisher | Source | Last checked |")
        print("|---:|---:|---|---|---|")
        for age, source in sorted(stale, reverse=True, key=lambda item: item[0]):
            policy = args.max_age if args.max_age is not None else source["refresh_days"]
            print(
                f"| {age} days | {policy} days | {source['publisher']} | "
                f"[{source['title']}]({source['url']}) | {source['last_checked']} |"
            )
        print()
        print("Re-check each source, update claims if necessary, then change last_checked in data/sources.json.")
        return 1

    print("All registered sources are within the freshness window.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
