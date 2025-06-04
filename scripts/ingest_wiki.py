#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fragmenta un Markdown completo (tmp_full.md) en múltiples archivos .md,
usando un mapa de encabezados y un índice maestro. Asimismo, acepta overrides
manuales y fuzzy matching con corte configurable.
"""

import sys
import yaml
import re
import unicodedata
import logging
import argparse
from pathlib import Path
from difflib import get_close_matches

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def normalize_slug(text: str) -> str:
    """
    Convierte el texto a un slug:
      - Normaliza a NFKD (elimina acentos).
      - Convierte a ASCII descartando lo no mapeable.
      - Elimina caracteres no alfanuméricos, espacios o guiones.
      - Reemplaza secuencias de espacios o guiones por "_".
      - Convierte a minúsculas.
    """
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^A-Za-z0-9\s-]", "", ascii_text)
    underscored = re.sub(r"[\s-]+", "_", cleaned).strip("_")
    return underscored.lower()

def buscar_destino(titulo: str, index_data: dict, alias_map: dict, fuzzy_cutoff: float) -> Path:
    """
    Decide la ruta destino para un bloque:
      1) Si título EXACTO está en alias_map → devuelve Path(alias_map[título]).
      2) Sino, construye un mapa de “clave normalizada” → Path desde index_data.
      3) Aplica fuzzy matching sobre las claves con cutoff; devuelve match si existe.
      4) Si no hay match, retorna None.
    """
    # 1) Override manual
    if titulo in alias_map:
        return Path(alias_map[titulo])

    # 2) Construir diccionario de slugs desde índice
    ruta_map = {}
    candidatos = []

    for sec in index_data.get("secciones", []):
        sec_titulo = sec.get("titulo", "")
        sec_slug = sec.get("slug", normalize_slug(sec_titulo))
        id_prefix = f"{sec.get('id')}_{sec_slug}" if "id" in sec else sec_slug

        # Ruta de sección principal
        key_sec = normalize_slug(sec_titulo)
        ruta_map[key_sec] = Path(f"wiki/{id_prefix}.md")
        candidatos.append(key_sec)

        # Cada subtema (si existe)
        for sub in sec.get("subtemas", []):
            key_sub = normalize_slug(sub)
            # Si sub contiene “sql”, carpeta específica; else carpeta = slug de sección
            carpeta = "02_Instancias_SQL" if "sql" in key_sub else sec_slug
            ruta_map[key_sub] = Path(f"wiki/{carpeta}/{normalize_slug(sub)}.md")
            candidatos.append(key_sub)

    # 3) Fuzzy matching
    titulo_norm = normalize_slug(titulo)
    match = get_close_matches(titulo_norm, candidatos, n=1, cutoff=fuzzy_cutoff)
    if match:
        return ruta_map[match[0]]

    logging.warning(f"No match para '{titulo}' → normalizado: '{titulo_norm}'")
    return None

def limpiar_nombre_archivo(texto: str) -> str:
    """
    Para bloques sin destino, crea un nombre de archivo a partir del título:
      - Normaliza a ASCII, quita numeración inicial, elimina caracteres no válidos,
        reemplaza espacios/guiones por "_", evita duplicados de "_", y limita a 128 caracteres.
    """
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii").strip()
    texto = re.sub(r"^[0-9.]+\s*", "", texto)
    texto = re.sub(r'[\\/:*?"<>|]', "", texto)
    texto = re.sub(r'[\s-]+', '_', texto)
    texto = re.sub(r'_+', '_', texto).strip('_')
    return texto[:128]

def main():
    parser = argparse.ArgumentParser(description="Fragmenta tmp_full.md según mapa e índice.")
    parser.add_argument("--mapa",    default="_fuentes/mapa_encabezados.yaml", help="YAML de encabezados")
    parser.add_argument("--index",   default="index_PlataformaBBDD.yaml",    help="Índice maestro YAML")
    parser.add_argument("--fuente",  default="_fuentes/tmp_full.md",         help="Markdown completo")
    parser.add_argument("--alias",   default="_fuentes/alias_override.yaml", help="Overrides YAML (opcional)")
    parser.add_argument("--cutoff",  type=float, default=0.4,                help="Umbral fuzzy matching")
    args = parser.parse_args()

    wiki_path     = Path("wiki")
    mapa_file     = Path(args.mapa)
    index_file    = Path(args.index)
    tmp_file      = Path(args.fuente)
    override_file = Path(args.alias)

    # 1) Cargar alias_override (si existe)
    alias_map = {}
    if override_file.exists():
        try:
            raw_override = override_file.read_text(encoding="utf-8")
            safe_override = raw_override.replace(r"\>", r"\\>")
            alias_map = yaml.safe_load(safe_override) or {}
        except yaml.YAMLError as e:
            logging.error(f"Error parseando alias_override.yaml: {e}")

    # 2) Cargar mapa, índice y líneas de markdown
    try:
        mapa = yaml.safe_load(mapa_file.read_text(encoding="utf-8"))
        index_data = yaml.safe_load(index_file.read_text(encoding="utf-8"))
        tmp_lines = tmp_file.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        logging.critical(f"Error al cargar archivos: {e}")
        sys.exit(1)

    assert isinstance(mapa, list), "mapa_encabezados.yaml debe ser una lista"
    bloques = []

    # 3) Fragmentar en bloques según start_line/end_line
    for i, sec in enumerate(mapa):
        start = sec.get("start_line", 0) - 1
        end = (mapa[i + 1].get("start_line", len(tmp_lines)+1) - 1) if (i + 1) < len(mapa) else len(tmp_lines)
        titulo = sec.get("titulo") or sec.get("title")
        nivel = sec.get("h_level", 1)

        if not titulo:
            logging.warning(f"Bloque sin 'titulo': {sec}")
            continue
        if start < 0 or end > len(tmp_lines):
            logging.warning(f"Rango inválido ({start}, {end}) en '{titulo}'")
            continue

        bloques.append((titulo, nivel, tmp_lines[start:end]))

    # 4) Escribir cada bloque en su ruta destino (o 99_Nuevas_Secciones si no hay match)
    no_match_count = 0
    for titulo, nivel, contenido in bloques:
        destino = buscar_destino(titulo, index_data, alias_map, fuzzy_cutoff=args.cutoff)
        if not destino:
            # Asignar a carpeta wildcard
            nombre_def = limpiar_nombre_archivo(titulo)
            destino = wiki_path / "99_Nuevas_Secciones" / f"{nombre_def}.md"
            no_match_count += 1

        destino.parent.mkdir(parents=True, exist_ok=True)
        md_texto = f"{'#' * nivel} {titulo}\n\n" + "\n".join(contenido)
        destino.write_text(md_texto, encoding="utf-8")
        logging.info(f"[✓] {titulo} → {destino}")

    logging.info(f"Resumen: {len(bloques)} bloques procesados | {no_match_count} sin coincidencia")

if __name__ == "__main__":
    main()
