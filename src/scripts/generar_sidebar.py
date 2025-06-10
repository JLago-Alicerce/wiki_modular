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

sys.path.append(str(Path(__file__).resolve().parents[2]))

import argparse
from typing import Any, Dict, List

import yaml

from wiki_modular import limpiar_slug, load_yaml
from wiki_modular.config import WIKI_DIR

# --------------------------------------------------
# Rutas de proyecto
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT_DIR / "index_PlataformaBBDD.yaml"
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


def validate_index_schema(data: Dict[str, Any], *, tolerant: bool = False) -> None:
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
        raise InvalidIndexSchemaError(
            "El YAML debe contener clave 'secciones' como lista."
        )

    for idx, seccion in enumerate(data["secciones"], start=1):
        if not isinstance(seccion, dict):
            raise InvalidIndexSchemaError(
                f"La sección en posición {idx} no es un mapeo válido."
            )

        # Exigimos únicamente 'titulo' y opcionalmente 'id'
        if "titulo" not in seccion:
            raise InvalidIndexSchemaError(
                f"Falta 'titulo' en la sección de índice {idx}."
            )
        if not tolerant and "id" not in seccion:
            raise InvalidIndexSchemaError(
                "Falta 'id' en la sección de índice "
                f"{idx} (ejecute con --tolerant para permitirlo)."
            )

        # subtemas, si existe, debe ser lista
        if "subtemas" in seccion and not isinstance(seccion["subtemas"], list):
            raise InvalidIndexSchemaError(
                f"'subtemas' en la sección {idx} debe ser lista."
            )


def slugify(text: str) -> str:
    """Wrapper retrocompatible que usa :func:`limpiar_slug`."""
    return limpiar_slug(text)


def build_sidebar_lines(data: Dict[str, Any], *, tolerant: bool = False) -> List[str]:
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
    seen_paths = set()

    for seccion in secciones:
        sec_title = seccion["titulo"]
        # Si falta 'slug', generarlo desde 'titulo'
        sec_slug = seccion.get("slug", slugify(sec_title))
        sec_id = seccion.get("id")

        # Nombre de archivo de la sección: "<id>_<slug>.md" o "<slug>.md" si no hay id
        if sec_id is None and not tolerant:
            raise InvalidIndexSchemaError(
                f"Sección '{sec_title}' sin 'id'; use --tolerant para permitirlo"
            )

        prefix = f"{sec_id}_" if sec_id is not None else ""
        filename = f"{prefix}{sec_slug}.md"
        key = filename.lower()
        if key in seen_paths:
            msg = f"Ruta duplicada: {filename}"
            if not tolerant:
                raise InvalidIndexSchemaError(msg)
            else:
                continue
        seen_paths.add(key)
        lines.append(f"* [{sec_title}]({filename})")

        # Procesar subtemas (si existen)
        for sub in seccion.get("subtemas", []):
            sub_title = sub
            sub_slug = slugify(sub_title)

            # Evitar que un subtema duplique a la propia sección
            if sub_slug == sec_slug:
                continue

            # Regla por defecto: si contiene 'sql', carpeta "02_Instancias_SQL"
            if "sql" in sub_slug:
                carpeta = "02_Instancias_SQL"
            else:
                carpeta = sec_slug

            sub_filename = f"{sub_slug}.md"
            route = f"{carpeta}/{sub_filename}"
            key = route.lower()
            if key in seen_paths:
                if not tolerant:
                    raise InvalidIndexSchemaError(f"Ruta duplicada: {route}")
                else:
                    continue
            seen_paths.add(key)
            lines.append(f"  * [{sub_title}]({route})")

    lines.append("")  # Línea vacía al final
    return lines


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
