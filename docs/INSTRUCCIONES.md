# Guía rápida de uso

Este proyecto permite convertir documentos en Markdown y generar una wiki basada en Docsify.
La forma más sencilla de ejecutar todo el proceso es a través de
`wiki_cli.py`, que automatiza la limpieza, conversión e ingesta. También
existen utilidades para revisar el resultado antes de publicar.

```bash
python src/scripts/wiki_cli.py full _fuentes/_originales/
```

Con `full` se realiza la carga completa sobre todos los `.docx` y `.pdf` de la
carpeta indicada (o sobre un único archivo si se especifica). Puede utilizar
`reset` para vaciar la wiki antes de comenzar. Si prefiere revisar los archivos generados antes
de ingerir, ejecute:

```bash
python pipeline_codex.py _fuentes/_originales/archivo.docx
```

Otra alternativa interactiva es `wizard_publicacion.py`, que guía paso a
paso y muestra una vista previa del Markdown:

```bash
python src/scripts/wizard_publicacion.py
```

Los apartados siguientes describen el proceso manual si necesita ejecutar
los scripts por separado.

## Reiniciar y cargar desde cero

1. **Limpiar el entorno**

   Ejecute:

   ```bash
   python src/scripts/resetear_entorno.py
   ```

   Este script elimina la carpeta `wiki/`, los índices, el sidebar y los archivos temporales. Tras la limpieza se puede comenzar una ingesta desde cero.

2. **Convertir el documento fuente**

   Reemplace `archivo.docx` por su documento y ejecute:

   ```bash
   pandoc _fuentes/_originales/archivo.docx \
     --from=docx --to=gfm --output=_fuentes/tmp_full.md \
     --extract-media=wiki/assets --markdown-headings=atx --standalone --wrap=none
   python src/scripts/limpiar_md.py _fuentes/tmp_full.md
   ```
   Este paso elimina los atributos `{width=..., height=...}` de las imágenes
   que Pandoc incorpora y que Docsify no interpreta correctamente.

3. **Generar mapa e índice**

   ```bash
    python src/scripts/generar_mapa_encabezados.py
   python src/scripts/generar_index_desde_encabezados.py --precheck --ignore-extra
   ```
   La opción `--ignore-extra` permite continuar cuando existen entradas en
   `index_PlataformaBBDD.yaml` que no aparecen en el mapa actual, lo cual es
   útil al incorporar nueva documentación de manera incremental.

4. **Ingestar la wiki**

   ```bash
   python src/scripts/ingest_wiki_v2.py \
     --mapa _fuentes/mapa_encabezados.yaml \
     --index index_PlataformaBBDD.yaml \
    --fuente _fuentes/tmp_full.md \
    --alias _fuentes/alias_override.yaml \
    --cutoff 0.5
    --metadata
   ```

5. **Generar el sidebar y auditar**

   ```bash
   python src/scripts/generar_sidebar.py --index index_PlataformaBBDD.yaml --out _sidebar.md --tolerant
   python src/scripts/auditar_sidebar_vs_fs.py
   ```

Con esto la wiki quedará creada en la carpeta `wiki/`.

## Añadir documentos sin limpiar

Si desea incorporar nuevos `.docx` o `.pdf` sin borrar la wiki existente, copie los archivos en `_fuentes/_originales` y ejecute:

```bash
python src/scripts/procesar_nuevos.py
```

El script detecta documentos no procesados, aplica automáticamente la misma cadena de scripts anterior y actualiza la wiki conservando el contenido ya publicado.
Si tiene varios archivos pendientes puede copiarlos juntos y ejecutar el comando una sola vez; se procesarán de forma secuencial manteniendo el índice existente.
Los PDF se convertirán directamente a Markdown. Con la opción `--ocr` se intentará extraer texto mediante `pytesseract` cuando sea necesario. Los fallidos se registrarán en `errores_pdf.csv`.
Si necesita una recarga completa, ejecute previamente `python src/scripts/resetear_entorno.py` o use `python src/scripts/procesar_nuevos.py --clean`.

## Utilidades adicionales

- `src/scripts/web_uploader.py` permite cargar documentos mediante una pequeña
  interfaz web con drag & drop.
- `src/scripts/editor_markdown.py` abre un editor con vista previa para modificar
  los `.md` antes de publicarlos.
