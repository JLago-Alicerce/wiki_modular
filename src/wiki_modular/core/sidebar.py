"""Funciones para generar el sidebar de la wiki."""

from pathlib import Path
from typing import Any, Dict, List

import yaml

from wiki_modular import limpiar_slug, load_yaml


class IndexFileNotFoundError(FileNotFoundError):
    """Señala que el archivo de índice no existe."""


class InvalidIndexSchemaError(Exception):
    """El contenido del índice no cumple el esquema mínimo esperado."""


def load_index(path: Path) -> Dict[str, Any]:
    """Carga y parsea el YAML de índice desde ``path``."""
    if not path.exists():
        raise IndexFileNotFoundError(f"No se encontró '{path.name}' en la ruta: {path}")
    datos = load_yaml(path)
    return datos if isinstance(datos, dict) else {}


def validate_index_schema(data: Dict[str, Any], *, tolerant: bool = False) -> None:
    """Valida que ``data`` cumpla el formato requerido por el índice."""
    if "secciones" not in data or not isinstance(data["secciones"], list):
        raise InvalidIndexSchemaError("El YAML debe contener clave 'secciones' como lista.")

    for idx, seccion in enumerate(data["secciones"], start=1):
        if not isinstance(seccion, dict):
            raise InvalidIndexSchemaError(
                f"La sección en posición {idx} no es un mapeo válido."
            )
        if "titulo" not in seccion:
            raise InvalidIndexSchemaError(f"Falta 'titulo' en la sección de índice {idx}.")
        if not tolerant and "id" not in seccion:
            raise InvalidIndexSchemaError(
                "Falta 'id' en la sección de índice "
                f"{idx} (ejecute con --tolerant para permitirlo)."
            )
        if "subtemas" in seccion and not isinstance(seccion["subtemas"], list):
            raise InvalidIndexSchemaError(
                f"'subtemas' en la sección {idx} debe ser lista."
            )


def slugify(text: str) -> str:
    """Versión interna que delega en :func:`limpiar_slug`."""
    return limpiar_slug(text)


def build_sidebar_lines(data: Dict[str, Any], *, tolerant: bool = False) -> List[str]:
    """Construye las líneas de ``_sidebar.md`` a partir de ``data``."""
    lines: List[str] = ["* [Inicio](README.md)"]
    secciones = data["secciones"]
    seen_paths = set()

    for seccion in secciones:
        sec_title = seccion["titulo"]
        sec_slug = seccion.get("slug", slugify(sec_title))
        sec_id = seccion.get("id")
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

        for sub in seccion.get("subtemas", []):
            sub_title = sub
            sub_slug = slugify(sub_title)
            if sub_slug == sec_slug:
                continue
            carpeta = "02_Instancias_SQL" if "sql" in sub_slug else sec_slug
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

    lines.append("")
    return lines


__all__ = [
    "IndexFileNotFoundError",
    "InvalidIndexSchemaError",
    "load_index",
    "validate_index_schema",
    "build_sidebar_lines",
]
