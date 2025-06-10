#!/usr/bin/env python
"""Verifica coherencia entre los enlaces de _sidebar.md y los archivos en wiki/."""

import re
import sys
from pathlib import Path

from utils.entorno import ROOT_DIR, WIKI_DIR

ROOT = ROOT_DIR
SIDEBAR = WIKI_DIR / "_sidebar.md"


def obtener_links() -> list[str]:
    pat = re.compile(r"\(([^)]+\.md)\)")
    links = []
    for line in SIDEBAR.read_text(encoding="utf-8").splitlines():
        m = pat.search(line)
        if m:
            links.append(m.group(1).lstrip("/"))
    return links


def obtener_archivos() -> list[str]:
    files = []
    for p in WIKI_DIR.rglob("*.md"):
        if p.name == "README.md":
            continue
        files.append(str(p.relative_to(WIKI_DIR)).replace("\\", "/"))
    return files


def main() -> int:
    if not SIDEBAR.exists():
        print(
            "No se encontró _sidebar.md; ejecute generar_sidebar.py primero",
            file=sys.stderr,
        )
        return 1

    links = obtener_links()
    files = obtener_archivos()

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
