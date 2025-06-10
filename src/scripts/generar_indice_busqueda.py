#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genera un índice de búsqueda para Docsify.

Recorre la carpeta de la wiki, lee el YAML frontmatter de cada archivo
Markdown y construye `search_index.json` con el contenido y metadatos.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Tuple, List

import yaml

from wiki_modular import limpiar_slug


def extraer_frontmatter(path: Path) -> Tuple[Dict[str, str], str, List[Dict[str, object]]]:
    """Devuelve ``(metadata, cuerpo, encabezados)`` del Markdown."""
    texto = path.read_text(encoding="utf-8")
    if texto.startswith("---"):
        partes = texto.split("---", 2)
        if len(partes) >= 3:
            try:
                meta = yaml.safe_load(partes[1]) or {}
            except yaml.YAMLError:
                meta = {}
            cuerpo = partes[2].lstrip("\n")
        else:
            meta = {}
            cuerpo = texto
    else:
        meta = {}
        cuerpo = texto

    encabezados: List[Dict[str, object]] = []
    pat = re.compile(r"^(#{2,6})\s+(.*)$")
    for line in cuerpo.splitlines():
        m = pat.match(line.strip())
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            encabezados.append({
                "level": level,
                "text": text,
                "slug": limpiar_slug(text),
            })

    return meta, cuerpo, encabezados


def generar_indice(wiki_dir: Path) -> Dict[str, Dict[str, object]]:
    """Genera el diccionario para ``search_index.json`` desde ``wiki_dir``."""
    indice: Dict[str, Dict[str, object]] = {}
    for md in wiki_dir.rglob("*.md"):
        meta, cuerpo, encabezados = extraer_frontmatter(md)
        indice[str(md.relative_to(wiki_dir))] = {
            "metadata": meta,
            "content": cuerpo,
            "headers": encabezados,
        }
    return indice




def main() -> None:
    """CLI para crear ``search_index.json`` desde los Markdown de la wiki."""
    parser = argparse.ArgumentParser(description="Genera search_index.json")
    parser.add_argument("--wiki", default="wiki", help="Directorio raíz de la wiki")
    parser.add_argument("--output", default="search_index.json", help="Archivo JSON de salida")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki)
    data = generar_indice(wiki_dir)
    Path(args.output).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
