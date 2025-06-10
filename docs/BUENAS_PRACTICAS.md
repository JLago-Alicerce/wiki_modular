# Buenas prácticas

Este proyecto cuenta con dos componentes clave para mantener la wiki al día:

 - **Alimentador de documentación** (`procesar_nuevos.py` o `wiki_cli.py`): se encarga de convertir los nuevos archivos `.docx` o `.pdf` y generar las páginas correspondientes.
- **Supervisor de índices** (`verificar_pre_ingesta.py` y herramientas de generación de índices): comprueba que el mapa de encabezados y el índice estén sincronizados para evitar enlaces rotos.

A nivel de uso diario se recomienda:

1. **Organizar la carpeta `_fuentes/_originales`**
   - Mantenga aquí únicamente los documentos pendientes de procesar (tanto `.docx` como `.pdf`).
   - El alimentador registrará cada archivo en `procesados.log` para no repetir trabajos.
2. **Ejecutar el alimentador desde un entorno limpio**
   - Si es la primera carga o se han eliminado archivos manualmente, corra `resetear_entorno.py` antes de procesar.
   - Utilice `wiki_cli.py full <ruta>` para ejecutar todo el flujo sobre un archivo concreto o una carpeta con `.docx` y `.pdf`.
3. **Revisar los mensajes del alimentador**
   - Ante cualquier advertencia sobre coincidencias difusas, revise `alias_override.yaml` para forzar rutas correctas.
4. **Validar el índice periódicamente**
   - El supervisor de índices permite detectar títulos sin correspondencia antes de la ingesta con `verificar_pre_ingesta.py`.
   - Después de generar o modificar `index_PlataformaBBDD.yaml`, ejecute `generar_sidebar.py --tolerant` y `auditar_sidebar_vs_fs.py` para comprobar que no haya enlaces huérfanos.
5. **Mantener el repositorio versionado**
   - Incluya el índice YAML y los archivos procesados en control de versiones para poder revertir cambios si es necesario.
   - Documente en los commits cualquier ajuste manual aplicado al índice o a los slugs.

Seguir estas pautas ayuda a que el servicio de generación de la wiki sea consistente y rápido, evitando reprocesamientos innecesarios y minimizando los errores en los enlaces.

## Preparación del documento `.docx`

Para obtener una conversión limpia conviene cuidar la estructura del archivo original:

* Utilice los estilos de Word **Título 1**, **Título 2**, etc. para marcar los encabezados. El generador de índices se apoya en esos estilos para crear los slugs de cada sección.
* Evite numerar manualmente las secciones o aplicar formatos personalizados; deje que Word gestione la numeración.
* Inserte las imágenes de forma directa (copiar y pegar) y con un tamaño razonable. Estas se extraerán a `wiki/assets` durante la conversión.
* Procure que las tablas no contengan celdas anidadas ni combinadas de manera compleja. Pandoc procesa mejor las tablas simples.
* Guarde el documento final en formato `.docx` sin macros ni campos especiales para evitar advertencias.

Si el documento respeta estas reglas, la generación de la wiki será más fiable y requerirá menos ajustes manuales.

