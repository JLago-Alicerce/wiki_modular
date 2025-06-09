#!/usr/bin/env python
"""Elimina archivos .md de wiki/ que no estén enlazados en _sidebar.md."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
SIDEBAR = WIKI_DIR / "_sidebar.md"


def obtener_links() -> set[str]:
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
    files = set()
    for p in WIKI_DIR.rglob("*.md"):
        if p.name == "README.md":
            continue
        files.add(str(p.relative_to(WIKI_DIR)).replace("\\", "/"))
    return files


def main() -> None:
    links = obtener_links()
    files = obtener_archivos()
    orphans = [f for f in files if f not in links]
    for rel in orphans:
        path = WIKI_DIR / rel
        path.unlink(missing_ok=True)
        print(f"Removed {rel}")
    print(f"Huérfanos eliminados: {len(orphans)}")


if __name__ == "__main__":
    main()
