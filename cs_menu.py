#!/usr/bin/env python3
"""Render and select the centered Rich menu used by ``cs``."""

from __future__ import annotations

import argparse
import readline
import sys
import termios
import tty
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from rich import box
from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.text import Text


TOKYO_NIGHT = {
    "command": "#7aa2f7",
    "description": "#a9b1d6",
    "border": "#292e42",
    "section": "#bb9af7",
    "title": "#c0caf5",
}


@dataclass(frozen=True)
class MenuItem:
    kind: str
    value: str
    icon: str
    name: str
    description: str


ACTION_ITEMS = (
    MenuItem("action", "new", "󰐕", "crear", "Crear cheatsheet nuevo"),
    MenuItem("action", "add", "󰐕", "agregar", "Agregar comandos"),
    MenuItem("action", "edit", "󰏫", "editar", "Editar comandos"),
    MenuItem("action", "delete", "󰆴", "eliminar", "Eliminar comandos"),
    MenuItem("action", "alias", "󰌷", "alias", "Agregar alias vivo"),
    MenuItem("action", "find", "󰍉", "buscar", "Buscar comando o descripción"),
    MenuItem("action", "help", "󰞋", "ayuda", "Ver ayuda"),
)

CHEATSHEET_ICONS = {
    "aliases": "󰌷",
    "django": "󰌠",
    "docker": "󰡨",
    "git": "󰊢",
    "google": "󰖟",
    "nvim": "",
    "nvichad": "",
    "tmux": "",
    "warp": "󰆧",
}

MOSQUERA_SOFT_BANNER = r"""
   ███╗   ███╗ ██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗██████╗  █████╗     ███████╗ ██████╗ ███████╗████████╗
   ████╗ ████║██╔═══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔══██╗    ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝
   ██╔████╔██║██║   ██║███████╗██║   ██║██║   ██║█████╗  ██████╔╝███████║    ███████╗██║   ██║█████╗     ██║
   ██║╚██╔╝██║██║   ██║╚════██║██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗██╔══██║    ╚════██║██║   ██║██╔══╝     ██║
   ██║ ╚═╝ ██║╚██████╔╝███████║╚██████╔╝╚██████╔╝███████╗██║  ██║██║  ██║    ███████║╚██████╔╝██║        ██║
   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚═╝        ╚═╝
""".strip("\n")


def menu_items(cheatsheet_dir: Path) -> list[MenuItem]:
    """Return actions followed by the available cheatsheets."""
    cheatsheets = [
        MenuItem(
            "cheat",
            str(path),
            CHEATSHEET_ICONS.get(path.stem.casefold(), "󰈔"),
            path.stem,
            "Abrir cheatsheet",
        )
        for path in sorted(cheatsheet_dir.glob("*.md"))
        if not path.name.startswith("README")
    ]
    return [*ACTION_ITEMS, *cheatsheets]


def table(
    items: list[MenuItem], title: str, first_number: int, caption: str | None = None
) -> Table:
    """Build one numbered menu table with a fixed-width icon column."""
    menu = Table(
        title=f"[bold {TOKYO_NIGHT['title']}]{title}[/]",
        box=box.ROUNDED,
        border_style=TOKYO_NIGHT["border"],
        header_style=f"bold {TOKYO_NIGHT['section']}",
        show_lines=True,
        padding=(0, 1),
    )
    menu.add_column("Nº", justify="right", style=TOKYO_NIGHT["section"], width=3, no_wrap=True)
    menu.add_column("", justify="center", width=1, no_wrap=True)
    menu.add_column("Opción", style=f"bold {TOKYO_NIGHT['command']}")
    menu.add_column("Descripción", style=TOKYO_NIGHT["description"])

    for number, item in enumerate(items, start=first_number):
        menu.add_row(str(number), item.icon, item.name, item.description)

    if caption:
        menu.caption = caption
    return menu


def render_brand(console: Console) -> int:
    """Render a responsive Mosquera Soft banner and return its visual height."""
    banner_width = max(len(line) for line in MOSQUERA_SOFT_BANNER.splitlines())
    if console.width >= banner_width:
        console.print(Align.center(Text(MOSQUERA_SOFT_BANNER, style=f"bold {TOKYO_NIGHT['title']}")))
        height = 6
    else:
        console.print(Align.center(Text("MOSQUERA SOFT", style=f"bold {TOKYO_NIGHT['title']}")))
        height = 1

    console.print(Align.center(Text("Cheats Manager", style=f"bold {TOKYO_NIGHT['section']}")))
    return height + 2


