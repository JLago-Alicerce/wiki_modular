#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Genera el índice maestro a partir de un mapa de encabezados."""

import sys
from pathlib import Path

import yaml

from utils.entorno import add_src_to_path

add_src_to_path()
import argparse
import logging

from wiki_modular import limpiar_slug, load_yaml


def generar_indice(input_file: Path, output_file: Path) -> dict:
    """Genera el índice maestro desde un mapa de encabezados.

    Lee un YAML de encabezados (lista de dicts con 'titulo' y 'ruta') y
    construye un índice maestro (index_PlataformaBBDD.yaml) con:
      - id: número secuencial según orden en lista
      - titulo: texto original
      - slug: slug generado con limpiar_slug()
      - subtemas: (vacío por defecto; se puede completar manualmente)
    """
    if not input_file.exists():
        raise FileNotFoundError(f"No se encuentra: {input_file}")

    try:
        mapa = load_yaml(input_file)
    except yaml.YAMLError as e:
        logging.error(f"Error parseando YAML: {e}")
        return {
            "bloques_totales": 0,
            "bloques_omitidos": 0,
            "bloques_incluidos": 0,
            "output_file": str(output_file),
        }

    if not isinstance(mapa, list):
        logging.warning("El YAML de entrada no es una lista de bloques.")
        return {
            "bloques_totales": 0,
            "bloques_omitidos": 0,
            "bloques_incluidos": 0,
            "output_file": str(output_file),
        }

    index_data = {"secciones": []}
    if output_file.exists():
        try:
            existente = load_yaml(output_file)
            if isinstance(existente, dict) and isinstance(
                existente.get("secciones"), list
            ):
                index_data["secciones"] = existente["secciones"]
        except Exception as e:  # pragma: no cover - fallo no crítico
            logging.warning(f"No se pudo leer índice existente: {e}")

    max_id = max((sec.get("id", 0) for sec in index_data["secciones"]), default=0)
    omitidos = 0

    next_id = max_id
    for idx, bloque in enumerate(mapa, start=1):
        if not isinstance(bloque, dict) or "titulo" not in bloque:
            logging.warning(f"Bloque inválido u omisión en posición {idx}: {bloque}")
            omitidos += 1
            continue

        titulo = bloque["titulo"]
        slug = limpiar_slug(titulo)
        next_id += 1
        index_data["secciones"].append(
            {
                "id": next_id,
                "titulo": titulo,
                "slug": slug,
                "subtemas": [],  # Puede completarse manualmente tras revisar índice
            }
        )

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(index_data, f, allow_unicode=True)
        logging.info(
            "[✓] %s generado con %d secciones. Omitidos: %d.",
            output_file.name,
            len(index_data["secciones"]),
            omitidos,
        )
    except OSError as e:
        logging.error(f"No se pudo escribir en {output_file}: {e}")

    return {
        "bloques_totales": len(mapa),
        "bloques_omitidos": omitidos,
        "bloques_incluidos": len(index_data["secciones"]),
        "output_file": str(output_file),
    }


def main():
    """CLI para construir el índice a partir del mapa de encabezados."""
    parser = argparse.ArgumentParser(
        description="Genera índice YAML desde mapa de encabezados."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="_fuentes/mapa_encabezados.yaml",
        help="Archivo de entrada (mapa de encabezados).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="index_PlataformaBBDD.yaml",
        help="Archivo de salida (índice).",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--precheck",
        action="store_true",
        help="Ejecutar verificación previa de consistencia",
    )
    parser.add_argument(
        "--ignore-extra",
        action="store_true",
        help="Al usar --precheck, no fallar por entradas extra en el índice",
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    input_path = Path(args.input)
    output_path = Path(args.output)

    resultado = generar_indice(input_path, output_path)
    if resultado["bloques_incluidos"] == 0:
        logging.warning(
            "No se incluyeron secciones en el índice; revisa el YAML de entrada."
        )
        return 0

    if args.precheck:
        from subprocess import call

        from utils.entorno import script_path

        cmd = [
            sys.executable,
            str(script_path("verificar_pre_ingesta.py")),
            str(input_path),
            str(output_path),
        ]
        if args.ignore_extra:
            cmd.append("--ignore-extra")
        rc = call(cmd)
        if rc != 0:
            logging.error("Verificación previa falló")
            sys.exit(rc)


if __name__ == "__main__":
    main()
