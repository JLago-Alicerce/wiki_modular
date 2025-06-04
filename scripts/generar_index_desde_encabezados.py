import yaml
from pathlib import Path
import logging
import argparse
import sys

def generar_indice(input_file: Path, output_file: Path) -> dict:
    """
    Lee un archivo YAML (mapa_encabezados.yaml) y genera un índice (index_PlataformaBBDD.yaml)
    con una lista de secciones basadas en los campos 'titulo' y 'ruta'.
    
    :param input_file:  Ruta completa al archivo YAML de entrada.
    :param output_file: Ruta completa al archivo YAML de salida.
    :return:            Diccionario con estadísticas del proceso:
                        {
                            "bloques_totales": <int>,
                            "bloques_omitidos": <int>,
                            "bloques_incluidos": <int>,
                            "output_file": <str>
                        }
    """
    if not input_file.exists():
        raise FileNotFoundError(f"No se encuentra el archivo de entrada: {input_file}")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            mapa = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logging.error(f"Error al parsear YAML: {e}")
        return {
            "bloques_totales": 0,
            "bloques_omitidos": 0,
            "bloques_incluidos": 0,
            "output_file": str(output_file)
        }
    except OSError as e:
        logging.error(f"No se pudo leer el archivo: {e}")
        return {
            "bloques_totales": 0,
            "bloques_omitidos": 0,
            "bloques_incluidos": 0,
            "output_file": str(output_file)
        }

    if not isinstance(mapa, list):
        logging.warning(
            f"El contenido del archivo '{input_file.name}' no es una lista. "
            "Se esperaba una lista de bloques con 'titulo' y 'ruta'."
        )
        return {
            "bloques_totales": 0,
            "bloques_omitidos": 0,
            "bloques_incluidos": 0,
            "output_file": str(output_file)
        }

    index_data = {"secciones": []}
    bloques_omitidos = 0

    for bloque in mapa:
        if not isinstance(bloque, dict):
            logging.warning(f"Entrada inválida en el mapa: {bloque}")
            bloques_omitidos += 1
            continue

        titulo = bloque.get("titulo")
        ruta = bloque.get("ruta")

        if not titulo or not ruta:
            logging.warning(
                f"Se omite un bloque por campos incompletos: {bloque}"
            )
            bloques_omitidos += 1
            continue

        index_data["secciones"].append({"titulo": titulo, "ruta": ruta})

    # Guardar el índice en el archivo de salida
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(index_data, f, allow_unicode=True)
    except OSError as e:
        logging.error(f"No se pudo escribir en {output_file}: {e}")
        return {
            "bloques_totales": len(mapa),
            "bloques_omitidos": bloques_omitidos,
            "bloques_incluidos": len(index_data["secciones"]),
            "output_file": str(output_file)
        }

    logging.info(
        f"[✓] {output_file.name} generado con {len(index_data['secciones'])} entradas. "
        f"Se omitieron {bloques_omitidos} bloques."
    )

    return {
        "bloques_totales": len(mapa),
        "bloques_omitidos": bloques_omitidos,
        "bloques_incluidos": len(index_data["secciones"]),
        "output_file": str(output_file)
    }

def main():
    # Ejemplo de uso de argparse para manejar parámetros desde CLI
    parser = argparse.ArgumentParser(
        description="Genera un índice YAML a partir de un mapa de encabezados."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="_fuentes/mapa_encabezados.yaml",
        help="Ruta al archivo de entrada YAML (mapa_encabezados)."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="index_PlataformaBBDD.yaml",
        help="Ruta al archivo de salida YAML (índice)."
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Define el nivel de logging."
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    logging.debug("Iniciando generación de índice con configuración de debug.")

    mapa_path = Path(args.input)
    output_path = Path(args.output)

    resultado = generar_indice(mapa_path, output_path)
    logging.debug(f"Resultados: {resultado}")

    # Salir con código distinto de 0 si no se pudo generar nada
    if resultado["bloques_incluidos"] == 0:
        logging.warning("No se incluyeron bloques en el índice.")
        sys.exit(1)  # Devuelve un estado de error si es necesario

if __name__ == "__main__":
    main()
