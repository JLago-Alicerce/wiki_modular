"""Configuración común para la suite de pruebas."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

try:  # pragma: no cover - simple import guard for clarity
    import yaml  # noqa: F401
except ImportError as exc:  # pragma: no cover - fail fast if missing
    raise ImportError(
        "PyYAML is required to run the test suite. "
        "Instale las dependencias con 'pip install -e .' "
        "o 'pip install -r requirements.txt'"
    ) from exc
