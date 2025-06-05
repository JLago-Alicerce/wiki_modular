#!/usr/bin/env python3
"""Utilidades para normalizar y limpiar cadenas a slugs idempotentes."""
from wiki_modular import limpiar_slug

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(limpiar_slug(arg))
