#!/usr/bin/env python3
"""Run the v1.0 release-candidate checks through one explicit command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_COMMANDS = [
    "python3 scripts/validate_repo.py",
    "python3 scripts/validate_case_packs.py",
    "python3 scripts/validate_research_data.py",
    "python3 scripts/validate_role_playbooks.py",
    "python3 scripts/validate_learning_paths.py",
    "python3 scripts/validate_calibration.py",
    "python3 scripts/validate_parity_archive.py",
    "python3 -m unittest discover -s tests -v",
    "python3 -m py_compile scripts/*.py tests/*.py",
    "git diff --check",
    "python3 scripts/validate_release_manifest.py --check",
]
FULL_COMMANDS = [
    "npx --yes markdownlint-cli2@0.18.1 \"**/*.md\" \"#node_modules\"",
    "npx --yes markdownlint-cli2@0.23.2 \"**/*.md\" \"#node_modules\"",
    "python3 scripts/validate_mermaid.py --all --no-browser-sandbox",
]
NETWORK_COMMANDS = ["python3 scripts/check_external_links.py --timeout 12 --workers 6"]


def run(command: str) -> int:
    print(f"\n>>> {command}", flush=True)
    return subprocess.run(command, cwd=ROOT, shell=True, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run release-candidate validation.")
    parser.add_argument("--full", action="store_true", help="also lint all Markdown and render all Mermaid diagrams")
    parser.add_argument("--network", action="store_true", help="also check every public external link")
    parser.add_argument("--require-clean", action="store_true", help="fail unless the Git worktree and index are clean")
    args = parser.parse_args()

    commands = list(CORE_COMMANDS)
    if args.full:
        commands.extend(FULL_COMMANDS)
    if args.network:
        commands.extend(NETWORK_COMMANDS)
    for command in commands:
        if run(command) != 0:
            print(f"\nRelease verification stopped at: {command}", file=sys.stderr)
            return 1

    if args.require_clean:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print("\nRelease verification failed: Git worktree or index is not clean.", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            return 1

    mode = "full" if args.full else "core"
    network = " with network audit" if args.network else ""
    print(f"\nRelease verification passed: {mode}{network}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
