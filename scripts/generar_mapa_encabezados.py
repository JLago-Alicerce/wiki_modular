#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml
from pathlib import Path
from wiki_modular import limpiar_slug

def generate_map_from_markdown(md_path: Path, yaml_path: Path) -> None:
    """
    Lee un archivo Markdown y genera un YAML con sus encabezados (H1 a H5):
      - h_level: nivel de encabezado (1–5)
      - titulo: texto crudo del encabezado
      - ruta: slug generado con limpiar_slug() + ".md"
      - start_line: número de línea donde aparece el encabezado
      - end_line: línea anterior al comienzo del siguiente encabezado
    """
    if not md_path.exists():
        print(f"[X] No se encuentra el archivo Markdown: {md_path}")
        sys.exit(1)

    lines = md_path.read_text(encoding="utf-8").splitlines()
    mapa = []

    # 1) Detectar encabezados H1–H5
    for i, line in enumerate(lines):
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            if 1 <= level <= 5:
                raw_title = line[level:].strip()
                slug = limpiar_slug(raw_title)
                ruta = f"{slug}.md"
                mapa.append({
                    "h_level": level,
                    "titulo": raw_title,
                    "ruta": ruta,
                    "start_line": i + 1
                })

    # 2) Calcular end_line de cada bloque
    for idx in range(len(mapa) - 1):
        mapa[idx]["end_line"] = mapa[idx + 1]["start_line"] - 1
    if mapa:
        mapa[-1]["end_line"] = len(lines)

    # 3) Escribir YAML
    try:
        yaml_path.write_text(yaml.dump(mapa, allow_unicode=True), encoding="utf-8")
        print(f"[✓] Mapa generado con {len(mapa)} bloques (H1–H5).")
    except Exception as e:
        print(f"[X] Error al escribir {yaml_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    md_path = Path("_fuentes/tmp_full.md")
    yaml_path = Path("_fuentes/mapa_encabezados.yaml")
    generate_map_from_markdown(md_path, yaml_path)
