#!/usr/bin/env python
"""CLI unificada para las utilidades de wiki_modular."""
import argparse
import logging
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    """Execute ``cmd`` and abort on failure."""
    logging.info("Ejecutando: %s", " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


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
    run(cmd)
    run([sys.executable, "scripts/limpiar_md.py", str(tmp_md)])


def step_generate_index() -> None:
    run([sys.executable, "scripts/generar_mapa_encabezados.py"])
    run(
        [
            sys.executable,
            "scripts/generar_index_desde_encabezados.py",
            "--precheck",
        ]
    )


def step_ingest(cutoff: float) -> None:
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
    run([sys.executable, "scripts/generar_sidebar_desde_index.py"])
    run([sys.executable, "scripts/auditar_sidebar_vs_fs.py"])


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
        run([sys.executable, "scripts/resetear_entorno.py"])
        step_convert(args.doc)
        step_generate_index()
        step_ingest(args.cutoff)
        step_sidebar()
    elif args.command == "reset":
        run([sys.executable, "scripts/resetear_entorno.py"])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
