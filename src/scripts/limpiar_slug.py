#!/usr/bin/env python
"""Utilidades para normalizar y limpiar cadenas a slugs idempotentes."""

from utils.entorno import add_src_to_path

add_src_to_path()
from wiki_modular import limpiar_slug

if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        print(limpiar_slug(arg))
