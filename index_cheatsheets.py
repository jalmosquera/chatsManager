#!/usr/bin/env python3
"""Generate fzf candidates from cheatsheet commands and descriptions."""

from __future__ import annotations

import argparse
from pathlib import Path


def field(value: str) -> str:
    """Keep fzf's tab-delimited candidate format intact."""
    return " ".join(value.replace("\t", " ").splitlines()).strip()


def index_file(path: Path) -> list[tuple[str, str, str, str, str]]:
    """Extract path, tool, section, command, and description from one cheatsheet."""
    section = "General"
    in_code_block = False
    entries: list[tuple[str, str, str, str, str]] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue

        if line.startswith("## "):
            section = field(line[3:])
            continue

        if not in_code_block or not line.strip():
            continue

        command, separator, description = line.partition("  # ")
        entries.append(
            (
                str(path),
                path.stem,
                section,
                field(command),
                field(description) if separator else "",
            )
        )

    if not entries:
        entries.append((str(path), path.stem, "General", "", ""))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Index cheatsheets for fzf")
    parser.add_argument("directory", type=Path, help="Directory that contains cheatsheets")
    parser.add_argument(
        "--query",
        default="",
        help="Case-insensitive terms that must appear in a cheatsheet entry",
    )
    args = parser.parse_args()
    terms = args.query.casefold().split()

    for path in sorted(args.directory.glob("*.md")):
        if path.name.startswith("README"):
            continue
        for entry in index_file(path):
            searchable = " ".join(entry[1:]).casefold()
            if terms and not all(term in searchable for term in terms):
                continue
            print("\t".join(entry))


if __name__ == "__main__":
    main()
