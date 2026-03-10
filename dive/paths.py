#!/usr/bin/env python3
"""Centralized project path helpers."""

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent        # dive/
REPO_ROOT = PACKAGE_ROOT.parent                       # DIVE/
DATA_DIR = REPO_ROOT / "data"
TOOLS_DIR = REPO_ROOT / "tools"
TOOLS_CONFIG_DIR = TOOLS_DIR / "configs"


def ensure_tools_on_path() -> None:
    """Ensure local tools package is importable."""
    path_str = str(TOOLS_DIR)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


def data_path(*parts: str) -> Path:
    """Build absolute path under data/."""
    return DATA_DIR.joinpath(*parts)
