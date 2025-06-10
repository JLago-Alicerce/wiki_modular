#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Herramienta para comparar versiones de un Markdown.

Genera un diff lateral en HTML cargando la versión previa desde un
archivo de backup o desde Git.
"""

from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
import webbrowser
from pathlib import Path

from utils.entorno import add_src_to_path

add_src_to_path()


# --------------------------------------------------
def load_from_git(path: Path, revision: str) -> str:
    """Devuelve el contenido de ``path`` en ``revision`` usando ``git show``."""
    try:
        result = subprocess.run(
            ["git", "show", f"{revision}:{path.as_posix()}"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as exc:  # pragma: no cover - errors are fatal
        raise RuntimeError(f"No se pudo cargar {path} en {revision}") from exc


# --------------------------------------------------
def make_diff_html(old_text: str, new_text: str) -> str:
    """Genera un diff en HTML para ``old_text`` y ``new_text``."""
    diff = difflib.HtmlDiff(wrapcolumn=80)
    return diff.make_file(
        old_text.splitlines(),
        new_text.splitlines(),
        fromdesc="Anterior",
        todesc="Actual",
    )


# --------------------------------------------------
def main() -> None:
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Comparar versiones de un Markdown y mostrar un diff",
    )
    parser.add_argument("archivo", type=Path, help="Archivo Markdown actual")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--backup",
        type=Path,
        help="Ruta al archivo de respaldo a comparar",
    )
    group.add_argument(
        "--rev",
        default="HEAD^",
        help="Revisión de Git a comparar (por defecto HEAD^)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("_tmp/diff.html"),
        help="Archivo HTML de salida",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="No abrir el navegador automáticamente",
    )
    args = parser.parse_args()

    if not args.archivo.exists():
        print(f"[X] No existe {args.archivo}", file=sys.stderr)
        sys.exit(1)

    new_text = args.archivo.read_text(encoding="utf-8")

    if args.backup:
        if not args.backup.exists():
            print(f"[X] No existe {args.backup}", file=sys.stderr)
            sys.exit(1)
        old_text = args.backup.read_text(encoding="utf-8")
    else:
        try:
            old_text = load_from_git(args.archivo, args.rev)
        except RuntimeError as exc:
            print(f"[X] {exc}", file=sys.stderr)
            sys.exit(1)

    html = make_diff_html(old_text, new_text)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"✅ Diff guardado en {args.out}")
    if not args.no_open:
        webbrowser.open(args.out.resolve().as_uri())


if __name__ == "__main__":
    main()
