#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import yaml
import re
import unicodedata
import logging
import argparse
from pathlib import Path
from difflib import get_close_matches

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def normalizar(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
    txt = re.sub(r"[^a-z0-9\s]+", " ", txt.lower())
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def limpiar_nombre_archivo(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.strip()
    texto = re.sub(r"^[0-9.]+\s*", "", texto)
    texto = re.sub(r'[\\/:*?"<>|]', "", texto)
    texto = re.sub(r'[\s\-]+', '_', texto)
    texto = re.sub(r'_+', '_', texto)
    texto = texto.strip('_')
    return texto[:128]

def buscar_destino(titulo: str, index_data: dict, alias_map: dict, fuzzy_cutoff: float) -> Path:
    if titulo in alias_map:
        return Path(alias_map[titulo])

    ruta_map = {}
    candidatos = []

    for sec in index_data.get("secciones", []):
        sec_key = normalizar(sec.get("titulo", ""))
        slug = sec.get("slug", limpiar_nombre_archivo(sec.get("titulo", "")))
        id_prefix = f"{sec.get('id')}_{slug}" if "id" in sec else slug
        ruta_map[sec_key] = Path(f"wiki/{id_prefix}.md")
        candidatos.append(sec_key)

        for sub in sec.get("subtemas", []):
            sub_key = normalizar(sub)
            carpeta = "02_Instancias_SQL" if "sql" in sub_key else slug
            ruta_map[sub_key] = Path(f"wiki/{carpeta}/{sub.replace(' ', '_')}.md")
            candidatos.append(sub_key)

    titulo_norm = normalizar(titulo)
    coincidencia = get_close_matches(titulo_norm, candidatos, n=1, cutoff=fuzzy_cutoff)

    if coincidencia:
        return ruta_map[coincidencia[0]]

    logging.warning(f"No match for: '{titulo}' → normalizado: '{titulo_norm}'")
    return None

def main():
    parser = argparse.ArgumentParser(description="Fragmenta tmp_full.md según mapa e índice.")
    parser.add_argument("--mapa", default="_fuentes/mapa_encabezados.yaml")
    parser.add_argument("--index", default="index_PlataformaBBDD.yaml")
    parser.add_argument("--fuente", default="_fuentes/tmp_full.md")
    parser.add_argument("--alias", default="_fuentes/alias_override.yaml")
    parser.add_argument("--cutoff", type=float, default=0.4)
    args = parser.parse_args()

    wiki_path = Path("wiki")
    mapa_file = Path(args.mapa)
    index_file = Path(args.index)
    tmp_file = Path(args.fuente)
    override_file = Path(args.alias)

    alias_map = {}
    if override_file.exists():
        try:
            raw_override = override_file.read_text(encoding="utf-8")
            safe_override = raw_override.replace(r"\>", r"\\>")
            alias_map = yaml.safe_load(safe_override) or {}
        except yaml.YAMLError as e:
            logging.error(f"Error al parsear alias_override.yaml: {e}")

    try:
        mapa = yaml.safe_load(mapa_file.read_text(encoding="utf-8"))
        index_data = yaml.safe_load(index_file.read_text(encoding="utf-8"))
        tmp_lines = tmp_file.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        logging.critical(f"Error crítico al cargar archivos: {e}")
        sys.exit(1)

    assert isinstance(mapa, list), "mapa_encabezados.yaml debe contener una lista"
    bloques = []
    for i, sec in enumerate(mapa):
        start = sec.get("start_line", 0) - 1
        end = mapa[i + 1].get("start_line", len(tmp_lines)+1) - 1 if (i + 1) < len(mapa) else len(tmp_lines)
        titulo = sec.get("titulo") or sec.get("title")
        nivel = sec.get("h_level", 1)
        if not titulo:
            logging.warning(f"[!] Entrada sin 'titulo': {sec}")
            continue
        if start < 0 or end > len(tmp_lines):
            logging.warning(f"Rango inválido en bloque ({start}, {end}) – '{titulo}'")
            continue
        bloques.append((titulo, nivel, tmp_lines[start:end]))

    no_match = 0
    for titulo, nivel, contenido in bloques:
        destino = buscar_destino(titulo, index_data, alias_map, fuzzy_cutoff=args.cutoff)
        if not destino:
            destino = wiki_path / "99_Nuevas_Secciones" / f"{limpiar_nombre_archivo(titulo)}.md"
            no_match += 1

        destino.parent.mkdir(parents=True, exist_ok=True)
        md_texto = f"{'#' * nivel} {titulo}\n\n" + "\n".join(contenido)
        destino.write_text(md_texto, encoding="utf-8")
        logging.info(f"[✓] {titulo} → {destino}")

    logging.info(f"Resumen final: {len(bloques)} bloques procesados | {no_match} sin coincidencia")

if __name__ == "__main__":
    main()
