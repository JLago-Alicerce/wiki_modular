# Listado de scripts

A continuación se resumen las utilidades disponibles en la carpeta `scripts/`. Cada entrada indica brevemente para qué se emplea el archivo.

| Script | Descripción |
| ------ | ----------- |
| `auditar_sidebar_vs_fs.py` | Compara los enlaces del `_sidebar.md` con los archivos reales y genera un informe CSV de discrepancias. |
| `generar_index_desde_encabezados.py` | Construye `index_PlataformaBBDD.yaml` a partir de un mapa de encabezados. |
| `generar_mapa_encabezados.py` | Extrae los encabezados de un Markdown completo y genera `mapa_encabezados.yaml`. |
| `generar_sidebar.py` | Crea el archivo `_sidebar.md` a partir del índice YAML. |
| `ingest_wiki_v2.py` | Fragmenta `tmp_full.md` según el mapa de encabezados y el índice para poblar la carpeta `wiki/`. Con `--metadata` añade cabecera YAML con información del archivo origen. |
| `limpiar_md.py` | Elimina atributos de tamaño en las imágenes de un Markdown. |
| `limpiar_slug.py` | Normaliza cadenas a slugs seguros para usar como nombres de archivo. |
| `procesar_nuevos.py` | Automatiza la detección y procesamiento de nuevos `.docx` en `_fuentes/_originales`. |
| `resetear_entorno.py` | Borra la wiki y archivos generados para recomenzar una ingesta desde cero. |
| `mover_huerfanos.py` | Mueve a `wiki/_deprecated/` los `.md` que no aparecen en el índice ni en el sidebar. |
| `reubicar_nuevas_secciones.py` | Mueve las secciones creadas en `99_Nuevas_Secciones` a su destino definitivo según el índice. |
| `validar_sidebar_vs_fs.py` | Verifica que todos los enlaces del `_sidebar.md` tengan un archivo correspondiente y viceversa. |
| `verificar_pre_ingesta.py` | Comprueba que el mapa de encabezados y el índice estén sincronizados antes de ingerir. |
| `wiki_cli.py` | Interfaz de línea de comandos que agrupa los pasos habituales (convertir, indexar e ingerir). |

| `exportar_modulo.py` | Convierte todos los `.md` de una carpeta en un PDF único utilizando Pandoc. |