def render(console: Console, items: list[MenuItem], message: str | None = None) -> None:
    """Clear the terminal and center the CRUD and cheatsheet tables."""
    actions = [item for item in items if item.kind == "action"]
    cheatsheets = [item for item in items if item.kind == "cheat"]
    caption = message or "/ busca · Número o nombre selecciona · Tab completa · Esc cancela"

    console.clear()
    banner_height = 8 if console.width >= max(len(line) for line in MOSQUERA_SOFT_BANNER.splitlines()) else 3
    top_padding = max((console.height - len(items) - banner_height - 15) // 2, 0)
    console.file.write("\n" * top_padding)
    render_brand(console)
    console.print()
    console.print(Align.center(table(actions, "Acciones CRUD", 1)))
    console.print()
    console.print(Align.center(table(cheatsheets, "Cheatsheets", len(actions) + 1, caption)))


def match_item(raw: str, items: list[MenuItem]) -> tuple[MenuItem | None, str | None]:
    """Resolve a number, exact name, or unique case-insensitive text match."""
    query = raw.strip().casefold()
    if not query:
        return None, "Ingresá un número o nombre."
    if query == "/":
        return next(item for item in items if item.kind == "action" and item.value == "find"), None
    if query.isdecimal():
        position = int(query) - 1
        if 0 <= position < len(items):
            return items[position], None
        return None, f"No existe la opción {raw}."

    exact_matches = [item for item in items if item.name.casefold() == query]
    if len(exact_matches) == 1:
        return exact_matches[0], None

    matches = [
        item
        for item in items
        if query in f"{item.name} {item.description}".casefold()
    ]
    if len(matches) == 1:
        return matches[0], None
    if not matches:
        return None, f"No encontré una opción para «{raw}»."
    return None, "La búsqueda coincide con varias opciones; usá Tab, más texto o su número."


def configure_completion(items: list[MenuItem]) -> None:
    """Make Tab complete names and slash open global search at the selection prompt."""
    names = sorted({item.name for item in items}, key=str.casefold)

    def complete(text: str, state: int) -> str | None:
        matches = [name for name in names if name.casefold().startswith(text.casefold())]
        return matches[state] if state < len(matches) else None

    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")


def read_selection(tty_in: TextIO, tty_out: TextIO) -> str | None:
    """Open search immediately on slash while preserving Readline for normal input."""
    attributes = termios.tcgetattr(tty_in.fileno())
    try:
        tty.setcbreak(tty_in.fileno())
        tty_out.write("\n⌕ Elegí una opción: ")
        tty_out.flush()
        first_key = tty_in.read(1)
    finally:
        termios.tcsetattr(tty_in.fileno(), termios.TCSADRAIN, attributes)

    if first_key == "/":
        tty_out.write("/\n")
        tty_out.flush()
        return "/"
    if first_key in ("\x1b", "\x03"):
        tty_out.write("\n")
        tty_out.flush()
        return None
    if first_key in ("\r", "\n"):
        tty_out.write("\n")
        tty_out.flush()
        return ""

    def seed_input() -> None:
        readline.insert_text(first_key)
        readline.redisplay()

    readline.set_startup_hook(seed_input)
    try:
        return input()
    finally:
        readline.set_startup_hook()


def prompt(tty_in: TextIO, tty_out: TextIO, items: list[MenuItem]) -> MenuItem | None:
    """Read a selection through the terminal while stdout remains machine-readable."""
    original_stdin, original_stdout = sys.stdin, sys.stdout
    sys.stdin, sys.stdout = tty_in, tty_out
    console = Console(file=tty_out, force_terminal=True, color_system="truecolor")
    configure_completion(items)
    message: str | None = None

    try:
        while True:
            render(console, items, message)
            try:
                selection = read_selection(tty_in, tty_out)
            except (EOFError, KeyboardInterrupt):
                return None
            if selection is None:
                return None
            item, message = match_item(selection, items)
            if item:
                return item
    finally:
        sys.stdin, sys.stdout = original_stdin, original_stdout


def main() -> None:
    parser = argparse.ArgumentParser(description="Centered cheatsheet menu")
    parser.add_argument("directory", type=Path, help="Cheatsheet directory")
    args = parser.parse_args()
    items = menu_items(args.directory)

    try:
        with open("/dev/tty", "r", encoding="utf-8") as tty_in, open(
            "/dev/tty", "w", encoding="utf-8"
        ) as tty_out:
            item = prompt(tty_in, tty_out, items)
    except OSError:
        parser.error("El menú interactivo requiere una terminal conectada.")

    if item:
        print(f"{item.kind}\t{item.value}")


if __name__ == "__main__":
    main()
