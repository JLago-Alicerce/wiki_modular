#!/usr/bin/env python
"""Normaliza estilos de encabezado en archivos .docx.

Detecta numeraciones como ``1.``, ``2.1.``, ``3.4.5.`` y aplica
autom\u00e1ticamente los estilos ``T\u00edtulo 1``, ``T\u00edtulo 2`` y
``T\u00edtulo 3`` sobre el documento resultante. Es idempotente y
puede ejecutarse varias veces sin degradar los estilos existentes.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from docx import Document


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detecta encabezados numerados y aplica estilos Word"
    )
    parser.add_argument("file", type=Path, help="Documento .docx a normalizar")
    parser.add_argument(
        "--dry-run", action="store_true", help="Mostrar títulos detectados"
    )
    args = parser.parse_args()

    doc = Document(str(args.file))
    headings: list[tuple[str, str]] = []

    patterns = [
        (r"^\d+\.\d+\.\d+\.\s", "Heading 3", "T\u00edtulo 3"),
        (r"^\d+\.\d+\.\s", "Heading 2", "T\u00edtulo 2"),
        (r"^\d+\.\s", "Heading 1", "T\u00edtulo 1"),
    ]

    for para in doc.paragraphs:
        text = para.text.strip()
        matched = False
        for pattern, style_name, label in patterns:
            if re.match(pattern, text):
                headings.append((style_name, text))
                matched = True
                if not args.dry_run and para.style.name != style_name:
                    para.style = style_name
                    print(f"[\u2713] Se aplic\u00f3 {label}: \"{text}\"")
                break

        if matched:
            continue

        if para.runs and para.runs[0].bold and len(text.split()) < 12:
            headings.append(("Heading 2", text))
            if not args.dry_run and para.style.name != "Heading 2":
                para.style = "Heading 2"
                print(f"[\u2713] Se aplic\u00f3 T\u00edtulo 2: \"{text}\"")

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
