#!/usr/bin/env python
"""Reinicia y procesa todo el contenido de ``_fuentes/_originales``."""

import logging
import subprocess
import sys
from pathlib import Path

# Permitir ejecutar el script sin instalar el paquete
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR / "src"))

from scripts import procesar_nuevos as pn  # type: ignore


def run(cmd: list[str]) -> None:
    """Execute ``cmd`` aborting on error."""
    logging.info("Ejecutando: %s", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Comando fallido: {' '.join(cmd)}")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    # 1. Limpiar todo el entorno
    reset_script = Path(__file__).resolve().parent / "resetear_entorno.py"
    run([sys.executable, str(reset_script)])

    orig_dir = pn.ORIG_DIR
    if not orig_dir.exists():
        logging.info("Directorio %s no existe", orig_dir)
        return

    # 2. Procesar todos los PDFs
    for pdf in sorted(orig_dir.glob("*.pdf")):
        logging.info("Procesando PDF %s", pdf.name)
        md = pn.convertir_pdf(pdf)
        if not md:
            logging.info("Ignorando %s por errores", pdf.name)
            continue
        pn.run_pipeline(pdf, skip_pandoc=True)

    # 3. Procesar todos los DOCX
    for docx in sorted(orig_dir.glob("*.docx")):
        logging.info("Procesando DOCX %s", docx.name)
        pn.run_pipeline(docx)

    # 4. Generar índice de búsqueda
    idx_script = Path(__file__).resolve().parent / "generar_indice_busqueda.py"
    run([sys.executable, str(idx_script)])


if __name__ == "__main__":
    main()
