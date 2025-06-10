#!/usr/bin/env python
"""Limpia atributos de imagen en un archivo Markdown."""
import sys
from pathlib import Path

from utils.entorno import add_src_to_path

add_src_to_path()
from wiki_modular import limpiar_archivo_markdown


def main() -> None:
    md_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_fuentes/tmp_full.md")
    limpiar_archivo_markdown(md_path)


if __name__ == "__main__":
    main()
