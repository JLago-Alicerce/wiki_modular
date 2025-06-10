#!/usr/bin/env python
"""Servidor web para subir archivos a '_fuentes/_originales'."""

from __future__ import annotations

import cgi
import os
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler

from wiki_modular.config import ORIGINALES_DIR

PAGE_HTML = """
<!DOCTYPE html>
<html lang=\"es\">
<head>
<meta charset=\"utf-8\">
<title>Subir documentos</title>
<style>
#dropzone {
  width: 100%;
  height: 200px;
  border: 2px dashed #888;
  border-radius: 10px;
  text-align: center;
  line-height: 200px;
  color: #888;
  font-family: sans-serif;
}
#dropzone.dragover {
  background-color: #eee;
  color: #000;
}
</style>
</head>
<body>
<div id=\"dropzone\">Arrastre archivos .docx o .md aquí</div>
<script>
const drop = document.getElementById('dropzone');
drop.addEventListener('dragover', e => {e.preventDefault(); drop.classList.add('dragover');});
drop.addEventListener('dragleave', () => drop.classList.remove('dragover'));
drop.addEventListener('drop', e => {
  e.preventDefault();
  drop.classList.remove('dragover');
  const files = e.dataTransfer.files;
  for (const f of files) {
    const ext = f.name.split('.').pop().toLowerCase();
    if (!['docx','md'].includes(ext)) {
      alert('Extensión no soportada: ' + f.name);
      continue;
    }
    const fd = new FormData();
    fd.append('file', f, f.name);
    fetch('/upload', {method:'POST', body: fd}).then(r => {
      if(!r.ok) r.text().then(t => alert(t));
    }).catch(err => alert(err));
  }
});
</script>
</body>
</html>
"""


class UploadHandler(SimpleHTTPRequestHandler):
    """Maneja carga de archivos mediante POST."""

    def do_GET(self) -> None:  # noqa: D401
        """Servir la página principal."""
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PAGE_HTML.encode("utf-8"))
        else:
            self.send_error(404)

    def do_POST(self) -> None:  # noqa: D401
        """Recibir archivos y guardarlos en :data:`ORIGINALES_DIR`."""
        if self.path != "/upload":
            self.send_error(404)
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )

        files = form["file"]
        if not isinstance(files, list):
            files = [files]

        ORIGINALES_DIR.mkdir(parents=True, exist_ok=True)

        for item in files:
            filename = os.path.basename(item.filename)
            ext = filename.rsplit(".", 1)[-1].lower()
            if ext not in {"docx", "md"}:
                self.send_error(400, "Extensión no soportada")
                return
            dest = ORIGINALES_DIR / filename
            with open(dest, "wb") as f:
                shutil.copyfileobj(item.file, f)

        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"OK")


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Inicia el servidor de carga."""
    httpd = HTTPServer((host, port), UploadHandler)
    print(f"Servidor escuchando en http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
