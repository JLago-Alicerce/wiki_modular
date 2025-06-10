#!/usr/bin/env python
"""Verifica coherencia entre los enlaces de _sidebar.md y los archivos en wiki/."""

import sys

from utils.entorno import ROOT_DIR
from utils.wiki import get_sidebar_links, list_markdown_files
from wiki_modular.config import SIDEBAR_FILE, WIKI_DIR

ROOT = ROOT_DIR
SIDEBAR = SIDEBAR_FILE


def main() -> int:
    """Verifica que los enlaces del sidebar coincidan con el filesystem."""
    if not SIDEBAR.exists():
        print(
            "No se encontró _sidebar.md; ejecute generar_sidebar.py primero",
            file=sys.stderr,
        )
        return 1

    links = get_sidebar_links(SIDEBAR)
    files = list_markdown_files(WIKI_DIR)

    faltantes = [l for l in links if l not in files]
    huerfanos = [f for f in files if f not in links]

    for l in faltantes:
        print(f"NO_EXISTE | {l}")
    for f in huerfanos:
        print(f"SIN_ENLACE | {f}")

    if faltantes or huerfanos:
        print(f"❌ Faltantes: {len(faltantes)} | Huérfanos: {len(huerfanos)}")
        return 1
    print("✅ Sidebar y sistema de archivos coinciden")
    return 0


if __name__ == "__main__":
    sys.exit(main())
