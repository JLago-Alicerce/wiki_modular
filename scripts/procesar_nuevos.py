#!/usr/bin/env python
"""Procesa automáticamente nuevos archivos en ``_fuentes/_originales``.

Detecta documentos ``.docx`` y ``.pdf``. Los PDF legibles se convierten a DOCX
y se procesan con la misma cadena de scripts descrita en el README. Se mantiene
un registro en ``procesados.log`` para evitar reprocesos y se anotan los PDF con
errores en ``errores_pdf.csv``.
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

from pdfminer.high_level import extract_text

ORIG_DIR = Path('_fuentes/_originales')
LOG_FILE = Path('procesados.log')
PDF_ERRORS = Path('errores_pdf.csv')


PIPELINE = [
    lambda doc: [
        "pandoc",
        str(doc),
        "--from=docx",
        "--to=gfm",
        "--output=_fuentes/tmp_full.md",
        "--extract-media=wiki/assets",
        "--markdown-headings=atx",
        "--standalone",
        "--wrap=none",
    ],
    lambda _doc: [sys.executable, "scripts/limpiar_md.py", "_fuentes/tmp_full.md"],
    lambda _doc: [sys.executable, "scripts/generar_mapa_encabezados.py"],
    lambda _doc: [
        sys.executable,
        "scripts/generar_index_desde_encabezados.py",
        "--precheck",
        "--ignore-extra",
        "--output",
        "index_PlataformaBBDD.yaml",
    ],
    lambda _doc: [
        sys.executable,
        "scripts/ingest_wiki_v2.py",
        "--mapa",
        "_fuentes/mapa_encabezados.yaml",
        "--index",
        "index_PlataformaBBDD.yaml",
        "--fuente",
        "_fuentes/tmp_full.md",
        "--alias",
        "_fuentes/alias_override.yaml",
        "--cutoff",
        "0.5",
    ],
    lambda _doc: [sys.executable, "scripts/generar_sidebar.py", "--tolerant"],
    lambda _doc: [sys.executable, "scripts/auditar_sidebar_vs_fs.py"],
]


def load_log() -> Dict[str, str]:
    processed = {}
    if LOG_FILE.exists():
        for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
            try:
                entry = json.loads(line)
                processed[entry["file"]] = entry["processed_at"]
            except Exception:
                continue
    return processed


def append_log(filename: str) -> None:
    entry = {"file": filename, "processed_at": datetime.now().isoformat()}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def registrar_error_pdf(filename: str, error: str) -> None:
    """Añade ``filename,error`` a :data:`PDF_ERRORS`."""
    with PDF_ERRORS.open('a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([filename, error])


def convertir_pdf(pdf: Path) -> Path | None:
    """Convierte ``pdf`` a DOCX si es legible.

    Devuelve la ruta del DOCX generado o ``None`` si hay errores.
    """
    try:
        texto = extract_text(str(pdf))
        if not texto.strip():
            raise ValueError('sin texto extraído')
    except Exception as exc:  # noqa: BLE001
        registrar_error_pdf(pdf.name, str(exc))
        logging.error('No se pudo leer %s: %s', pdf.name, exc)
        return None

    docx_path = pdf.with_suffix('.docx')
    cmd = ['pandoc', str(pdf), '-o', str(docx_path)]
    logging.info('Convirtiendo %s a %s', pdf.name, docx_path.name)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        registrar_error_pdf(pdf.name, 'pandoc error')
        logging.error('Fallo convirtiendo %s', pdf.name)
        return None
    return docx_path


def run_pipeline(doc: Path) -> None:
    for build_cmd in PIPELINE:
        cmd = build_cmd(doc)
        logging.info("Ejecutando: %s", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            raise RuntimeError(f"Paso fallido: {' '.join(cmd)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Procesa automáticamente nuevos .docx o .pdf"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Ejecutar resetear_entorno.py antes de procesar",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    if args.clean:
        logging.info("Limpiando entorno previo")
        rc = subprocess.run([sys.executable, "scripts/resetear_entorno.py"]).returncode
        if rc != 0:
            raise RuntimeError("resetear_entorno.py fallo")

    processed = load_log()

    # Convertir PDFs a DOCX antes de buscar nuevos archivos
    for pdf in sorted(ORIG_DIR.glob('*.pdf')):
        docx_dest = pdf.with_suffix('.docx')
        if not docx_dest.exists():
            convertir_pdf(pdf)

    new_files = []

    for doc in sorted(ORIG_DIR.glob("*.docx")):
        if doc.name in processed:
            logging.info("Ya procesado %s en %s", doc.name, processed[doc.name])
        else:
            new_files.append(doc)

    if not new_files:
        logging.info("No hay archivos nuevos en %s", ORIG_DIR)
        return

    for doc in new_files:
        logging.info("Procesando %s", doc.name)
        try:
            run_pipeline(doc)
        except Exception as e:
            logging.error("Error procesando %s: %s", doc.name, e)
            raise
        else:
            append_log(doc.name)
            logging.info("Procesado correctamente: %s", doc.name)


if __name__ == "__main__":
    main()
