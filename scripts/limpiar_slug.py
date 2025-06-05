#!/usr/bin/env python
"""Utilidades para normalizar y limpiar cadenas a slugs idempotentes."""
import sys
from pathlib import Path

# Permitir ejecutar el script sin instalar el paquete
sys.path.append(str(Path(__file__).resolve().parents[1]))
from wiki_modular import limpiar_slug

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(limpiar_slug(arg))
