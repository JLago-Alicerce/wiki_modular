"""Herramientas para generar el índice de búsqueda."""

import json
from pathlib import Path
from typing import Dict, Tuple

import yaml


def extraer_frontmatter(path: Path) -> Tuple[Dict[str, str], str]:
    """Devuelve la metadata y el cuerpo de un archivo Markdown."""
    texto = path.read_text(encoding="utf-8")
    if texto.startswith("---"):
        partes = texto.split("---", 2)
        if len(partes) >= 3:
            try:
                meta = yaml.safe_load(partes[1]) or {}
            except yaml.YAMLError:
                meta = {}
            cuerpo = partes[2].lstrip("\n")
            return meta, cuerpo
    return {}, texto


def generar_indice(wiki_dir: Path) -> Dict[str, Dict[str, object]]:
    """Recorre ``wiki_dir`` y construye un diccionario utilizable por Docsify."""
    indice: Dict[str, Dict[str, object]] = {}
    for md in wiki_dir.rglob("*.md"):
        meta, cuerpo = extraer_frontmatter(md)
        indice[str(md.relative_to(wiki_dir))] = {"metadata": meta, "content": cuerpo}
    return indice


__all__ = ["extraer_frontmatter", "generar_indice"]
