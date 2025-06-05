# wiki_modular

Este repositorio contiene utilidades para fragmentar documentación en Markdown
y construir una wiki lista para Docsify.

## Flujo recomendado

1. Convertir el `.docx` a Markdown (reemplazar por tu archivo):

```bash
pandoc _fuentes/_originales/archivo.docx \
  --from=docx --to=markdown --output=_fuentes/tmp_full.md \
  --extract-media=wiki/assets --markdown-headings=atx --standalone --wrap=none
```

2. Generar mapa de encabezados y el índice:

```bash
python3 scripts/generar_mapa_encabezados.py
python3 scripts/generar_index_desde_encabezados.py --precheck
```

3. Ingestar la wiki:

```bash
python3 scripts/ingest_wiki_v2.py \
  --mapa _fuentes/mapa_encabezados.yaml \
  --index index_PlataformaBBDD.yaml \
  --fuente _fuentes/tmp_full.md \
  --alias _fuentes/alias_override.yaml \
  --cutoff 0.5
```

4. Generar el sidebar:

```bash
python3 scripts/generar_sidebar_desde_index.py
```

5. Auditar enlaces vs. archivos:

```bash
python3 scripts/auditar_sidebar_vs_fs.py
```

El archivo `_fuentes/alias_override.yaml` permite definir emparejamientos de
títulos con slugs personalizados cuando el algoritmo de coincidencia difusa no
encuentra el destino correcto.

## Utilidades

- `scripts/limpiar_slug.py`: función central para normalizar títulos.
- `scripts/verificar_pre_ingesta.py`: comprueba consistencia entre el mapa y el índice.
- `scripts/resetear_entorno.py`: elimina wiki, índices y archivos temporales para empezar de cero.



