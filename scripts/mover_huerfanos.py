#!/usr/bin/env python
"""Detecta archivos Markdown huérfanos y los mueve a ``wiki/_deprecated``."""
import csv
import re
import sys
from pathlib import Path

# Permitir ejecutar el script sin instalar el paquete
sys.path.append(str(Path(__file__).resolve().parents[1]))
from wiki_modular import load_yaml, limpiar_slug

ROOT_DIR = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT_DIR / "wiki"
INDEX_FILE = ROOT_DIR / "index_PlataformaBBDD.yaml"
SIDEBAR_FILE = WIKI_DIR / "_sidebar.md"
DEPRECATED_DIR = WIKI_DIR / "_deprecated"
CSV_REPORT = ROOT_DIR / "orphaned_files.csv"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def paths_from_index(index_data):
    paths = set()
    for section in index_data.get("secciones", []):
        slug = section.get("slug", limpiar_slug(section.get("titulo", "")))
        sec_id = section.get("id")
        prefix = f"{sec_id}_" if sec_id is not None else ""
        paths.add(f"{prefix}{slug}.md")
        for sub in section.get("subtemas", []):
            sub_slug = limpiar_slug(sub)
            folder = "02_Instancias_SQL" if "sql" in sub_slug else slug
            paths.add(f"{folder}/{sub_slug}.md")
    return {p.lower() for p in paths}


def paths_from_sidebar(text: str):
    pat = re.compile(r"\(([^)]+\.md)\)")
    return {m.group(1).lstrip("/").lower() for m in pat.finditer(text)}


def collect_fs_paths():
    fs_paths = {}
    for p in WIKI_DIR.rglob("*.md"):
        rel = p.relative_to(WIKI_DIR).as_posix()
        if rel.lower() in {"readme.md", "_sidebar.md"}:
            continue
        if is_under(p, DEPRECATED_DIR):
            continue
        fs_paths[rel.lower()] = p
    return fs_paths


def move_orphans(orphan_paths):
    DEPRECATED_DIR.mkdir(exist_ok=True)
    rows = []
    for rel, p in orphan_paths.items():
        dest = DEPRECATED_DIR / p.name
        base = dest.stem
        ext = dest.suffix
        i = 1
        while dest.exists():
            dest = dest.with_name(f"{base}_{i}{ext}")
            i += 1
        p.rename(dest)
        rows.append({"file": str(p), "moved_to": str(dest)})
    return rows


def main() -> None:
    index_paths = set()
    if INDEX_FILE.exists():
        try:
            index_data = load_yaml(INDEX_FILE)
            index_paths = paths_from_index(index_data)
        except Exception as e:  # pragma: no cover - errors produce empty paths
            print(f"[WARN] No se pudo leer {INDEX_FILE}: {e}")

    sidebar_paths = set()
    if SIDEBAR_FILE.exists():
        sidebar_paths = paths_from_sidebar(SIDEBAR_FILE.read_text(encoding="utf-8"))

    referenced = index_paths | sidebar_paths
    fs_paths = collect_fs_paths()
    orphan_keys = set(fs_paths) - referenced
    orphan_paths = {k: fs_paths[k] for k in orphan_keys}

    rows = move_orphans(orphan_paths)

    with CSV_REPORT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "moved_to"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Reporte generado: {CSV_REPORT}")


if __name__ == "__main__":
    main()
