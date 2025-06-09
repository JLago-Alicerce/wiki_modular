#!/usr/bin/env python
"""Valida que todos los enlaces del sidebar tengan archivo y viceversa."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "validar_sidebar_vs_fs.py"


def main() -> int:
    return subprocess.call([sys.executable, str(SCRIPT)])


if __name__ == "__main__":
    sys.exit(main())
