#!/usr/bin/env python
"""Limpia archivos generados para reiniciar la wiki desde cero."""

import shutil
from datetime import datetime
from pathlib import Path


RUTAS = [
    Path("wiki"),
    Path("wiki/_sidebar.md"),
    Path("index_PlataformaBBDD.yaml"),
    Path("mismatch_report.csv"),
    Path("procesados.log"),
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
        if path.name == "procesados.log":
            archive_dir = Path("logs")
            archive_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = archive_dir / f"procesados_{timestamp}.log"
            shutil.move(str(path), archive_path)
            print(f"[✓] Log archivado en: {archive_path}")
        else:
            path.unlink()
            print(f"[✓] Archivo eliminado: {path}")
    else:
        print(f"[ ] No existe: {path}")


def main() -> None:
    wiki_dir = Path("wiki")
    readme_backup = None
    readme_path = wiki_dir / "README.md"
    if readme_path.exists():
        readme_backup = readme_path.read_text(encoding="utf-8")

    for ruta in RUTAS:
        eliminar(ruta)

    if readme_backup is not None:
        wiki_dir.mkdir(exist_ok=True)
        readme_path.write_text(readme_backup, encoding="utf-8")
        print(f"[✓] README restaurado: {readme_path}")

    print("✅ Entorno limpio. Puede ejecutar los scripts de carga desde cero.")


if __name__ == "__main__":
    main()
