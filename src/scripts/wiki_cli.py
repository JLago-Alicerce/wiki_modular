#!/usr/bin/env python
"""CLI unificada para las utilidades de wiki_modular."""
import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

from wiki_modular.config import load_config


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    """Execute ``cmd`` and abort on failure."""
    logging.info("Ejecutando: %s", " ".join(cmd))
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def step_convert(doc: Path, cfg: dict, env: dict[str, str]) -> None:
    tmp_md = Path(cfg["fuente_md"])
    wiki_dir = Path(cfg["wiki_dir"])
    cmd = [
        "pandoc",
        str(doc),
        "--from=docx",
        "--to=gfm",
        "--output=" + str(tmp_md),
        "--extract-media=" + str(wiki_dir / "assets"),
        "--markdown-headings=atx",
        "--standalone",
        "--wrap=none",
    ]
    run(cmd, env=env)
    run([sys.executable, "scripts/limpiar_md.py", str(tmp_md)], env=env)


def step_generate_index(cfg: dict, env: dict[str, str]) -> None:
    run(
        [
            sys.executable,
            "scripts/generar_mapa_encabezados.py",
            "--md",
            cfg["fuente_md"],
            "--out",
            cfg["mapa_file"],
        ],
        env=env,
    )
    run(
        [
            sys.executable,
            "scripts/generar_index_desde_encabezados.py",
            "--input",
            cfg["mapa_file"],
            "--output",
            cfg["index_file"],
            "--precheck",
        ],
        env=env,
    )


def step_ingest(cfg: dict, cutoff: float, env: dict[str, str]) -> None:
    run(
        [
            sys.executable,
            "scripts/ingest_wiki_v2.py",
            "--mapa",
            cfg["mapa_file"],
            "--index",
            cfg["index_file"],
            "--fuente",
            cfg["fuente_md"],
            "--alias",
            cfg["alias_file"],
            "--suggestions",
            cfg["suggestions"],
            "--cutoff",
            str(cutoff),
        ],
        env=env,
    )


def step_sidebar(cfg: dict, env: dict[str, str]) -> None:
    run(
        [
            sys.executable,
            "scripts/generar_sidebar.py",
            "--index",
            cfg["index_file"],
            "--out",
            cfg["sidebar_file"],
            "--tolerant",
        ],
        env=env,
    )
    run([sys.executable, "scripts/auditar_sidebar_vs_fs.py"], env=env)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Utilidades unificadas de wiki_modular"
    )
    sub = parser.add_subparsers(dest="command")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Archivo de configuraci\u00f3n del proyecto",
    )

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
    cfg = load_config(args.config)
    run_env = {**os.environ, "WIKI_CONFIG": str(args.config)}
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
    )

    if args.command == "full":
        run(
            [
                sys.executable,
                "scripts/resetear_entorno.py",
                "--config",
                str(args.config),
            ],
            env=run_env,
        )
        step_convert(args.doc, cfg, run_env)
        step_generate_index(cfg, run_env)
        step_ingest(cfg, args.cutoff, run_env)
        step_sidebar(cfg, run_env)
    elif args.command == "reset":
        run(
            [
                sys.executable,
                "scripts/resetear_entorno.py",
                "--config",
                str(args.config),
            ],
            env=run_env,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
