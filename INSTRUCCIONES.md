# Guía rápida de uso

Este proyecto permite convertir documentos en Markdown y generar una wiki basada en Docsify. A continuación se describen los pasos para arrancar una carga desde cero y para añadir nueva documentación sin borrar la existente.

## Reiniciar y cargar desde cero

1. **Limpiar el entorno**

   Ejecute:

   ```bash
   python scripts/resetear_entorno.py
   ```

   Este script elimina la carpeta `wiki/`, los índices, el sidebar y los archivos temporales. Tras la limpieza se puede comenzar una ingesta desde cero.

2. **Convertir el documento fuente**

   Reemplace `archivo.docx` por su documento y ejecute:

   ```bash
   pandoc _fuentes/_originales/archivo.docx \
     --from=docx --to=markdown --output=_fuentes/tmp_full.md \
     --extract-media=wiki/assets --markdown-headings=atx --standalone --wrap=none
   ```

3. **Generar mapa e índice**

   ```bash
   python scripts/generar_mapa_encabezados.py
   python scripts/generar_index_desde_encabezados.py --precheck
   ```

4. **Ingestar la wiki**

   ```bash
   python scripts/ingest_wiki_v2.py \
     --mapa _fuentes/mapa_encabezados.yaml \
     --index index_PlataformaBBDD.yaml \
     --fuente _fuentes/tmp_full.md \
     --alias _fuentes/alias_override.yaml \
     --cutoff 0.5
   ```

5. **Generar el sidebar y auditar**

   ```bash
   python scripts/generar_sidebar_desde_index.py --index index_PlataformaBBDD.yaml --out _sidebar.md
   python scripts/auditar_sidebar_vs_fs.py
   ```

Con esto la wiki quedará creada en la carpeta `wiki/`.

## Añadir documentos sin limpiar

Si desea incorporar nuevos `.docx` sin borrar la wiki existente, copie los archivos en `_fuentes/_originales` y ejecute:

```bash
python scripts/procesar_nuevos.py
```

El script detecta documentos no procesados, aplica automáticamente la misma cadena de scripts anterior y actualiza la wiki conservando el contenido ya publicado.
Si necesita una recarga completa, ejecute previamente `python scripts/resetear_entorno.py` o use `python scripts/procesar_nuevos.py --clean`.
