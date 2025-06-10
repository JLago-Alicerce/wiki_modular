#!/usr/bin/env python
"""Verifica consistencia entre mapa de encabezados e índice antes de la ingesta."""
import argparse
import sys
from pathlib import Path
from typing import Set

import yaml


def load_titles(path: Path, key: str) -> Set[str]:
    """Carga títulos desde YAML."""
    if not path.exists():
        print(f"[ERROR] No encontrado: {path}")
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {item.get(key, "") for item in data if isinstance(item, dict)}
    if isinstance(data, dict):
        return {
            item.get("titulo", "")
            for item in data.get("secciones", [])
            if isinstance(item, dict)
        }
    return set()


def main(mapa_path: str, index_path: str, ignore_extra: bool = False) -> int:
    """Compara el mapa con el índice y retorna ``1`` si hay inconsistencias."""
    mapa_titulos = load_titles(Path(mapa_path), "titulo")
    index_titulos = load_titles(Path(index_path), "titulo")

    faltantes = mapa_titulos - index_titulos
    huérfanos = index_titulos - mapa_titulos

    for t in sorted(faltantes):
        print(f"NO_ENCONTRADO_EN_INDEX | {t}")
    for t in sorted(huérfanos):
        print(f"INDEX_SIN_ENCABEZADO | {t}")

    extras_error = huérfanos and not ignore_extra

    return 1 if faltantes or extras_error else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compara el mapa de encabezados con el índice de secciones"
    )
    parser.add_argument(
        "mapa",
        nargs="?",
        default="_fuentes/mapa_encabezados.yaml",
        help="Ruta al YAML de mapa de encabezados",
    )
    parser.add_argument(
        "index",
        nargs="?",
        default="index_PlataformaBBDD.yaml",
        help="Ruta al índice YAML",
    )
    parser.add_argument(
        "--ignore-extra",
        action="store_true",
        help="Ignorar entradas extra del índice que no estén en el mapa",
    )
    args = parser.parse_args()
    sys.exit(main(args.mapa, args.index, args.ignore_extra))
