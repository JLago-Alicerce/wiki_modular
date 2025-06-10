#!/usr/bin/env python
"""CLI unificada para las utilidades de wiki_modular."""
import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

import wiki_modular.config as config

from utils.entorno import run as exec_cmd


def run(cmd: list[str]) -> None:
    """Execute ``cmd`` using :func:`utils.entorno.run`."""
    exec_cmd(cmd)




def step_convert(doc: Path) -> None:
    """Convierte ``doc`` a Markdown y lo limpia."""
    tmp_md = Path("_fuentes/tmp_full.md")
    cmd = [
        "pandoc",
        str(doc),
        "--from=docx",
        "--to=gfm",
        "--output=" + str(tmp_md),
        f"--extract-media={config.ASSETS_DIR}",
        "--markdown-headings=atx",
        "--standalone",
        "--wrap=none",
    ]
    try:
        run(cmd)
        run([sys.executable, "scripts/limpiar_md.py", str(tmp_md)])
    except Exception as exc:
        logging.error("Fallo en la conversi\u00f3n: %s", exc)
        raise


def step_generate_index() -> None:

    """Genera mapa de encabezados e índice maestro."""
    run([sys.executable, "scripts/generar_mapa_encabezados.py"])
    run(
        [
            sys.executable,
            "scripts/generar_index_desde_encabezados.py",
            "--precheck",
        ]
    )


def step_ingest(cutoff: float) -> None:
    """Fragmenta la wiki utilizando ``cutoff`` para fuzzy matching."""
    run(
        [
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
            str(cutoff),
        ]
    )


def step_sidebar() -> None:
    """Genera el sidebar y ejecuta la auditoría básica."""
    run([sys.executable, "scripts/generar_sidebar.py", "--tolerant"])
    run([sys.executable, "scripts/auditar_sidebar_vs_fs.py"])




def main() -> None:
    """Punto de entrada principal de la CLI unificada."""
    parser = argparse.ArgumentParser(
        description="Utilidades unificadas de wiki_modular"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Archivo de configuraci\u00f3n a utilizar",
    )
    sub = parser.add_subparsers(dest="command")

    full = sub.add_parser(
        "full",
        help="Ejecutar flujo completo a partir de un .docx",
    )
    full.add_argument("doc", type=Path, help="Archivo .docx de entrada")
    full.add_argument(
        "--cutoff",
        type=float,
        default=0.5,
        help="Umbral fuzzy matching",
    )

    sub.add_parser("reset", help="Limpiar entorno de trabajo")

    args = parser.parse_args()

    if args.config:
        os.environ["WM_CONFIG"] = str(args.config)
        config.load_config(args.config)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
    )

    if args.command == "full":
        if not args.doc.exists() or not args.doc.is_file():
            parser.error(f"El archivo {args.doc} no existe")
        if args.doc.suffix.lower() != ".docx":
            parser.error("El documento debe tener extensi\u00f3n .docx")
        if not 0 <= args.cutoff <= 1:
            parser.error("--cutoff debe estar entre 0 y 1")

        try:
            run([sys.executable, "scripts/resetear_entorno.py"])
            step_convert(args.doc)
            step_generate_index()
            step_ingest(args.cutoff)
            step_sidebar()
        except Exception as exc:
            logging.error("Ejecución interrumpida: %s", exc)
            raise SystemExit(1)
    elif args.command == "reset":
        run([sys.executable, "scripts/resetear_entorno.py"])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
