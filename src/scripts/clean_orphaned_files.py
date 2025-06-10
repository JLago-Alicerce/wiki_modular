#!/usr/bin/env python
"""Elimina archivos .md de wiki/ que no estén enlazados en _sidebar.md."""
import re
from pathlib import Path

from utils.entorno import ROOT_DIR, WIKI_DIR

ROOT = ROOT_DIR
SIDEBAR = WIKI_DIR / "_sidebar.md"


def obtener_links() -> set[str]:
    """Devuelve los enlaces Markdown listados en ``_sidebar.md``."""
    if not SIDEBAR.exists():
        return set()
    pat = re.compile(r"\(([^)]+\.md)\)")
    links = set()
    for line in SIDEBAR.read_text(encoding="utf-8").splitlines():
        m = pat.search(line)
        if m:
            links.add(m.group(1).lstrip("/"))
    return links


def obtener_archivos() -> set[str]:
    """Enumera todos los archivos Markdown reales en ``wiki/``."""
    files = set()
    for p in WIKI_DIR.rglob("*.md"):
        if p.name == "README.md":
            continue
        files.add(str(p.relative_to(WIKI_DIR)).replace("\\", "/"))
    return files


def main() -> None:
    """Elimina archivos sin referencia en ``_sidebar.md``."""
    links = obtener_links()
    files = obtener_archivos()
    # Identificar rutas presentes en el sistema de archivos pero no en el
    # sidebar para considerarlas huérfanas.
    orphans = [f for f in files if f not in links]
    for rel in orphans:
        path = WIKI_DIR / rel
        path.unlink(missing_ok=True)
        print(f"Removed {rel}")
    print(f"Huérfanos eliminados: {len(orphans)}")


if __name__ == "__main__":
    main()
