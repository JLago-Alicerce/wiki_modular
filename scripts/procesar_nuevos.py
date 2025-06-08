#!/usr/bin/env python
"""Procesa automáticamente nuevos archivos en `_fuentes/_originales`.

Revisa si existen archivos `.docx` nuevos en la carpeta y ejecuta la cadena de
scripts definida en el README. Mantiene un log en `procesados.log` con la fecha
de cada archivo procesado para evitar reprocesos.
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

ORIG_DIR = Path('_fuentes/_originales')
LOG_FILE = Path('procesados.log')

PIPELINE = [
    lambda doc: [
        'pandoc', str(doc),
        '--from=docx', '--to=gfm', '--output=_fuentes/tmp_full.md',
        '--extract-media=wiki/assets', '--markdown-headings=atx',
        '--standalone', '--wrap=none'
    ],
    lambda _doc: [sys.executable, 'scripts/limpiar_md.py', '_fuentes/tmp_full.md'],
    lambda _doc: [sys.executable, 'scripts/generar_mapa_encabezados.py'],
    lambda _doc: [sys.executable, 'scripts/generar_index_desde_encabezados.py', '--precheck'],
    lambda _doc: [
        sys.executable, 'scripts/ingest_wiki_v2.py',
        '--mapa', '_fuentes/mapa_encabezados.yaml',
        '--index', 'index_PlataformaBBDD.yaml',
        '--fuente', '_fuentes/tmp_full.md',
        '--alias', '_fuentes/alias_override.yaml',
        '--cutoff', '0.5'
    ],
    lambda _doc: [sys.executable, 'scripts/generar_sidebar_desde_index.py'],
    lambda _doc: [sys.executable, 'scripts/auditar_sidebar_vs_fs.py'],
]


def load_log() -> Dict[str, str]:
    processed = {}
    if LOG_FILE.exists():
        for line in LOG_FILE.read_text(encoding='utf-8').splitlines():
            try:
                entry = json.loads(line)
                processed[entry['file']] = entry['processed_at']
            except Exception:
                continue
    return processed


def append_log(filename: str) -> None:
    entry = {'file': filename, 'processed_at': datetime.now().isoformat()}
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')


def run_pipeline(doc: Path) -> None:
    for build_cmd in PIPELINE:
        cmd = build_cmd(doc)
        logging.info('Ejecutando: %s', ' '.join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            raise RuntimeError(f"Paso fallido: {' '.join(cmd)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Procesa automáticamente nuevos .docx")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Ejecutar resetear_entorno.py antes de procesar"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    if args.clean:
        logging.info('Limpiando entorno previo')
        rc = subprocess.run([sys.executable, 'scripts/resetear_entorno.py']).returncode
        if rc != 0:
            raise RuntimeError('resetear_entorno.py fallo')

    processed = load_log()
    new_files = []

    for doc in sorted(ORIG_DIR.glob('*.docx')):
        if doc.name in processed:
            logging.info('Ya procesado %s en %s', doc.name, processed[doc.name])
        else:
            new_files.append(doc)

    if not new_files:
        logging.info('No hay archivos nuevos en %s', ORIG_DIR)
        return

    for doc in new_files:
        logging.info('Procesando %s', doc.name)
        try:
            run_pipeline(doc)
        except Exception as e:
            logging.error('Error procesando %s: %s', doc.name, e)
            raise
        else:
            append_log(doc.name)
            logging.info('Procesado correctamente: %s', doc.name)


if __name__ == '__main__':
    main()
