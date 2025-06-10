#!/usr/bin/env python
"""Editor WYSIWYG para archivos Markdown.

Lanza un servidor Flask con SimpleMDE para editar el archivo indicado.
Al pulsar "Guardar y publicar" se escribe el contenido y se actualiza el
índice de búsqueda.
"""

from __future__ import annotations

import argparse
import sys
import webbrowser
from pathlib import Path

from flask import Flask, render_template_string, request

from utils.entorno import add_src_to_path, run, script_path

add_src_to_path()

app = Flask(__name__)
FILE: Path

HTML_TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">
  <script src="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>
</head>
<body>
  <textarea id="editor"></textarea>
  <button onclick="save()">Guardar y publicar</button>
  <script>
    var editor = new SimpleMDE({ element: document.getElementById('editor') });
    fetch('/load').then(r => r.text()).then(t => editor.value(t));
    function save() {
      fetch('/save', { method: 'POST', body: editor.value() })
        .then(r => r.text()).then(alert);
    }
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    """Renderiza el editor de Markdown."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/load")
def load_content():
    """Devuelve el contenido actual del archivo."""
    return FILE.read_text(encoding="utf-8")


@app.route("/save", methods=["POST"])
def save_content():
    """Guarda el archivo y actualiza el índice de búsqueda."""
    FILE.write_text(request.get_data(as_text=True), encoding="utf-8")
    run([sys.executable, str(script_path("generar_indice_busqueda.py"))])
    return "Guardado"


def main() -> None:
    """Lanza la aplicación de edición."""
    parser = argparse.ArgumentParser(description="Editor visual para Markdown")
    parser.add_argument("file", type=Path, help="Archivo .md a editar")
    args = parser.parse_args()

    global FILE
    FILE = args.file
    if not FILE.exists():
        FILE.write_text("", encoding="utf-8")

    webbrowser.open("http://127.0.0.1:5000")
    app.run()


if __name__ == "__main__":
    main()
