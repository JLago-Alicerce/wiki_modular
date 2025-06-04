#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml
import logging
import argparse
from pathlib import Path

def normalize_slug(text: str) -> str:
    """
    Convierte el texto a un slug:
      - Normaliza a NFKD (elimina acentos/diacríticos).
      - Convierte a ASCII descartando caracteres no mapeables.
      - Elimina todo lo que no sea alfanumérico, espacio o guion.
      - Reemplaza secuencias de espacios o guiones por un solo "_".
      - Convierte a minúsculas.
    """
    import re, unicodedata
    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    cleaned = re.sub(r'[^A-Za-z0-9\s-]', '', ascii_text)
    underscored = re.sub(r'[\s-]+', '_', cleaned).strip('_')
    return underscored.lower()

def generar_indice(input_file: Path, output_file: Path) -> dict:
    """
    Lee un YAML de encabezados (lista de dicts con 'titulo' y 'ruta') y
    construye un índice maestro (index_PlataformaBBDD.yaml) con:
      - id: número secuencial según orden en lista
      - titulo: texto original
      - slug: slug generado con normalize_slug()
      - subtemas: (vacío por defecto; se puede completar manualmente)
    """
    if not input_file.exists():
        raise FileNotFoundError(f"No se encuentra: {input_file}")

    try:
        mapa = yaml.safe_load(input_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        logging.error(f"Error parseando YAML: {e}")
        return {"bloques_totales": 0, "bloques_omitidos": 0, "bloques_incluidos": 0, "output_file": str(output_file)}

    if not isinstance(mapa, list):
        logging.warning("El YAML de entrada no es una lista de bloques.")
        return {"bloques_totales": 0, "bloques_omitidos": 0, "bloques_incluidos": 0, "output_file": str(output_file)}

    index_data = {"secciones": []}
    omitidos = 0

    for idx, bloque in enumerate(mapa, start=1):
        if not isinstance(bloque, dict) or "titulo" not in bloque:
            logging.warning(f"Bloque inválido u omisión en posición {idx}: {bloque}")
            omitidos += 1
            continue

        titulo = bloque["titulo"]
        slug = normalize_slug(titulo)
        index_data["secciones"].append({
            "id": idx,
            "titulo": titulo,
            "slug": slug,
            "subtemas": []  # Puede completarse manualmente tras revisar índice
        })

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(index_data, f, allow_unicode=True)
        logging.info(f"[✓] {output_file.name} generado con {len(index_data['secciones'])} secciones. Omitidos: {omitidos}.")
    except OSError as e:
        logging.error(f"No se pudo escribir en {output_file}: {e}")

    return {
        "bloques_totales": len(mapa),
        "bloques_omitidos": omitidos,
        "bloques_incluidos": len(index_data["secciones"]),
        "output_file": str(output_file)
    }

def main():
    parser = argparse.ArgumentParser(description="Genera índice YAML desde mapa de encabezados.")
    parser.add_argument("--input", type=str, default="_fuentes/mapa_encabezados.yaml", help="Archivo de entrada (mapa de encabezados).")
    parser.add_argument("--output", type=str, default="index_PlataformaBBDD.yaml", help="Archivo de salida (índice).")
    parser.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    input_path = Path(args.input)
    output_path = Path(args.output)

    resultado = generar_indice(input_path, output_path)
    if resultado["bloques_incluidos"] == 0:
        logging.warning("No se incluyeron secciones en el índice; revisa el YAML de entrada.")
        sys.exit(1)

if __name__ == "__main__":
    main()
