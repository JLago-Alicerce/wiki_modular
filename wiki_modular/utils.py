import re
import yaml
import unicodedata
from pathlib import Path
from typing import Any

__all__ = [
    "limpiar_slug",
    "load_yaml",
    "limpiar_atributos_imagenes",
    "limpiar_archivo_markdown",
]


def limpiar_slug(texto: str) -> str:
    """Devuelve un slug idempotente para nombres de archivo."""
    if not isinstance(texto, str):
        texto = str(texto)
    ascii_text = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    ascii_text = ascii_text.lower()
    ascii_text = ascii_text.replace(" ", "_").replace("/", "_")
    ascii_text = re.sub(r"[^a-z0-9_-]", "", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    return ascii_text


def load_yaml(path: Path) -> Any:
    """Carga y parsea un YAML desde ``path`` si existe."""
    if not path.exists():
        raise FileNotFoundError(path)
    content = path.read_text(encoding="utf-8")
    return yaml.safe_load(content)


_IMG_ATTR_RE = re.compile(r"(!\[[^\]]*\]\([^\)]+\))\{[^\}]*\}")


def limpiar_atributos_imagenes(texto: str) -> str:
    """Elimina ``{width=..., height=...}`` de las imágenes."""
    return _IMG_ATTR_RE.sub(r"\1", texto)


def limpiar_archivo_markdown(path: Path) -> None:
    """Aplica :func:`limpiar_atributos_imagenes` sobre ``path`` si existe."""
    if not path.exists():
        return
    contenido = path.read_text(encoding="utf-8")
    limpio = limpiar_atributos_imagenes(contenido)
    path.write_text(limpio, encoding="utf-8")
