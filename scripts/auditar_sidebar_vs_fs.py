#!/usr/bin/env python3
"""
Compara los enlaces de _sidebar.md con los .md reales en disco
y genera un CSV con las discrepancias + propuesta de slug 'limpio'.
"""
import re, unicodedata, csv
from pathlib import Path

# --- Config ---
ROOT = Path(__file__).resolve().parent.parent           # ..\Conocimiento_Tecnico_Navantia
SIDEBAR = ROOT / "_sidebar.md"                         # sidebar global
WIKI_DIR = ROOT / "wiki"                               # raíz de .md

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

# --- 1) Lee enlaces del sidebar ---
pat_link = re.compile(r"\]\(([^)]+\.md)\)")
links = []
for line in SIDEBAR.read_text(encoding="utf8").splitlines():
    m = pat_link.search(line)
    if m:
        links.append(m.group(1).lstrip("/"))

# --- 2) Índice físico ---
files = {str(p.relative_to(ROOT)).replace("\\","/").lower(): p for p in WIKI_DIR.rglob("*.md")}

# --- 3) Compara ---
rows = []
for link in links:
    norm_link = limpiar_path(link)
    # Busca coincidencia fuzzy sobre las rutas físicas normalizadas
    match = None
    for fs_path in files:
        if limpiar_path(fs_path) == norm_link:
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
with out.open("w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)

print(f"✅ Auditoría terminada: {out}")


# Añade al final del script anterior
import argparse, shutil, sys
ap = argparse.ArgumentParser()
ap.add_argument("--fix", choices=["fs","sidebar"], help="Aplicar corrección")
args = ap.parse_args()

if args.fix == "sidebar":
    new_sidebar = []
    for row in rows:
        if row["status"] == "OK":
            new_sidebar.append(row["enlace_sidebar"])
        else:
            # Si NO_MATCH y hubo sugerencia slug_fs
            if row["coincidencia_fs"]:
                new_sidebar.append(row["coincidencia_fs"])
            else:
                new_sidebar.append(row["enlace_sidebar"] + "  <!-- pendiente -->")
    # reconstruye líneas (mantén jerarquía si quieres)
    with open(ROOT/"_sidebar_actualizado.md","w",encoding="utf8") as f:
        for l in new_sidebar:
            f.write(f"* [{Path(l).stem}]({l})\n")
    print("➡️ Generado _sidebar_actualizado.md")

elif args.fix == "fs":
    for row in rows:
        if row["status"] == "NO_MATCH" and row["coincidencia_fs"]:
            src = ROOT / row["coincidencia_fs"]
            dst = ROOT / row["enlace_sidebar"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            print(f"🡒 {src}  →  {dst}")
    print("➡️ Archivos renombrados / movidos")

else:
    sys.exit(0)

print("→ Abre mismatch_report.csv para ver qué enlaces no encuentran archivo.")