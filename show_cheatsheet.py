#!/usr/bin/env python3
"""Launch the Rich cheatsheet renderer with its Homebrew Python environment."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def rich_python() -> Path | None:
    """Locate the Python environment that contains the Rich dependency."""
    result = subprocess.run(
        ["brew", "--prefix", "rich-cli"],
        capture_output=True,
        check=False,
        text=True,
    )
    python = Path(result.stdout.strip()) / "libexec" / "bin" / "python"
    return python if result.returncode == 0 and python.is_file() else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Open a cheatsheet with the Rich renderer")
    parser.add_argument("file", type=Path, help="Cheatsheet Markdown file")
    parser.add_argument(
        "--no-pager",
        action="store_true",
        help="Print directly instead of opening the pager",
    )
    args = parser.parse_args()

    python = rich_python()
    if python is None:
        parser.error("rich-cli no está instalado. Instalalo con: brew install rich-cli")

    renderer = Path(__file__).with_name("render_cheatsheet.py")
    command = [str(python), str(renderer), str(args.file)]
    if args.no_pager:
        command.append("--no-pager")
    subprocess.run(command, check=False)


if __name__ == "__main__":
    main()
