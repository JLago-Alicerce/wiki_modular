# Uso de `alias_override.yaml`

El archivo `_fuentes/alias_override.yaml` permite forzar la ruta de ciertos títulos cuando
el algoritmo de coincidencia difusa no encuentra un destino adecuado.
Se trata de un mapeo YAML sencillo donde la clave es el título original
y el valor es la ruta relativa dentro de `wiki/` (con extensión `.md`).

```yaml
"Instalación Avanzada": "instalacion_avanzada_personalizada"
"Configuración PAD": "configuracion_pad"
```

Durante la ingesta, si un título coincide exactamente con alguna clave del
archivo, el bloque se escribirá en la ruta indicada sin aplicar "fuzzy matching".
De este modo se pueden resolver manualmente excepciones o nombres ambiguos.

## Revisión de sugerencias

Cuando `ingest_wiki_v2.py` no encuentra destino para un título, el script lo
guarda en `wiki/99_Nuevas_Secciones` y añade una fila al archivo
`_fuentes/alias_suggestions.csv` con dos columnas: el título original y el slug
sugerido. Para incorporarlas:

1. Abra `_fuentes/alias_suggestions.csv` en un editor de texto o una hoja de
   cálculo.
2. Revise cada par título/slug y decida la ruta definitiva deseada.
3. Añada esas entradas en `_fuentes/alias_override.yaml` con la sintaxis
   `"Título": "ruta/slug"`.
4. Vuelva a ejecutar la ingesta especificando `--alias _fuentes/alias_override.yaml`.

Tras incorporar las sugerencias puede eliminar el CSV o dejarlo para referencia.

