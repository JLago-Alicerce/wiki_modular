#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml
from pathlib import Path

# Permitir ejecutar el script sin instalar el paquete
sys.path.append(str(Path(__file__).resolve().parents[1]))
from wiki_modular import load_yaml
import logging
import argparse
from wiki_modular import limpiar_slug


def generar_indice(input_file: Path, output_file: Path) -> dict:
    """
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
        return {"bloques_totales": 0, "bloques_omitidos": 0, "bloques_incluidos": 0, "output_file": str(output_file)}

    if not isinstance(mapa, list):
        logging.warning("El YAML de entrada no es una lista de bloques.")
        return {"bloques_totales": 0, "bloques_omitidos": 0, "bloques_incluidos": 0, "output_file": str(output_file)}

    index_data = {"secciones": []}
    if output_file.exists():
        try:
            existente = load_yaml(output_file)
            if isinstance(existente, dict) and isinstance(existente.get("secciones"), list):
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
        index_data["secciones"].append({
            "id": next_id,
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
    parser.add_argument("--precheck", action="store_true", help="Ejecutar verificación previa de consistencia")
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    input_path = Path(args.input)
    output_path = Path(args.output)

    resultado = generar_indice(input_path, output_path)
    if resultado["bloques_incluidos"] == 0:
        logging.warning("No se incluyeron secciones en el índice; revisa el YAML de entrada.")
        sys.exit(1)

    if args.precheck:
        from subprocess import call
        rc = call([sys.executable, "scripts/verificar_pre_ingesta.py", str(input_path), str(output_path)])
        if rc != 0:
            logging.error("Verificación previa falló")
            sys.exit(rc)

if __name__ == "__main__":
    main()
