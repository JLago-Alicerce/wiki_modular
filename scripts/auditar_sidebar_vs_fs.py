#!/usr/bin/env python
"""
Compara los enlaces de _sidebar.md con los .md reales en disco
y genera un CSV con las discrepancias + propuesta de slug 'limpio'.
"""
import re
import unicodedata
import csv
import sys
from pathlib import Path

# --- Config ---
ROOT = Path(__file__).resolve().parent.parent           # ..\Conocimiento_Tecnico_Navantia
WIKI_DIR = ROOT / "wiki"                               # raíz de .md
SIDEBAR = WIKI_DIR / "_sidebar.md"                         # sidebar global

def limpiar_path(ruta: str) -> str:
    partes = []
    for seg in ruta.split("/"):
        if seg.lower().endswith(".md"):
            nombre = seg[:-3]  # sin .md
            nombre = unicodedata.normalize("NFKD", nombre).encode("ascii","ignore").decode()
            nombre = re.sub(r"[^\w\s\-]", "", nombre)
            nombre = nombre.replace(" ", "_").replace("-", "_")
            nombre = re.sub(r"_+", "_", nombre).strip("_").lower()
            partes.append(nombre + ".md")
        else:
            nombre = unicodedata.normalize("NFKD", seg).encode("ascii","ignore").decode()
            nombre = re.sub(r"[^\w\s\-]", "", nombre)
            nombre = nombre.replace(" ", "_").replace("-", "_")
            nombre = re.sub(r"_+", "_", nombre).strip("_").lower()
            partes.append(nombre)
    return "/".join(partes)

def main() -> None:
    """Ejecuta la auditoría del sidebar vs. los archivos físicos."""
    if not SIDEBAR.exists():
        print(
            "No se encontró _sidebar.md; ejecute generar_sidebar_desde_index.py primero",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- 1) Lee enlaces del sidebar ---
    pat_link = re.compile(r"\]\(([^)]+\.md)\)")
    links = []
    for line in SIDEBAR.read_text(encoding="utf8").splitlines():
        m = pat_link.search(line)
        if m:
            link = m.group(1).lstrip("/")
            # Ignore README entries as they are handled implicitly by Docsify
            if Path(link).name.lower() == "readme.md":
                continue
            links.append(link)

    # --- 2) Índice físico ---
    # Usa rutas relativas a WIKI_DIR para facilitar la comparación con los enlaces
    # del sidebar, que normalmente no incluyen el prefijo "wiki/".
    files = {
        str(p.relative_to(WIKI_DIR)).replace("\\", "/").lower(): p
        for p in WIKI_DIR.rglob("*.md")
        if p.name.lower() != "readme.md"
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
        rows.append({
            "enlace_sidebar": link,
            "coincidencia_fs": match or "",
            "slug_sidebar": norm_link,
            "slug_fs": limpiar_path(match) if match else "",
            "status": "OK" if match else "NO_MATCH"
        })

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
        sys.exit(1)

    with out.open("w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

    mismatches = [r for r in rows if r["status"] == "NO_MATCH"]
    if mismatches:
        print(
            f"❌ Se encontraron {len(mismatches)} enlaces sin correspondencia"
        )
        sys.exit(1)
    else:
        print("✅ Auditoría OK: no hay rutas rotas.")


if __name__ == "__main__":
    main()
