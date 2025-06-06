#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
generar_sidebar_desde_index.py
------------------------------
Genera el archivo '_sidebar.md' dentro de la carpeta 'wiki/' para Docsify a
partir de 'index_PlataformaBBDD.yaml'.
Esta versión es tolerante a la ausencia del campo 'id' y del campo 'slug' en cada sección.
"""

import sys
import yaml
from pathlib import Path

# Permitir ejecutar el script sin instalar el paquete
sys.path.append(str(Path(__file__).resolve().parents[1]))
from wiki_modular import load_yaml
import unicodedata
import re
from wiki_modular import limpiar_slug
from typing import Any, Dict, List

# --------------------------------------------------
# Rutas de proyecto
# --------------------------------------------------
ROOT_DIR     = Path(__file__).resolve().parent.parent
WIKI_DIR     = ROOT_DIR / "wiki"
INDEX_FILE   = ROOT_DIR / "index_PlataformaBBDD.yaml"
SIDEBAR_FILE = WIKI_DIR / "_sidebar.md"


# --------------------------------------------------
# Excepciones personalizadas
# --------------------------------------------------
class IndexFileNotFoundError(FileNotFoundError):
    """
    Excepción lanzada cuando 'index_PlataformaBBDD.yaml' no se encuentra.
    """
    pass

class InvalidIndexSchemaError(Exception):
    """
    Excepción lanzada cuando la estructura del YAML no cumple con el formato esperado.
    """
    pass


# --------------------------------------------------
# Funciones auxiliares
# --------------------------------------------------
def load_index(path: Path) -> Dict[str, Any]:
    """
    Carga y parsea el YAML de índice desde la ruta especificada.

    :param path: Ruta al archivo 'index_PlataformaBBDD.yaml'.
    :return:     Diccionario con los datos parseados del índice.
    :raises IndexFileNotFoundError: Si el archivo no existe.
    :raises yaml.YAMLError: Si ocurre un error al parsear el YAML.
    """
    if not path.exists():
        raise IndexFileNotFoundError(f"No se encontró '{path.name}' en la ruta: {path}")

    datos = load_yaml(path)
    return datos if isinstance(datos, dict) else {}


def validate_index_schema(data: Dict[str, Any]) -> None:
    """
    Valida la estructura del diccionario 'data' para que cumpla el formato mínimo:

    data = {
      "secciones": [
        {
          "titulo": <str>,
          "slug":   <str> (opcional),
          "id":     <str|int> (opcional),
          "subtemas": [<str>, ...] (opcional)
        },
        ...
      ]
    }

    Si falta 'slug', se generará automáticamente más adelante en build_sidebar_lines().

    :param data: Contenido cargado desde 'index_PlataformaBBDD.yaml'.
    :raises InvalidIndexSchemaError: Si falta "secciones" o el contenido esperado en cada sección.
    """
    if "secciones" not in data or not isinstance(data["secciones"], list):
        raise InvalidIndexSchemaError("El YAML debe contener clave 'secciones' como lista.")

    for idx, seccion in enumerate(data["secciones"], start=1):
        if not isinstance(seccion, dict):
            raise InvalidIndexSchemaError(f"La sección en posición {idx} no es un mapeo válido.")

        # Exigimos únicamente 'titulo'; 'slug' es opcional
        if "titulo" not in seccion:
            raise InvalidIndexSchemaError(f"Falta 'titulo' en la sección de índice {idx}.")

        # subtemas, si existe, debe ser lista
        if "subtemas" in seccion and not isinstance(seccion["subtemas"], list):
            raise InvalidIndexSchemaError(f"'subtemas' en la sección {idx} debe ser lista.")


def slugify(text: str) -> str:
    """Wrapper retrocompatible que usa :func:`limpiar_slug`."""
    return limpiar_slug(text)


def build_sidebar_lines(data: Dict[str, Any]) -> List[str]:
    """
    Construye las líneas que se usarán en el archivo '_sidebar.md'.
    
    Para cada sección:
      * Si falta 'slug', se genera con slugify(titulo).
      * Se genera un enlace de la forma:
          * [Título sección](<id>_<slug_seccion>.md)
        donde '<id>_' aparece solo si la sección tiene el campo 'id'.
    
    Para cada subtema:
      * Se anida con dos espacios y un asterisco:
          *   [Título subtema](<carpeta_subtemas>/<slug_subtema>.md)
      * Si el 'subtema' contiene la palabra 'sql', se coloca en '02_Instancias_SQL';
        de lo contrario, se usa el 'slug' de la sección principal.

    :param data: Estructura validada (con 'secciones') proveniente del índice YAML.
    :return:     Lista de líneas que conformarán el contenido de '_sidebar.md'.
    """
    lines: List[str] = ["* [Inicio](README.md)"]
    secciones = data["secciones"]

    for seccion in secciones:
        sec_title = seccion["titulo"]
        # Si falta 'slug', generarlo desde 'titulo'
        sec_slug = seccion.get("slug", slugify(sec_title))
        sec_id   = seccion.get("id")

        # Nombre de archivo de la sección: "<id>_<slug>.md" o "<slug>.md" si no hay id
        prefix = f"{sec_id}_" if sec_id is not None else ""
        filename = f"{prefix}{sec_slug}.md"
        lines.append(f"* [{sec_title}]({filename})")

        # Procesar subtemas (si existen)
        for sub in seccion.get("subtemas", []):
            sub_title = sub
            sub_slug  = slugify(sub_title)

            # Regla por defecto: si contiene 'sql', carpeta "02_Instancias_SQL"
            if "sql" in sub_slug:
                carpeta = "02_Instancias_SQL"
            else:
                carpeta = sec_slug

            sub_filename = f"{sub_slug}.md"
            lines.append(f"  * [{sub_title}]({carpeta}/{sub_filename})")

    lines.append("")  # Línea vacía al final
    return lines


# --------------------------------------------------
# Función principal (entry point)
# --------------------------------------------------
def main() -> None:
    """
    Flujo principal:
      1) Carga el índice 'index_PlataformaBBDD.yaml'.
      2) Valida la estructura (exige 'titulo'; 'slug' se crea si falta).
      3) Construye las líneas de '_sidebar.md'.
      4) Escribe el resultado en '_sidebar.md'.
    """
    # 1) Cargar índice
    try:
        index_data = load_index(INDEX_FILE)
    except IndexFileNotFoundError as fnf:
        print(f"[ERROR] {fnf}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as parse_err:
        print(f"[ERROR] Falló parseo de YAML en '{INDEX_FILE.name}': {parse_err}", file=sys.stderr)
        sys.exit(1)

    # 2) Validar esquema
    try:
        validate_index_schema(index_data)
    except InvalidIndexSchemaError as schema_err:
        print(f"[ERROR] Índice con estructura inválida: {schema_err}", file=sys.stderr)
        sys.exit(1)

    # 3) Generar líneas de _sidebar.md
    sidebar_lines = build_sidebar_lines(index_data)

    # 4) Escribir en disco
    try:
        SIDEBAR_FILE.write_text("\n".join(sidebar_lines), encoding="utf-8")
        print("✅ '_sidebar.md' generado/actualizado correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo escribir '{SIDEBAR_FILE}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
