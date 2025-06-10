#!/usr/bin/env python
"""Normaliza estilos de encabezado en archivos .docx."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from docx import Document


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detecta títulos simulados y aplica estilos Word"
    )
    parser.add_argument("file", type=Path, help="Documento .docx a normalizar")
    parser.add_argument(
        "--dry-run", action="store_true", help="Mostrar títulos detectados"
    )
    args = parser.parse_args()

    doc = Document(str(args.file))
    headings: list[tuple[str, str]] = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if re.match(r"^\d+\.\s", text):
            headings.append(("H1", text))
            if not args.dry_run:
                para.style = "Heading 1"
        elif re.match(r"^\d+\.\d+\s", text):
            headings.append(("H2", text))
            if not args.dry_run:
                para.style = "Heading 2"
        elif para.runs and para.runs[0].bold and len(text.split()) < 12:
            headings.append(("H2", text))
            if not args.dry_run:
                para.style = "Heading 2"

    if args.dry_run:
        for level, title in headings:
            print(f"{level}: {title}")
        return

    dest_dir = args.file.parent.parent / "_originales_normalizados"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / args.file.name
    doc.save(dest)


if __name__ == "__main__":
    main()
