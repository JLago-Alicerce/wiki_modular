# wiki_modular

Herramientas para construir una wiki modular con [Docsify](https://docsify.js.org/) a partir de un único documento Markdown.
Los scripts en `scripts/` permiten generar el mapa de encabezados, un índice maestro y el fichero `_sidebar.md` requerido por Docsify.

## Requisitos

- Python 3.8 o superior.
- Dependencias listadas en `requirements.txt`.
- Node.js para ejecutar Docsify en local.

Instala las dependencias de Python con:

```bash
pip install -r requirements.txt
```

## Uso rápido

1. Genera el mapa de encabezados:
   ```bash
   python scripts/generar_mapa_encabezados.py
   ```
2. Crea el índice maestro:
   ```bash
   python scripts/generar_index_desde_encabezados.py
   ```
3. Construye el `_sidebar.md`:
   ```bash
   python scripts/generar_sidebar_desde_index.py
   ```

Puedes ejecutar toda la cadena y una auditoría básica con:

```bash
make build
```

### Fragmentar la wiki

El script `ingest_wiki.py` divide el Markdown completo en secciones individuales usando el índice:

```bash
python scripts/ingest_wiki.py --fuente _fuentes/tmp_full.md --mapa _fuentes/mapa_encabezados.yaml --index index_PlataformaBBDD.yaml
```

### Servir la documentación

Para previsualizar la wiki en local con Docsify:

```bash
npx docsify serve .
```

### Ejecutar pruebas

```bash
pytest
```

## Licencia

Distribuido bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.
