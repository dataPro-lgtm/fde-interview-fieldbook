#!/usr/bin/env python3
"""Render Mermaid blocks from all or changed Markdown files."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MERMAID_CLI_VERSION = "11.12.0"
MERMAID_START = re.compile(r"^\s*```mermaid\s*$")
FENCE_END = re.compile(r"^\s*```\s*$")
VALIDATOR_DEPENDENCIES = {
    ".github/workflows/content-quality.yml",
    "scripts/validate_mermaid.py",
}


@dataclass(frozen=True)
class MermaidBlock:
    source: Path
    line: int
    content: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--all", action="store_true", help="validate every Markdown file")
    selection.add_argument("--base", help="validate Markdown changed between this Git ref and HEAD")
    selection.add_argument("--files", nargs="+", help="validate the listed repository-relative Markdown files")
    parser.add_argument("--timeout", type=int, default=60, help="seconds allowed per diagram")
    parser.add_argument(
        "--no-browser-sandbox",
        action="store_true",
        help="disable the Chromium sandbox in an already isolated CI runner",
    )
    return parser.parse_args()


def repository_path(raw: str) -> Path:
    path = (ROOT / raw).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {raw}") from exc
    if path.suffix.lower() != ".md":
        raise ValueError(f"Mermaid source is not Markdown: {raw}")
    if not path.is_file():
        raise ValueError(f"Markdown file does not exist: {raw}")
    return path


def changed_markdown(base: str) -> list[Path]:
    if not base or set(base) == {"0"}:
        return sorted(ROOT.rglob("*.md"))
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"cannot determine changed Markdown from {base}: {result.stderr.strip()}")
    changed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    if changed & VALIDATOR_DEPENDENCIES:
        return sorted(ROOT.rglob("*.md"))
    return [repository_path(line) for line in sorted(changed) if line.lower().endswith(".md")]


def selected_markdown(args: argparse.Namespace) -> list[Path]:
    if args.files:
        return sorted({repository_path(raw) for raw in args.files})
    if args.base:
        return changed_markdown(args.base)
    return sorted(ROOT.rglob("*.md"))


def extract_blocks(path: Path) -> list[MermaidBlock]:
    blocks: list[MermaidBlock] = []
    start_line: int | None = None
    content: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if start_line is None and MERMAID_START.match(line):
            start_line = line_number
            content = []
            continue
        if start_line is not None and FENCE_END.match(line):
            diagram = "\n".join(content).strip()
            if not diagram:
                raise ValueError(f"empty Mermaid block: {path.relative_to(ROOT)}:{start_line}")
            blocks.append(MermaidBlock(path, start_line, diagram + "\n"))
            start_line = None
            content = []
            continue
        if start_line is not None:
            content.append(line)
    if start_line is not None:
        raise ValueError(f"unterminated Mermaid block: {path.relative_to(ROOT)}:{start_line}")
    return blocks


def renderer_command(input_path: Path, output_path: Path, puppeteer_config: Path | None = None) -> list[str]:
    command = [
        "npx",
        "--yes",
        f"@mermaid-js/mermaid-cli@{MERMAID_CLI_VERSION}",
        "-i",
        str(input_path),
        "-o",
        str(output_path),
        "-b",
        "transparent",
    ]
    if puppeteer_config is not None:
        command.extend(["-p", str(puppeteer_config)])
    return command


def render_block(
    block: MermaidBlock,
    workdir: Path,
    index: int,
    timeout: int,
    puppeteer_config: Path | None = None,
) -> str | None:
    source_label = block.source.relative_to(ROOT).as_posix()
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", source_label).strip("-")
    input_path = workdir / f"{stem}-{index}.mmd"
    output_path = workdir / f"{stem}-{index}.svg"
    input_path.write_text(block.content, encoding="utf-8")
    command = renderer_command(input_path, output_path, puppeteer_config)
    try:
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return f"render timed out after {timeout}s: {source_label}:{block.line}"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        return f"render failed: {source_label}:{block.line}\n{detail}"
    if not output_path.is_file() or output_path.stat().st_size == 0:
        return f"renderer produced no SVG: {source_label}:{block.line}"
    return None


def main() -> int:
    args = parse_args()
    try:
        markdown_files = selected_markdown(args)
        blocks = [block for path in markdown_files for block in extract_blocks(path)]
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Mermaid validation failed:\n- {exc}")
        return 1

    if not blocks:
        print(f"Mermaid validation passed: no diagrams in {len(markdown_files)} selected Markdown files.")
        return 0

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="fde-mermaid-") as temporary:
        workdir = Path(temporary)
        puppeteer_config: Path | None = None
        if args.no_browser_sandbox:
            puppeteer_config = workdir / "puppeteer-ci.json"
            puppeteer_config.write_text('{"args":["--no-sandbox"]}\n', encoding="utf-8")
        for index, block in enumerate(blocks, start=1):
            failure = render_block(block, workdir, index, args.timeout, puppeteer_config)
            if failure:
                failures.append(failure)

    if failures:
        print("Mermaid validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        f"Mermaid validation passed: {len(blocks)} diagrams in "
        f"{len(markdown_files)} selected Markdown files (CLI {MERMAID_CLI_VERSION})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
