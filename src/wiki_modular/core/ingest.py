"""Funciones comunes utilizadas durante la ingesta de la wiki."""

import csv
import logging
import re
import unicodedata
from difflib import get_close_matches
from pathlib import Path
from typing import Any

import yaml

from wiki_modular import limpiar_slug, load_yaml

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def buscar_destino(
    titulo: str, index_data: dict, alias_map: dict, fuzzy_cutoff: float
) -> Path:
    """Determina la ruta destino para un bloque de contenido."""
    if titulo in alias_map:
        return Path(alias_map[titulo])

    ruta_map: dict[str, Path] = {}
    candidatos: list[str] = []
    for sec in index_data.get("secciones", []):
        sec_titulo = sec.get("titulo", "")
        sec_slug = sec.get("slug", limpiar_slug(sec_titulo))
        id_prefix = f"{sec.get('id')}_{sec_slug}" if "id" in sec else sec_slug
        key_sec = limpiar_slug(sec_titulo)
        ruta_map[key_sec] = Path(f"wiki/{id_prefix}.md")
        candidatos.append(key_sec)
        for sub in sec.get("subtemas", []):
            key_sub = limpiar_slug(sub)
            carpeta = "02_Instancias_SQL" if "sql" in key_sub else sec_slug
            ruta_map[key_sub] = Path(f"wiki/{carpeta}/{limpiar_slug(sub)}.md")
            candidatos.append(key_sub)

    titulo_norm = limpiar_slug(titulo)
    match = get_close_matches(titulo_norm, candidatos, n=1, cutoff=fuzzy_cutoff)
    if match:
        return ruta_map[match[0]]

    logging.warning("No match para '%s' → normalizado: '%s'", titulo, titulo_norm)
    return None


def limpiar_nombre_archivo(texto: str) -> str:
    """Genera un nombre de archivo válido a partir de ``texto``."""
    texto = (
        unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii").strip()
    )
    texto = re.sub(r"^[0-9.]+\s*", "", texto)
    texto = re.sub(r'[\\/:*?"<>|]', "", texto)
    texto = re.sub(r"[\s-]+", "_", texto)
    texto = re.sub(r"_+", "_", texto).strip("_")
    return texto[:128]


def append_suggestion(path: Path, titulo: str, slug: str) -> None:
    """Guarda ``titulo`` y ``slug`` en ``path`` si es posible."""
    try:
        if path.suffix.lower() in {".yaml", ".yml"}:
            data: dict[str, Any] = {}
            if path.exists():
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if titulo not in data:
                data[titulo] = slug
                path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        else:
            new_file = not path.exists()
            with path.open("a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if new_file:
                    writer.writerow(["titulo", "slug"])
                writer.writerow([titulo, slug])
    except Exception as e:  # pragma: no cover - solo logueo
        logging.error("No se pudo actualizar %s: %s", path, e)


__all__ = ["buscar_destino", "limpiar_nombre_archivo", "append_suggestion"]
