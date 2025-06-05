#!/usr/bin/env python
"""Limpia archivos generados para reiniciar la wiki desde cero."""

import shutil
from pathlib import Path


RUTAS = [
    Path("wiki"),
    Path("_sidebar.md"),
    Path("index_PlataformaBBDD.yaml"),
    Path("mismatch_report.csv"),
    Path("_tmp"),
    Path("_fuentes/tmp_full.md"),
    Path("_fuentes/mapa_encabezados.yaml"),
]


def eliminar(path: Path) -> None:
    """Elimina un archivo o directorio si existe."""
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
        print(f"[✓] Carpeta eliminada: {path}")
    elif path.exists():
        path.unlink()
        print(f"[✓] Archivo eliminado: {path}")
    else:
        print(f"[ ] No existe: {path}")


def main() -> None:
    for ruta in RUTAS:
        eliminar(ruta)
    print("✅ Entorno limpio. Puede ejecutar los scripts de carga desde cero.")


if __name__ == "__main__":
    main()
