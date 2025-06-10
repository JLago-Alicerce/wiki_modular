#!/usr/bin/env python
"""Pipeline de publicación Codex.

Ejecuta de forma ordenada los pasos para generar la wiki desde un DOCX.
"""
import argparse
import logging
import subprocess
import sys
from pathlib import Path

from wiki_modular.config import ASSETS_DIR


def run(cmd: list[str]) -> int:
    """Execute a command and return its exit code."""

    logging.info("$ %s", " ".join(cmd))
    result = subprocess.run(cmd)
    logging.info("return code: %s", result.returncode)
    return result.returncode


def main() -> None:
    """Run the full wiki generation pipeline."""

    parser = argparse.ArgumentParser(
        description="Ejecuta pipeline completo de Codex",
    )
    parser.add_argument("docx", type=Path, help="Archivo DOCX de entrada")
    parser.add_argument(
        "--cutoff",
        type=float,
        default=0.5,
        help="Umbral fuzzy matching",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
    )

    steps = [
        (
            "convertir_docx",
            [
                "pandoc",
                str(args.docx),
                "--from=docx",
                "--to=gfm",
                "--output=_fuentes/tmp_full.md",
                f"--extract-media={ASSETS_DIR}",
                "--markdown-headings=atx",
                "--standalone",
                "--wrap=none",
            ],
        ),
        (
            "limpiar_md",
            [sys.executable, "scripts/limpiar_md.py", "_fuentes/tmp_full.md"],
        ),
        (
            "mapa_encabezados",
            [sys.executable, "scripts/generar_mapa_encabezados.py"],
        ),
        (
            "generar_index",
            [sys.executable, "scripts/generar_index_desde_encabezados.py"],
        ),
    ]

    for name, cmd in steps:
        logging.info("=== %s ===", name)
        rc = run(cmd)
        if rc != 0:
            sys.exit(rc)

    input(
        "\nRevisar mapa e índice antes de ingerir. "
        "Pulsa Enter para continuar o Ctrl+C para abortar..."
    )

    ingest_cmd = [
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
        str(args.cutoff),
    ]
    logging.info("=== ingestar ===")
    rc = run(ingest_cmd)
    if rc != 0:
        sys.exit(rc)

    final_steps = [
        (
            "generar_sidebar",
            # Genera el _sidebar.md a partir del índice
            [sys.executable, "scripts/generar_sidebar.py"],
        ),
        (
            "validar_enlaces",
            [sys.executable, "scripts/validar_sidebar_vs_fs.py"],
        ),
        (
            "limpiar_huerfanos",
            [sys.executable, "scripts/clean_orphaned_files.py"],
        ),
    ]

    for name, cmd in final_steps:
        logging.info("=== %s ===", name)
        rc = run(cmd)
        if rc != 0:
            sys.exit(rc)

    logging.info("Pipeline completado correctamente")


if __name__ == "__main__":
    main()
