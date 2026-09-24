"""Shared three-column storage format for cheatsheet command entries."""

from __future__ import annotations

from dataclasses import dataclass


EMPTY_DESCRIPTION = "-"


@dataclass(frozen=True)
class Entry:
    name: str
    command: str
    description: str


def parse_entry(line: str) -> Entry:
    """Read a tab-separated entry, falling back to the previous Markdown format."""
    fields = line.split("\t")
    if len(fields) == 3:
        name, command, description = (field.strip() for field in fields)
        return Entry(name, command, "" if description == EMPTY_DESCRIPTION else description)

    command, separator, description = line.partition("  # ")
    command = command.strip()
    return Entry(command, command, description.strip() if separator else "")


def format_entry(name: str, command: str, description: str) -> str:
    """Store one entry without allowing field separators inside user input."""
    values = (name, command, description)
    if any("\t" in value or "\n" in value for value in values):
        raise ValueError("El nombre, comando y descripción no pueden contener tabulaciones ni saltos de línea")
    return "\t".join((name, command, description or EMPTY_DESCRIPTION))
