#!/usr/bin/env python
"""Asistente paso a paso para publicar un documento.

Guía al usuario a través de cuatro fases:
(1) Cargar, (2) Procesar, (3) Revisar y (4) Publicar.
Permite avanzar, retroceder o repetir cada paso.
"""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]


class Wizard:
    """Implementación del asistente de publicación."""

    def __init__(self) -> None:
        self.steps = [
            ("Cargar", self.step_load),
            ("Procesar", self.step_process),
            ("Revisar", self.step_review),
            ("Publicar", self.step_publish),
        ]
        self.index = 0
        self.docx: Path | None = None
        logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    # --------------------------------------------------
    def run_cmd(self, cmd: list[str]) -> int:
        """Ejecuta ``cmd`` mostrando el retorno."""
        logging.info("$ %s", " ".join(cmd))
        return subprocess.run(cmd).returncode

    # --------------------------------------------------
    def step_load(self) -> None:
        """Solicita la ruta del documento a procesar."""
        while True:
            inp = input("Ruta del archivo .docx: ").strip()
            if not inp:
                print("Debe introducir una ruta válida")
                continue
            p = (ROOT_DIR / inp) if not Path(inp).is_absolute() else Path(inp)
            if not p.exists():
                print(f"No existe: {p}")
                continue
            if p.suffix.lower() != ".docx":
                print("El archivo debe tener extensión .docx")
                continue
            self.docx = p
            break

    # --------------------------------------------------
    def step_process(self) -> None:
        """Convierte y prepara los archivos para la ingesta."""
        assert self.docx is not None
        steps = [
            [
                "pandoc",
                str(self.docx),
                "--from=docx",
                "--to=gfm",
                "--output=_fuentes/tmp_full.md",
                "--extract-media=wiki/assets",
                "--markdown-headings=atx",
                "--standalone",
                "--wrap=none",
            ],
            [sys.executable, "scripts/limpiar_md.py", "_fuentes/tmp_full.md"],
            [sys.executable, "scripts/generar_mapa_encabezados.py"],
            [sys.executable, "scripts/generar_index_desde_encabezados.py"],
        ]
        for cmd in steps:
            rc = self.run_cmd(cmd)
            if rc != 0:
                raise RuntimeError(f"Paso fallido: {' '.join(cmd)}")

    # --------------------------------------------------
    def step_review(self) -> None:
        """Pausa para que el usuario revise el mapa e índice."""
        print("\nRevisa los archivos generados en '_fuentes/' y 'index_PlataformaBBDD.yaml'.")
        input("Pulsa Enter para continuar...")

    # --------------------------------------------------
    def step_publish(self) -> None:
        """Ingiere y valida la wiki."""
        cmds = [
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
            ],
            [sys.executable, "scripts/generar_sidebar.py"],
            [sys.executable, "scripts/validar_sidebar_vs_fs.py"],
            [sys.executable, "scripts/clean_orphaned_files.py"],
            [sys.executable, "scripts/generar_indice_busqueda.py"],
        ]
        for cmd in cmds:
            rc = self.run_cmd(cmd)
            if rc != 0:
                raise RuntimeError(f"Paso fallido: {' '.join(cmd)}")
        print("Publicación completada.")

    # --------------------------------------------------
    def loop(self) -> None:
        while self.index < len(self.steps):
            name, func = self.steps[self.index]
            print(f"\n=== Paso {self.index + 1}: {name} ===")
            try:
                func()
            except Exception as exc:  # noqa: BLE001
                print(f"[ERROR] {exc}")
            action = input("[N]ext, [B]ack, [R]epeat, [Q]uit > ").lower().strip()
            if action == "b":
                if self.index > 0:
                    self.index -= 1
                continue
            if action == "r":
                continue
            if action == "q":
                print("Saliendo del asistente")
                return
            self.index += 1


def main() -> None:
    Wizard().loop()


if __name__ == "__main__":
    main()
