"""Submódulos centrales con funciones reutilizables."""

from .sidebar import load_index, validate_index_schema, build_sidebar_lines
from .ingest import buscar_destino, limpiar_nombre_archivo, append_suggestion
from .search import extraer_frontmatter, generar_indice

__all__ = [
    "load_index",
    "validate_index_schema",
    "build_sidebar_lines",
    "buscar_destino",
    "limpiar_nombre_archivo",
    "append_suggestion",
    "extraer_frontmatter",
    "generar_indice",
]
