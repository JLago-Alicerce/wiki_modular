from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from .utils import load_yaml

# Valores por defecto para todos los proyectos
DEFAULT_CONFIG: Dict[str, Any] = {
    "wiki_dir": "wiki",
    "mapa_file": "_fuentes/mapa_encabezados.yaml",
    "index_file": "index_PlataformaBBDD.yaml",
    "fuente_md": "_fuentes/tmp_full.md",
    "alias_file": "_fuentes/alias_override.yaml",
    "suggestions": "_fuentes/alias_suggestions.csv",
    "sidebar_file": None,  # se resolverá a <wiki_dir>/_sidebar.md
    "cutoff": 0.5,
}


def load_config(path: str | Path | None = None) -> Dict[str, Any]:
    """Carga la configuración del proyecto.

    Si ``path`` es ``None`` se intentará leer la ruta desde la
    variable de entorno ``WIKI_CONFIG`` y, en última instancia,
    ``config.yaml`` en el directorio actual.
    """
    if path is None:
        path = os.environ.get("WIKI_CONFIG", "config.yaml")
    cfg_path = Path(path)
    if cfg_path.exists():
        data = load_yaml(cfg_path)
        if not isinstance(data, dict):
            raise ValueError(f"{cfg_path} debe contener un mapeo YAML")
        config = DEFAULT_CONFIG.copy()
        config.update(data)
    else:
        config = DEFAULT_CONFIG.copy()
    if config.get("sidebar_file") is None:
        config["sidebar_file"] = str(Path(config["wiki_dir"]) / "_sidebar.md")
    return config
