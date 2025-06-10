#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genera un mapa de encabezados a partir de un archivo Markdown."""

import re
import sys
from pathlib import Path

import yaml

from utils.entorno import add_src_to_path

add_src_to_path()
from wiki_modular import limpiar_slug  # noqa: E402


def generate_map_from_markdown(md_path: Path, yaml_path: Path) -> None:
    """Genera un YAML con los encabezados H2 de ``md_path``.

    Cada entrada contiene:
        - ``h_level``: siempre ``2``.
        - ``titulo``: texto crudo del encabezado.
        - ``ruta``: resultado de :func:`limpiar_slug` + ``.md``.
        - ``start_line``: número de línea donde aparece el H2.
        - ``end_line``: línea anterior al siguiente H2 (o EOF).
    """
    if not md_path.exists():
        print(f"[X] No se encuentra el archivo Markdown: {md_path}")
        sys.exit(1)

    lines = md_path.read_text(encoding="utf-8").splitlines()
    mapa = []
    pat_h2 = re.compile(r"^\s*##(?!#)\s*(.*)$")
    current = None

    for i, line in enumerate(lines):
        m = pat_h2.match(line)
        if m:
            if current:
                current["end_line"] = i
                mapa.append(current)

            raw_title = m.group(1).strip()
            slug = limpiar_slug(raw_title)
            ruta = f"{slug}.md"
            current = {
                "h_level": 2,
                "titulo": raw_title,
                "ruta": ruta,
                "start_line": i + 1,
            }

    if current:
        current["end_line"] = len(lines)
        mapa.append(current)

    # 2) Escribir YAML
    try:
        yaml_path.write_text(yaml.dump(mapa, allow_unicode=True), encoding="utf-8")
        print(f"[✓] Mapa generado con {len(mapa)} bloques (H2).")
    except Exception as e:
        print(f"[X] Error al escribir {yaml_path}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    md_path = Path("_fuentes/tmp_full.md")
    yaml_path = Path("_fuentes/mapa_encabezados.yaml")
    generate_map_from_markdown(md_path, yaml_path)
