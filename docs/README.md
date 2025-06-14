# wiki_modular

Este repositorio contiene utilidades para fragmentar documentación en Markdown
y construir una wiki lista para Docsify. Todas las funciones comunes se
encuentran dentro del paquete `wiki_modular` y se pueden instalar de dos
maneras:

```bash
# Versión publicada desde PyPI
pip install wiki_modular

# O bien la copia clonada para desarrollo
pip install -e .
```

> **Nota:** el modo editable instala el proyecto y todas las dependencias
> necesarias (por ejemplo `PyYAML`). Si se invocan los scripts sin haber
> realizado esta instalación previa, es probable que falten paquetes y se
> produzcan errores.

## Flujo recomendado

Si prefiere ejecutar todos los pasos de forma automática puede utilizar la
interfaz unificada:

```bash
python src/scripts/wiki_cli.py full _fuentes/_originales
```

El comando `full` limpiará el entorno, procesará un archivo individual o todos
los `.docx` y `.pdf` de la carpeta indicada, generará los índices, realizará la
ingesta y validará el resultado. También existe
`python src/scripts/wiki_cli.py reset` para borrar la wiki e índices antes de una
nueva carga.

Otra alternativa es `pipeline_codex.py`, que ejecuta los mismos pasos pero se
detiene tras generar el mapa e índice para revisar los archivos antes de
ingestar definitivamente:

```bash
python pipeline_codex.py _fuentes/_originales/archivo.docx
```

Si se prefiere una guía interactiva existe `wizard_publicacion.py`, que
permite avanzar y retroceder por cada etapa y ahora muestra una
previsualización del Markdown antes de publicar:

```bash
python src/scripts/wizard_publicacion.py
```

> **Nota**: si quiere reconstruir la wiki desde cero antes de procesar nuevos documentos, ejecute:
>
> ```bash
> python src/scripts/resetear_entorno.py
> ```
>
> Esto limpia la carpeta `wiki/`, los índices y archivos temporales para evitar conflictos.

1. Convertir el `.docx` a Markdown (reemplazar por tu archivo):

```bash
pandoc _fuentes/_originales/archivo.docx \
  --from=docx --to=gfm --output=_fuentes/tmp_full.md \
  --extract-media=wiki/assets --markdown-headings=atx --standalone --wrap=none
python src/scripts/limpiar_md.py _fuentes/tmp_full.md
```
Este paso elimina los atributos `{width=..., height=...}` que Pandoc añade a las
imágenes y que Docsify no interpreta.

2. Generar mapa de encabezados y el índice:

```bash
python src/scripts/generar_mapa_encabezados.py
python src/scripts/generar_index_desde_encabezados.py --precheck --ignore-extra
```

Si `index_PlataformaBBDD.yaml` ya existe, el script añadirá las nuevas secciones
al final manteniendo los `subtemas` previamente definidos. Con la opción
`--ignore-extra` la verificación previa solo fallará cuando el mapa incluya
títulos que no existan en el índice, por lo que se pueden procesar varios
documentos de forma incremental sin reiniciar la wiki.

El archivo `index_PlataformaBBDD.yaml` resultante contiene una lista de secciones con el siguiente esquema:

```yaml
secciones:
  - id: 1
    titulo: 1. Objeto del documento
    slug: 1_objeto_del_documento
    subtemas: []
```

3. Ingestar la wiki:

```bash
python src/scripts/ingest_wiki_v2.py \
  --mapa _fuentes/mapa_encabezados.yaml \
  --index index_PlataformaBBDD.yaml \
  --fuente _fuentes/tmp_full.md \
  --alias _fuentes/alias_override.yaml \
 --cutoff 0.5
  --metadata
```

4. Generar el sidebar (puede personalizar las rutas con `--index` y `--out`):

```bash
python src/scripts/generar_sidebar.py --index index_PlataformaBBDD.yaml --out _sidebar.md --tolerant
```

5. Auditar enlaces vs. archivos:

```bash
python src/scripts/auditar_sidebar_vs_fs.py
```

Para comprobar que todos los ficheros de `wiki/` aparecen enlazados y que no
existen enlaces rotos, puede ejecutarse:

```bash
python src/scripts/validar_sidebar_vs_fs.py
```

6. Generar el índice de búsqueda:

```bash
python src/scripts/generar_indice_busqueda.py
```

Si prefiere automatizar la detección y el procesado de nuevos `.docx` o `.pdf`, puede
utilizar:

