#!/usr/bin/env python
"""Audita enlaces del sidebar versus archivos reales.

Compara los enlaces de ``_sidebar.md`` con los archivos ``.md`` presentes
en la wiki y genera un CSV con las discrepancias más una propuesta de slug
"limpio".
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

from utils.entorno import ROOT_DIR
from utils.wiki import get_sidebar_links, list_markdown_files
from wiki_modular.config import SIDEBAR_FILE, WIKI_DIR

ROOT = ROOT_DIR
SIDEBAR = SIDEBAR_FILE


def limpiar_path(ruta: str) -> str:
    """Normaliza ``ruta`` a un slug comparable para la auditoría."""
    partes = []
    for seg in ruta.split("/"):
        if seg.lower().endswith(".md"):
            nombre = seg[:-3]  # sin .md
            nombre = (
                unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode()
            )
            nombre = re.sub(r"[^\w\s\-]", "", nombre)
            nombre = nombre.replace(" ", "_").replace("-", "_")
            nombre = re.sub(r"_+", "_", nombre).strip("_").lower()
            partes.append(nombre + ".md")
        else:
            nombre = (
                unicodedata.normalize("NFKD", seg).encode("ascii", "ignore").decode()
            )
            nombre = re.sub(r"[^\w\s\-]", "", nombre)
            nombre = nombre.replace(" ", "_").replace("-", "_")
            nombre = re.sub(r"_+", "_", nombre).strip("_").lower()
            partes.append(nombre)
    return "/".join(partes)


def main() -> None:
    """Ejecuta la auditoría del sidebar vs. los archivos físicos."""
    if not SIDEBAR.exists():
        print(
            "No se encontró _sidebar.md; ejecute generar_sidebar.py primero",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- 1) Lee enlaces del sidebar ---
    links = [
        l for l in get_sidebar_links(SIDEBAR) if Path(l).name.lower() != "readme.md"
    ]

    # --- 2) Índice físico ---
    # Usa rutas relativas a WIKI_DIR para facilitar la comparación con los enlaces
    # del sidebar, que normalmente no incluyen el prefijo "wiki/".
    files = {
        f.lower(): WIKI_DIR / f
        for f in list_markdown_files(WIKI_DIR)
        if Path(f).name.lower() != "readme.md"
    }

    # --- 3) Compara ---
    rows = []
    for link in links:
        norm_link = limpiar_path(link)
        # Busca coincidencia exacta sobre las rutas físicas normalizadas
        match = None
        for fs_path in files:
            fs_norm = limpiar_path(fs_path)
            if fs_norm == norm_link:
                match = fs_path
                break
        # Si no hay coincidencia exacta, intenta ignorando prefijos numéricos
        if not match:
            base_link = re.sub(r"^[0-9]+_", "", norm_link)
            for fs_path in files:
                fs_norm = limpiar_path(fs_path)
                base_fs = re.sub(r"^[0-9]+_", "", fs_norm)
                if base_fs == base_link:
                    match = fs_path
                    break
        rows.append(
            {
                "enlace_sidebar": link,
                "coincidencia_fs": match or "",
                "slug_sidebar": norm_link,
                "slug_fs": limpiar_path(match) if match else "",
                "status": "OK" if match else "NO_MATCH",
            }
        )

    # --- 4) Exporta CSV ---
    out = ROOT / "mismatch_report.csv"

    if not rows:
        # Si no se encontraron enlaces en el sidebar, crear CSV vacío con
        # cabeceras conocidas para mantener la compatibilidad con otras
        # herramientas y avisar al usuario.
        headers = [
            "enlace_sidebar",
            "coincidencia_fs",
            "slug_sidebar",
            "slug_fs",
            "status",
        ]
        with out.open("w", newline="", encoding="utf8") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
        print("No se encontraron enlaces en _sidebar.md")
        return

    with out.open("w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    mismatches = [r for r in rows if r["status"] == "NO_MATCH"]
    if mismatches:
        print(f"❌ Se encontraron {len(mismatches)} enlaces sin correspondencia")
        sys.exit(1)
    else:
        print("✅ Auditoría OK: no hay rutas rotas.")


if __name__ == "__main__":
    main()
