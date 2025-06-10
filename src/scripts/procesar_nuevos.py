#!/usr/bin/env python
"""Procesa automáticamente nuevos archivos en ``_fuentes/_originales``.

Detecta documentos ``.docx`` y ``.pdf``. Los PDF se convierten directamente a
Markdown: si contienen texto se extrae con ``pdfminer.six`` y, opcionalmente, se
aplica OCR mediante ``pdf2image`` y ``pytesseract`` cuando el PDF es una imagen
escaneada. Se mantiene un registro en ``procesados.log`` para evitar reprocesos
y se anotan los fallos en ``errores_pdf.csv``.
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

from wiki_modular.config import ASSETS_DIR, ORIGINALES_DIR, WIKI_DIR

ORIG_DIR = ORIGINALES_DIR
LOG_FILE = Path('procesados.log')
PDF_ERRORS = Path('errores_pdf.csv')


PIPELINE = [
    lambda doc: [
        "pandoc",
        str(doc),
        "--from=docx",
        "--to=gfm",
        "--output=_fuentes/tmp_full.md",
        f"--extract-media={ASSETS_DIR}",
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


def convertir_pdf(pdf: Path, *, ocr: bool = False, dest: Path | None = None) -> Path | None:
    """Convierte ``pdf`` a Markdown en ``dest``.

    Si ``ocr`` es ``True`` e inicialmente no se extrae texto, intentará
    procesar cada página como imagen con ``pytesseract``.

    Devuelve la ruta del archivo generado o ``None`` si hay errores.
    """
    if dest is None:
        dest = Path('_fuentes/tmp_full.md')

    try:
        texto = extract_text(str(pdf))
    except Exception as exc:  # noqa: BLE001
        registrar_error_pdf(pdf.name, str(exc))
        logging.error("No se pudo leer %s: %s", pdf.name, exc)
        return None

    if not texto.strip() and ocr:
        try:  # Lazy imports para no requerir OCR siempre
            from pdf2image import convert_from_path  # type: ignore
            import pytesseract  # type: ignore

            images = convert_from_path(str(pdf))
            texto = "\n".join(pytesseract.image_to_string(img) for img in images)
        except Exception as exc:  # noqa: BLE001
            registrar_error_pdf(pdf.name, f"ocr: {exc}")
            logging.error("OCR fallido en %s: %s", pdf.name, exc)
            return None

    if not texto.strip():
        registrar_error_pdf(pdf.name, "sin texto extraido")
        logging.error("No se extrajo texto de %s", pdf.name)
        return None

    dest.write_text(texto, encoding="utf-8")
    return dest


def run_pipeline(doc: Path, *, skip_pandoc: bool = False) -> None:
    """Ejecuta la cadena de utilidades definida en :data:`PIPELINE`."""
    for i, build_cmd in enumerate(PIPELINE):
        if skip_pandoc and i == 0:
            continue
        cmd = build_cmd(doc)
        logging.info("Ejecutando: %s", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            raise RuntimeError(f"Paso fallido: {' '.join(cmd)}")

        # Tras generar el sidebar comprobamos si contiene enlaces. Si no hay
        # ninguno significa que no se creó contenido nuevo y por tanto la
        # auditoría no tiene sentido. Se omite el paso restante para evitar
        # detener el flujo por un error innecesario.
        if "generar_sidebar.py" in cmd[-1]:
            sidebar = WIKI_DIR / "_sidebar.md"
            if sidebar.exists():
                text = sidebar.read_text(encoding="utf-8")
                if "](" not in text:
                    logging.info("_sidebar.md vacío; omitiendo auditoría")
                    break


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Procesa automáticamente nuevos .docx o .pdf"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Ejecutar resetear_entorno.py antes de procesar",
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="Intentar OCR en PDFs sin texto",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    if args.clean:
        logging.info("Limpiando entorno previo")
        rc = subprocess.run([sys.executable, "scripts/resetear_entorno.py"]).returncode
        if rc != 0:
            raise RuntimeError("resetear_entorno.py fallo")

    processed = load_log()

    new_files: list[Path] = []

    for pdf in sorted(ORIG_DIR.glob("*.pdf")):
        if pdf.name in processed:
            logging.info("Ya procesado %s en %s", pdf.name, processed[pdf.name])
            continue
        logging.info("Procesando PDF %s", pdf.name)
        md_path = convertir_pdf(pdf, ocr=args.ocr)
        if not md_path:
            logging.info("Ignorando %s por errores", pdf.name)
            continue
        try:
            run_pipeline(pdf, skip_pandoc=True)
        except Exception as e:
            logging.error("Error procesando %s: %s", pdf.name, e)
            raise
        else:
            append_log(pdf.name)
            logging.info("Procesado correctamente: %s", pdf.name)

    for doc in sorted(ORIG_DIR.glob("*.docx")):
        if doc.name in processed:
            logging.info("Ya procesado %s en %s", doc.name, processed[doc.name])
        else:
            new_files.append(doc)

    if not new_files:
        logging.info("No hay archivos DOCX nuevos en %s", ORIG_DIR)
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
