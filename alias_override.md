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

## Sugerencias automáticas

Cuando un título no obtiene coincidencia se guarda una propuesta en
`_fuentes/alias_suggestions.csv` (o el archivo indicado con `--suggestions`).
Cada entrada contiene el título original y el slug normalizado. Revise este
archivo tras la ingesta y copie las filas pertinentes a `alias_override.yaml` para
que se apliquen en la siguiente ejecución. Puede eliminar las sugerencias una
vez incorporadas.

