#!/usr/bin/env python
"""Verifica consistencia entre mapa de encabezados e índice antes de la ingesta."""
import sys
import yaml
from pathlib import Path
from typing import Set


def load_titles(path: Path, key: str) -> Set[str]:
    """Carga títulos desde YAML"""
    if not path.exists():
        print(f"[ERROR] No encontrado: {path}")
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {item.get(key, "") for item in data if isinstance(item, dict)}
    if isinstance(data, dict):
        return {item.get("titulo", "") for item in data.get("secciones", []) if isinstance(item, dict)}
    return set()


def main(mapa_path: str, index_path: str) -> int:
    mapa_titulos = load_titles(Path(mapa_path), "titulo")
    index_titulos = load_titles(Path(index_path), "titulo")

    faltantes = mapa_titulos - index_titulos
    huérfanos = index_titulos - mapa_titulos

    for t in sorted(faltantes):
        print(f"NO_ENCONTRADO_EN_INDEX | {t}")
    for t in sorted(huérfanos):
        print(f"INDEX_SIN_ENCABEZADO | {t}")

    return 1 if faltantes or huérfanos else 0


if __name__ == "__main__":
    mapa = sys.argv[1] if len(sys.argv) > 1 else "_fuentes/mapa_encabezados.yaml"
    index = sys.argv[2] if len(sys.argv) > 2 else "index_PlataformaBBDD.yaml"
    sys.exit(main(mapa, index))

