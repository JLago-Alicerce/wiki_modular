#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genera un índice de búsqueda para Docsify.

Recorre la carpeta de la wiki, lee el YAML frontmatter de cada archivo
Markdown y construye `search_index.json` con el contenido y metadatos.
"""

import argparse
import json
from pathlib import Path

from wiki_modular.core.search import extraer_frontmatter, generar_indice


def main() -> None:
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
