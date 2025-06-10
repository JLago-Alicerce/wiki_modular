"""Carga de configuraciones para rutas del proyecto."""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = ROOT_DIR / "config.yaml"

_DEFAULTS = {
    "originales_dir": "_fuentes/_originales",
    "wiki_dir": "wiki",
    "assets_dir": "wiki/assets",
}


def _load() -> dict[str, Path]:
    if CONFIG_FILE.exists():
        data = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
    else:
        data = {}
    merged = {**_DEFAULTS, **data}
    return {k: Path(v) for k, v in merged.items()}


CONFIG = _load()
ORIGINALES_DIR: Path = CONFIG["originales_dir"]
WIKI_DIR: Path = CONFIG["wiki_dir"]
ASSETS_DIR: Path = CONFIG["assets_dir"]

__all__ = [
    "ORIGINALES_DIR",
    "WIKI_DIR",
    "ASSETS_DIR",
]
