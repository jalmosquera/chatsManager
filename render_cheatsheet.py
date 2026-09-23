#!/usr/bin/env python3
"""Render cheatsheets as colorized command and description columns."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from contextlib import nullcontext
from pathlib import Path

from rich import box
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


TOKYO_NIGHT = {
    "command": "#7aa2f7",
    "description": "#a9b1d6",
    "border": "#292e42",
    "section": "#bb9af7",
    "title": "#c0caf5",
}


def tmux_color(option: str, attribute: str) -> str | None:
    """Return a hex color from an active Tmux style option."""
    if not os.environ.get("TMUX"):
        return None

    result = subprocess.run(
        ["tmux", "show-options", "-g", option],
        capture_output=True,
        check=False,
        text=True,
    )
    match = re.search(rf"\b{attribute}=(#[0-9a-fA-F]{{6}})", result.stdout)
    return match.group(1) if match else None


def active_theme() -> dict[str, str]:
    """Use Tmux colors when available, otherwise use Tokyo Night."""
    theme = TOKYO_NIGHT.copy()
    theme["command"] = tmux_color("pane-active-border-style", "fg") or theme["command"]
    theme["description"] = tmux_color("status-style", "fg") or theme["description"]
    theme["border"] = tmux_color("window-status-current-style", "bg") or theme["border"]
    theme["section"] = tmux_color("status-left-style", "fg") or theme["section"]
    theme["title"] = tmux_color("window-status-current-style", "fg") or theme["title"]
    return theme


def command_table(lines: list[str], theme: dict[str, str]) -> Table:
    """Build a two-column table from Bash comments used as descriptions."""
    has_descriptions = any("  # " in line for line in lines)
    table = Table(
        box=box.ROUNDED,
        border_style=theme["border"],
        padding=(0, 1),
        show_header=False,
        show_lines=True,
    )
    table.add_column(style=f"bold {theme['command']}", ratio=3)
    if has_descriptions:
        table.add_column(style=theme["description"], ratio=2)

    for line in lines:
        command, separator, description = line.partition("  # ")
        if not separator or not has_descriptions:
            table.add_row(line)
            continue
        table.add_row(command.rstrip(), description.strip())

    return table


def render(path: Path, use_pager: bool) -> None:
    """Render headings, prose, and code blocks from a cheatsheet Markdown file."""
    theme = active_theme()
    console = Console(
        force_terminal=not use_pager,
        color_system="truecolor" if not use_pager else "auto",
    )
    if use_pager:
        pager = os.environ.get("PAGER", "")
        if not pager:
            os.environ["PAGER"] = "less -R"
        elif pager.split()[0].endswith("less") and "-R" not in pager and "-r" not in pager:
            os.environ["PAGER"] = f"{pager} -R"

    lines = path.read_text(encoding="utf-8").splitlines()
    prose: list[str] = []
    code_lines: list[str] = []
    in_code_block = False

    def flush_prose() -> None:
        if prose:
            console.print(Markdown("\n".join(prose)))
            prose.clear()

    pager_context = console.pager(styles=True) if use_pager else nullcontext()
    with pager_context:
        for line in lines:
            if line.startswith("```"):
                if in_code_block:
                    console.print(Align.center(command_table(code_lines, theme)))
                    code_lines.clear()
                    in_code_block = False
                else:
                    flush_prose()
                    in_code_block = True
                continue

            if in_code_block:
                code_lines.append(line)
                continue

            if line.startswith("# "):
                flush_prose()
                console.print(
                    Align.center(
                        Panel(
                            Text(line[2:], style=f"bold {theme['title']}"),
                            border_style=theme["border"],
                            padding=(0, 1),
                            expand=False,
                        )
                    )
                )
                continue

            if line.startswith("## "):
                flush_prose()
                console.print(Align.center(Text(line[3:], style=f"bold {theme['section']}")))
                continue

            if line == "---":
                flush_prose()
                continue

            prose.append(line)

        if in_code_block:
            console.print(Align.center(command_table(code_lines, theme)))
        flush_prose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a cheatsheet in the terminal")
    parser.add_argument("file", type=Path, help="Markdown cheatsheet to render")
    parser.add_argument(
        "--no-pager",
        action="store_true",
        help="Print directly instead of opening the pager",
    )
    args = parser.parse_args()

    if not args.file.is_file():
        parser.error(f"No existe el cheatsheet: {args.file}")

    render(args.file, use_pager=not args.no_pager)


if __name__ == "__main__":
    main()
