#!/usr/bin/env python3
"""Generate fzf candidates from cheatsheet commands and descriptions."""

from __future__ import annotations

import argparse
from pathlib import Path

from cheatsheet_format import parse_entry


def field(value: str) -> str:
    """Keep fzf's tab-delimited candidate format intact."""
    return " ".join(value.replace("\t", " ").splitlines()).strip()


def index_file(path: Path) -> list[tuple[str, str, str, str, str, str]]:
    """Extract path, tool, section, name, command, and description from one cheatsheet."""
    section = "General"
    in_code_block = False
    entries: list[tuple[str, str, str, str, str, str]] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue

        if line.startswith("## "):
            section = field(line[3:])
            continue

        if not in_code_block or not line.strip():
            continue

        entry = parse_entry(line)
        entries.append(
            (
                str(path),
                path.stem,
                section,
                field(entry.name),
                field(entry.command),
                field(entry.description),
            )
        )

    if not entries:
        entries.append((str(path), path.stem, "General", "", "", ""))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Index cheatsheets for fzf")
    parser.add_argument("directory", type=Path, help="Directory that contains cheatsheets")
    parser.add_argument(
        "--query",
        default="",
        help="Case-insensitive terms that must appear in a cheatsheet entry",
    )
    parser.add_argument("--file", type=Path, help="Search only one cheatsheet Markdown file")
    args = parser.parse_args()
    terms = args.query.casefold().split()

    paths = [args.file] if args.file else sorted(args.directory.glob("*.md"))
    for path in paths:
        if not path.is_file():
            parser.error(f"No existe el cheatsheet: {path}")
        if path.name.startswith("README"):
            continue
        for entry in index_file(path):
            searchable = " ".join(entry[1:]).casefold()
            if terms and not all(term in searchable for term in terms):
                continue
            print("\t".join(entry))


if __name__ == "__main__":
    main()
