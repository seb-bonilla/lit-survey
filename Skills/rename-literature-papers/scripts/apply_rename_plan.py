"""Validate and apply paired PDF/Markdown renames without moving directories."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path, PureWindowsPath


SAFE_STEM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
REQUIRED_COLUMNS = {"pdf_relative", "markdown_name", "new_stem"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def load_plan(plan_file: Path) -> list[dict[str, str]]:
    with plan_file.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
            raise ValueError("plan must contain pdf_relative, markdown_name, and new_stem")
        return list(reader)


def filesystem_path(path: Path) -> Path:
    """Use Windows extended-length paths without changing logical locations."""
    if os.name == "nt":
        resolved = str(path.resolve(strict=False))
        if not resolved.startswith("\\\\?\\"):
            return Path("\\\\?\\" + resolved)
    return path


def main() -> int:
    args = parse_args()
    folder = args.folder.resolve()
    markdown_dir = folder / "markdown"
    rows = load_plan(args.plan)
    prepared: list[tuple[Path, Path, Path, Path, dict[str, str]]] = []
    errors: list[str] = []
    destinations: set[str] = set()

    for index, row in enumerate(rows, 2):
        pdf_source = folder / PureWindowsPath(row["pdf_relative"])
        md_source = markdown_dir / row["markdown_name"]
        stem = row["new_stem"].strip()
        pdf_target = pdf_source.with_name(stem + ".pdf")
        md_target = md_source.with_name(stem + ".md")

        if not inside(pdf_source, folder) or not inside(md_source, markdown_dir):
            errors.append(f"row {index}: source escapes its permitted directory")
        if pdf_source.parent == markdown_dir or md_source.parent != markdown_dir:
            errors.append(f"row {index}: invalid source location")
        if not filesystem_path(pdf_source).is_file() or not filesystem_path(md_source).is_file():
            errors.append(f"row {index}: missing source pair")
        if not SAFE_STEM.fullmatch(stem):
            errors.append(f"row {index}: unsafe new stem {stem!r}")
        if len(stem) > 170:
            errors.append(f"row {index}: new stem is longer than 170 characters")
        for target in (pdf_target, md_target):
            key = str(target).casefold()
            if key in destinations:
                errors.append(f"row {index}: duplicate target {target}")
            destinations.add(key)
            if filesystem_path(target).exists() and target != pdf_source and target != md_source:
                errors.append(f"row {index}: target already exists {target}")
        prepared.append((pdf_source, md_source, pdf_target, md_target, row))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    action = "RENAME" if args.apply else "WOULD RENAME"
    for pdf_source, md_source, pdf_target, md_target, _ in prepared:
        print(f"{action}: {pdf_source.relative_to(folder)} -> {pdf_target.name}")
        print(f"{action}: markdown/{md_source.name} -> markdown/{md_target.name}")

    if not args.apply:
        print(f"Validated {len(prepared)} pair(s); no files changed")
        return 0

    failed = 0
    for pdf_source, md_source, pdf_target, md_target, row in prepared:
        try:
            filesystem_path(pdf_source).rename(filesystem_path(pdf_target))
            try:
                filesystem_path(md_source).rename(filesystem_path(md_target))
            except Exception:
                filesystem_path(pdf_target).rename(filesystem_path(pdf_source))
                raise
        except Exception as exc:
            failed += 1
            print(
                f"FAILED: {pdf_source.relative_to(folder)}: "
                f"{type(exc).__name__}: {exc}",
                file=sys.stderr,
            )

    print(f"Completed: {len(prepared) - failed}; failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
