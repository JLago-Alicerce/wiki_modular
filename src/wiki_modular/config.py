"""Carga de configuraciones para rutas del proyecto."""
from __future__ import annotations

import os
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_FILE = ROOT_DIR / "config.yaml"

# If ``WM_CONFIG`` is defined use that path, otherwise fallback to ``DEFAULT_FILE``.
CONFIG_FILE = Path(os.environ.get("WM_CONFIG", DEFAULT_FILE))

_DEFAULTS = {
    "originales_dir": "_fuentes/_originales",
    "wiki_dir": "wiki",
    "assets_dir": "wiki/assets",
    "sidebar_file": "wiki/_sidebar.md",
}


def _load(path: Path) -> dict[str, Path]:
    """Load configuration from ``path`` and merge with defaults."""
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        data = {}
    merged = {**_DEFAULTS, **data}
    return {k: Path(v) for k, v in merged.items()}


CONFIG = _load(CONFIG_FILE)
ORIGINALES_DIR: Path = CONFIG["originales_dir"]
WIKI_DIR: Path = CONFIG["wiki_dir"]
ASSETS_DIR: Path = CONFIG["assets_dir"]
SIDEBAR_FILE: Path = CONFIG["sidebar_file"]


def load_config(path: str | Path) -> None:
    """Cargar configuración desde ``path`` y actualizar constantes."""
    global CONFIG_FILE, CONFIG, ORIGINALES_DIR, WIKI_DIR, ASSETS_DIR, SIDEBAR_FILE
    CONFIG_FILE = Path(path)
    CONFIG = _load(CONFIG_FILE)
    ORIGINALES_DIR = CONFIG["originales_dir"]
    WIKI_DIR = CONFIG["wiki_dir"]
    ASSETS_DIR = CONFIG["assets_dir"]
    SIDEBAR_FILE = CONFIG["sidebar_file"]


__all__ = [
    "ORIGINALES_DIR",
    "WIKI_DIR",
    "ASSETS_DIR",
    "SIDEBAR_FILE",
    "load_config",
]
