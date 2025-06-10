#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
generar_sidebar.py
------------------
Genera el archivo ``_sidebar.md`` a partir de ``index_PlataformaBBDD.yaml``.

Permite operar en modo estricto o tolerante mediante ``--tolerant``. El modo
estricto exige que cada sección tenga un ``id`` único y detecta rutas
duplicadas; el modo tolerante omite esas comprobaciones.
"""

import sys
from pathlib import Path

from utils.entorno import add_src_to_path, ROOT_DIR, WIKI_DIR

add_src_to_path()

import argparse
from typing import Any, Dict, List

import yaml


from wiki_modular import limpiar_slug, load_yaml
from wiki_modular.config import WIKI_DIR

from wiki_modular.core.sidebar import (
    IndexFileNotFoundError,
    InvalidIndexSchemaError,
    build_sidebar_lines,
    load_index,
    validate_index_schema,
)


# --------------------------------------------------
# Rutas de proyecto
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

INDEX_FILE = ROOT_DIR / "index_PlataformaBBDD.yaml"
SIDEBAR_FILE = WIKI_DIR / "_sidebar.md"


# --------------------------------------------------
# Función principal (entry point)
# --------------------------------------------------
def main() -> None:
    """Genera ``_sidebar.md`` a partir de un índice YAML."""
    parser = argparse.ArgumentParser(
        description="Genera el _sidebar.md desde un índice YAML"
    )
    parser.add_argument(
        "--index", type=str, default=str(INDEX_FILE), help="Ruta al índice YAML"
    )
    parser.add_argument(
        "--out", type=str, default=str(SIDEBAR_FILE), help="Archivo de salida"
    )
    parser.add_argument(
        "--tolerant",
        action="store_true",
        help="Permitir secciones sin id y rutas duplicadas",
    )
    args = parser.parse_args()

    index_path = Path(args.index)
    sidebar_path = Path(args.out)

    # 1) Cargar índice
    try:
        index_data = load_index(index_path)
    except IndexFileNotFoundError as fnf:
        print(f"[ERROR] {fnf}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as parse_err:
        print(
            f"[ERROR] Falló parseo de YAML en '{index_path.name}': {parse_err}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2) Validar esquema
    try:
        validate_index_schema(index_data, tolerant=args.tolerant)
    except InvalidIndexSchemaError as schema_err:
        print(f"[ERROR] Índice con estructura inválida: {schema_err}", file=sys.stderr)
        sys.exit(1)

    # 3) Generar líneas de _sidebar.md
    sidebar_lines = build_sidebar_lines(index_data, tolerant=args.tolerant)

    # 4) Escribir en disco
    try:
        sidebar_path.write_text("\n".join(sidebar_lines), encoding="utf-8")
        print(f"✅ '{sidebar_path}' generado/actualizado correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo escribir '{sidebar_path}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
