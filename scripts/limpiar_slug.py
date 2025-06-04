#!/usr/bin/env python3
"""Utilidades para normalizar y limpiar cadenas a slugs idempotentes."""
import re
import unicodedata


def limpiar_slug(texto: str) -> str:
    """Devuelve un slug idempotente para nombres de archivo.

    Pasos aplicados:
        - Normaliza a ASCII eliminando diacríticos.
        - Convierte a minúsculas.
        - Reemplaza espacios y barras con "_".
        - Elimina caracteres fuera de ``[a-z0-9_-]``.
        - Comprime repeticiones de "_".
    """
    if not isinstance(texto, str):
        texto = str(texto)
    ascii_text = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    ascii_text = ascii_text.lower()
    ascii_text = ascii_text.replace(" ", "_").replace("/", "_")
    ascii_text = re.sub(r"[^a-z0-9_-]", "", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    return ascii_text

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(limpiar_slug(arg))