```bash
python src/scripts/procesar_nuevos.py --clean
```

El indicador `--clean` ejecuta `resetear_entorno.py` para garantizar que la
wiki se regenere desde cero. Los PDF se convierten directamente a Markdown
mediante `pdfminer.six` y opcionalmente `pytesseract` con `--ocr`. Los que no
puedan procesarse se anotarán en `errores_pdf.csv`.

### Personalización de rutas

La mayoría de los scripts aceptan argumentos opcionales para indicar dónde
buscar los archivos de entrada o dónde generar las salidas. Consulte `-h` en
cada utilidad para ver todas las opciones. Esto permite integrar el flujo en
proyectos con estructuras de directorio diferentes.

El archivo `_fuentes/alias_override.yaml` permite definir emparejamientos de
títulos con slugs personalizados cuando el algoritmo de coincidencia difusa no
encuentra el destino correcto. Consulte [alias_override.md](alias_override.md)
para ver el formato detallado y algunos ejemplos de uso. Además, los títulos
sin coincidencia se anotan en `_fuentes/alias_suggestions.csv` junto con el slug
propuesto para facilitar su revisión.

-## Utilidades

- `src/scripts/limpiar_slug.py`: muestra en consola la versión normalizada de los argumentos recibidos.
- `src/scripts/verificar_pre_ingesta.py`: comprueba consistencia entre el mapa y el índice. Con `--ignore-extra` sólo advierte por títulos faltantes.
- `src/scripts/validar_sidebar_vs_fs.py`: asegura que `_sidebar.md` está sincronizado con los ficheros de la carpeta `wiki/`.
- `src/scripts/resetear_entorno.py`: elimina wiki, índices y archivos temporales para empezar de cero.
- `src/scripts/generar_indice_busqueda.py`: crea `search_index.json` a partir de los Markdown de `wiki/`.
- `src/scripts/clean_orphaned_files.py`: borra los `.md` que no estén enlazados en `_sidebar.md`.
- `src/scripts/comparar_versiones.py`: genera un diff lateral entre la versión
  actual de un `.md` y una copia previa desde un backup o `git`.
- `src/scripts/web_uploader.py`: lanza un servidor sencillo para cargar `.docx` o `.md` mediante drag & drop.
- `pipeline_codex.py`: alternativa a `wiki_cli.py` que pausa antes de ingerir para revisión manual.
- `src/scripts/mover_huerfanos.py`: tras comparar el índice y el sidebar, mueve los archivos Markdown no referenciados a `wiki/_deprecated/`.
- `utils/entorno.py`: centraliza la adición de `src/` al `PYTHONPATH` mediante `add_src_to_path()` y ofrece `run()` para lanzar otros scripts de forma consistente.
- `src/scripts/editor_markdown.py`: abre un editor web con vista previa y un botón "guardar y publicar" para modificar archivos Markdown.

## Búsqueda en la wiki

Ejecuta `python src/scripts/generar_indice_busqueda.py` tras la ingesta para
generar `search_index.json`. Este archivo lo utiliza Docsify a través del
plugin de búsqueda configurado en `index.html`.

Para consultas más detalladas existe la página
`buscar-avanzado.html`, que carga `search_index.json` mediante
[Lunr.js](https://lunrjs.com/). Este buscador permite filtrar por
`source_file`, `conversion_date` o el nivel de encabezado (`H2`, `H3`,
etc.) y muestra fragmentos de contexto con los términos resaltados.
Al hacer clic se navega directamente a la sección correspondiente.
El campo principal responde al momento de escribir para mostrar los
resultados dinámicamente.

## Convención de nombres de ramas

Para evitar problemas de compatibilidad entre sistemas y servidores Git,
procure nombrar las ramas únicamente con caracteres ASCII (letras
`A-Z`, `a-z`, números y guiones). Se desaconseja el uso de acentos,
espacios o caracteres especiales.

## Pruebas

Antes de ejecutar `pytest` asegúrsate de instalar las dependencias del
proyecto con alguno de los siguientes comandos:

```bash
pip install -e .
# o
pip install -r requirements.txt
```

Luego ejecute todos los tests con:

```bash
pytest
```

Si tiene `pre-commit` instalado puede ejecutar `pre-commit run --all-files` para
verificar formato y estilo antes de enviar cambios.

Todas las pruebas deberían completarse correctamente sin requerir acceso a la red.
