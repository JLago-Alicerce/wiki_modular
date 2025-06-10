#!/usr/bin/env python
"""Elimina archivos .md de wiki/ que no estén enlazados en _sidebar.md."""
from utils.entorno import ROOT_DIR
from utils.wiki import get_sidebar_links, list_markdown_files
from wiki_modular.config import SIDEBAR_FILE, WIKI_DIR

ROOT = ROOT_DIR


def main() -> None:
    """Elimina archivos sin referencia en ``_sidebar.md``."""
    links = set(get_sidebar_links(SIDEBAR_FILE))
    files = set(list_markdown_files(WIKI_DIR))
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
