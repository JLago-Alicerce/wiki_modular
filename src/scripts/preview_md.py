#!/usr/bin/env python
"""Visualizador web para archivos Markdown."""

from __future__ import annotations

import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

import markdown2

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"utf-8\" />
    <title>Vista previa</title>
</head>
<body>
{content}
<p>
    <a href=\"/action/approve\"><button>Aprobar y publicar</button></a>
    <a href=\"/action/edit\"><button>Volver a editar</button></a>
</p>
</body>
</html>
"""


class _Handler(http.server.SimpleHTTPRequestHandler):
    """Manejador HTTP mínimo para la vista previa."""

    page: str

    def do_GET(self) -> None:  # noqa: D401
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self.page.encode("utf-8"))
        elif self.path.startswith("/action/"):
            self.server.action = self.path.split("/", 2)[2]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Puede cerrar esta ventana.")
        else:
            self.send_error(404)


class PreviewServer(socketserver.TCPServer):
    """Servidor que almacena la acción seleccionada."""

    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, page: str):
        """Inicializa el servidor y asigna la página que se servirá."""
        super().__init__(server_address, RequestHandlerClass)
        self.action: str | None = None
        RequestHandlerClass.page = page


def preview_markdown(path: Path) -> str:
    """Muestra ``path`` en el navegador y devuelve la acción elegida."""
    html = markdown2.markdown_path(str(path))
    page = HTML_TEMPLATE.format(content=html)

    with PreviewServer(("localhost", 0), _Handler, page) as httpd:
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever)
        thread.start()
        webbrowser.open(f"http://localhost:{port}/")
        try:
            while httpd.action is None:
                thread.join(0.1)
        finally:
            httpd.shutdown()
            thread.join()
    return httpd.action or "edit"


def main() -> None:
    """CLI simple para lanzar la vista previa."""
    import argparse

    parser = argparse.ArgumentParser(description="Previsualiza un Markdown")
    parser.add_argument("file", type=Path, help="Archivo .md a mostrar")
    args = parser.parse_args()

    action = preview_markdown(args.file)
    print(f"Acción seleccionada: {action}")


if __name__ == "__main__":
    main()
