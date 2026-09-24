"""Resolve installation paths shared by the cheatsheet management scripts."""

from __future__ import annotations

import os
from pathlib import Path


def cheatsheets_dir() -> Path:
    return Path(os.environ.get("CS_CHEATS_DIR", "~/.cheatsheets")).expanduser()


def fish_aliases_file() -> Path:
    return Path(
        os.environ.get(
            "CS_FISH_ALIASES_FILE",
            "~/.config/fish/conf.d/cheats_manager_aliases.fish",
        )
    ).expanduser()
