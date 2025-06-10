#!/usr/bin/env python
"""Valida enlaces del sidebar y referencias internas en la wiki."""

import csv
import re
import sys
from pathlib import Path
from typing import Dict, List

from wiki_modular import limpiar_slug
from utils.entorno import ROOT_DIR, WIKI_DIR

ROOT = ROOT_DIR
SIDEBAR = WIKI_DIR / "_sidebar.md"


def slugify_path(path: str) -> str:
    """Normaliza ``path`` a un slug comparable."""
    path = path.lstrip("/")
    parts = []
    for part in Path(path).parts:
        if part.lower().endswith(".md"):
            parts.append(limpiar_slug(part[:-3]) + ".md")
        else:
            parts.append(limpiar_slug(part))
    return "/".join(parts)


def build_fs_index() -> Dict[str, str]:
    """Mapea rutas de la wiki normalizadas a su forma real."""
    index: Dict[str, str] = {}
    for p in WIKI_DIR.rglob("*.md"):
        if p.name.lower() == "readme.md":
            continue
        rel = str(p.relative_to(WIKI_DIR)).replace("\\", "/")
        index[slugify_path(rel)] = rel
    return index


def parse_sidebar_links() -> List[str]:
    pat = re.compile(r"\(([^)]+\.md)\)")
    links = []
    for line in SIDEBAR.read_text(encoding="utf-8").splitlines():
        m = pat.search(line)
        if m:
            links.append(m.group(1).lstrip("/"))
    return links


def parse_internal_links(md: Path) -> List[str]:
    pat = re.compile(r"\]\(/([^\)]+\.md)\)")
    links = []
    for line in md.read_text(encoding="utf-8").splitlines():
        for m in pat.finditer(line):
            links.append(m.group(1))
    return links


def buscar_coincidencia(slug: str, index: Dict[str, str]) -> str:
    if slug in index:
        return index[slug]
    base = re.sub(r"^[0-9]+_", "", slug)
    for key, val in index.items():
        if re.sub(r"^[0-9]+_", "", key) == base:
            return val
    return ""


def main() -> int:
    if not SIDEBAR.exists():
        print(
            "No se encontró _sidebar.md; ejecute "
            "generar_sidebar_desde_index.py primero",
            file=sys.stderr,
        )
        return 1

    fs_index = build_fs_index()

    rows = []

    # --- validar enlaces del sidebar ---
    for link in parse_sidebar_links():
        slug = slugify_path(link)
        match = buscar_coincidencia(slug, fs_index)
        if not match:
            rows.append(
                {
                    "origen": "_sidebar.md",
                    "enlace": link,
                    "esperado": slug,
                    "encontrado": match,
                }
            )

    # --- validar enlaces internos ---
    for md in WIKI_DIR.rglob("*.md"):
        if md.name.lower() == "readme.md":
            continue
        for link in parse_internal_links(md):
            slug = slugify_path(link)
            match = buscar_coincidencia(slug, fs_index)
            if not match:
                rows.append(
                    {
                        "origen": str(md.relative_to(WIKI_DIR)),
                        "enlace": link,
                        "esperado": slug,
                        "encontrado": match,
                    }
                )

    out = ROOT / "mismatch_report.csv"
    if rows:
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        print(f"❌ Se encontraron {len(rows)} enlaces rotos")
        return 1
    print("✅ Enlaces verificados correctamente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
