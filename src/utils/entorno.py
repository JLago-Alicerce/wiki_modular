from __future__ import annotations
import logging
import subprocess
import sys
from pathlib import Path

# Raiz del proyecto
ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "src"
SCRIPTS_DIR = SRC_DIR / "scripts"
WIKI_DIR = ROOT_DIR / "wiki"

# Alias retrocompatible
ROOT = ROOT_DIR


def add_src_to_path() -> None:
    """Asegura que :data:`SRC_DIR` está en ``sys.path``."""
    path = str(SRC_DIR)
    if path not in sys.path:
        sys.path.append(path)


def script_path(name: str) -> Path:
    """Devuelve la ruta absoluta de un script dentro de ``SCRIPTS_DIR``."""
    return SCRIPTS_DIR / name


def run(cmd: list[str]) -> None:
    """Ejecuta ``cmd`` y lanza :class:`RuntimeError` si falla."""
    logging.info("Ejecutando: %s", " ".join(map(str, cmd)))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Comando fallido: {' '.join(map(str, cmd))}")
