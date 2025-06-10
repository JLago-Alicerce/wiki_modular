#!/usr/bin/env python
"""Combina archivos Markdown de una carpeta y genera un PDF usando Pandoc."""
import argparse
import subprocess
from pathlib import Path


def main() -> None:
    """Combina los ``.md`` de una carpeta en un único PDF."""
    parser = argparse.ArgumentParser(description="Exportar carpeta de Markdown a PDF")
    parser.add_argument("carpeta", type=Path, help="Ruta de la carpeta con .md")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("salida.pdf"),
        help="Archivo PDF de salida",
    )
    args = parser.parse_args()

    md_files = sorted(args.carpeta.glob("*.md"))
    if not md_files:
        parser.error(f"No se encontraron archivos Markdown en {args.carpeta}")

    cmd = ["pandoc", *[str(p) for p in md_files], "-o", str(args.output)]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
