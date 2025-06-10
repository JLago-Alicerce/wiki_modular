#!/usr/bin/env python
"""CLI unificada para las utilidades de wiki_modular."""
import argparse
import logging
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    """Execute ``cmd`` and abort on failure."""
    logging.info("Ejecutando: %s", " ".join(str(c) for c in cmd))
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError as exc:
        logging.error("Comando no encontrado: %s", cmd[0])
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        logging.error("El comando falló (%s): %s", exc.returncode, " ".join(exc.cmd))
        raise SystemExit(exc.returncode) from exc


def step_convert(doc: Path) -> None:
    tmp_md = Path("_fuentes/tmp_full.md")
    cmd = [
        "pandoc",
        str(doc),
        "--from=docx",
        "--to=gfm",
        "--output=" + str(tmp_md),
        "--extract-media=wiki/assets",
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
    try:
        run([sys.executable, "scripts/generar_mapa_encabezados.py"])
        run(
            [
                sys.executable,
                "scripts/generar_index_desde_encabezados.py",
                "--precheck",
            ]
        )
    except Exception as exc:
        logging.error("Error al generar índices: %s", exc)
        raise


def step_ingest(cutoff: float) -> None:
    try:
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
    except Exception as exc:
        logging.error("Error en la ingesta: %s", exc)
        raise


def step_sidebar() -> None:
    try:
        run([sys.executable, "scripts/generar_sidebar.py", "--tolerant"])
        run([sys.executable, "scripts/auditar_sidebar_vs_fs.py"])
    except Exception as exc:
        logging.error("Error al generar el sidebar: %s", exc)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Utilidades unificadas de wiki_modular"
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
