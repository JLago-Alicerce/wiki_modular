# wiki_modular

Este repositorio contiene utilidades para fragmentar documentación en Markdown
y construir una wiki lista para Docsify. Todas las funciones comunes se
encuentran dentro del paquete `wiki_modular` y pueden instalarse con:

```bash
pip install -e .
```

> **Nota:** este comando instala el proyecto y todas las dependencias
> necesarias (por ejemplo `PyYAML`). Si se invocan los scripts sin haber
> realizado esta instalación previa, es probable que falten paquetes y se
> produzcan errores.

## Flujo recomendado

> **Nota**: si quiere reconstruir la wiki desde cero antes de procesar nuevos documentos, ejecute:
>
> ```bash
> python scripts/resetear_entorno.py
> ```
>
> Esto limpia la carpeta `wiki/`, los índices y archivos temporales para evitar conflictos.

1. Convertir el `.docx` a Markdown (reemplazar por tu archivo):

```bash
pandoc _fuentes/_originales/archivo.docx \
  --from=docx --to=markdown --output=_fuentes/tmp_full.md \
  --extract-media=wiki/assets --markdown-headings=atx --standalone --wrap=none
```

2. Generar mapa de encabezados y el índice:

```bash
python scripts/generar_mapa_encabezados.py
python scripts/generar_index_desde_encabezados.py --precheck
```

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
python scripts/ingest_wiki_v2.py \
  --mapa _fuentes/mapa_encabezados.yaml \
  --index index_PlataformaBBDD.yaml \
  --fuente _fuentes/tmp_full.md \
  --alias _fuentes/alias_override.yaml \
 --cutoff 0.5
```

4. Generar el sidebar (puede personalizar las rutas con `--index` y `--out`):

```bash
python scripts/generar_sidebar_desde_index.py --index index_PlataformaBBDD.yaml --out _sidebar.md
```

5. Auditar enlaces vs. archivos:

```bash
python scripts/auditar_sidebar_vs_fs.py
```

Para comprobar que todos los ficheros de `wiki/` aparecen enlazados y que no
existen enlaces rotos, puede ejecutarse:

```bash
python scripts/validar_sidebar_vs_fs.py
```

Si prefiere automatizar la detección y el procesado de nuevos `.docx`, puede
utilizar:

```bash
python scripts/procesar_nuevos.py --clean
```

El indicador `--clean` ejecuta `resetear_entorno.py` para garantizar que la
wiki se regenere desde cero.

### Personalización de rutas

La mayoría de los scripts aceptan argumentos opcionales para indicar dónde
buscar los archivos de entrada o dónde generar las salidas. Consulte `-h` en
cada utilidad para ver todas las opciones. Esto permite integrar el flujo en
proyectos con estructuras de directorio diferentes.

El archivo `_fuentes/alias_override.yaml` permite definir emparejamientos de
títulos con slugs personalizados cuando el algoritmo de coincidencia difusa no
encuentra el destino correcto.

## Utilidades

- `scripts/limpiar_slug.py`: muestra en consola la versión normalizada de los argumentos recibidos.
- `scripts/verificar_pre_ingesta.py`: comprueba consistencia entre el mapa y el índice.
- `scripts/validar_sidebar_vs_fs.py`: asegura que `_sidebar.md` está sincronizado con los ficheros de la carpeta `wiki/`.
- `scripts/resetear_entorno.py`: elimina wiki, índices y archivos temporales para empezar de cero.

## Convención de nombres de ramas

Para evitar problemas de compatibilidad entre sistemas y servidores Git,
procure nombrar las ramas únicamente con caracteres ASCII (letras
`A-Z`, `a-z`, números y guiones). Se desaconseja el uso de acentos,
espacios o caracteres especiales.
