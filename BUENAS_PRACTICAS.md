# Buenas prácticas

Este proyecto cuenta con dos componentes clave para mantener la wiki al día:

- **Alimentador de documentación** (`procesar_nuevos.py` o `wiki_cli.py`): se encarga de convertir los nuevos archivos `.docx` y generar las páginas correspondientes.
- **Supervisor de índices** (`verificar_pre_ingesta.py` y herramientas de generación de índices): comprueba que el mapa de encabezados y el índice estén sincronizados para evitar enlaces rotos.

A nivel de uso diario se recomienda:

1. **Organizar la carpeta `_fuentes/_originales`**
   - Mantenga aquí únicamente los documentos pendientes de procesar.
   - El alimentador registrará cada archivo en `procesados.log` para no repetir trabajos.
2. **Ejecutar el alimentador desde un entorno limpio**
   - Si es la primera carga o se han eliminado archivos manualmente, corra `resetear_entorno.py` antes de procesar.
   - Utilice `wiki_cli.py full <docx>` si desea realizar todo el flujo de una sola vez.
3. **Revisar los mensajes del alimentador**
   - Ante cualquier advertencia sobre coincidencias difusas, revise `alias_override.yaml` para forzar rutas correctas.
4. **Validar el índice periódicamente**
   - El supervisor de índices permite detectar títulos sin correspondencia antes de la ingesta con `verificar_pre_ingesta.py`.
   - Después de generar o modificar `index_PlataformaBBDD.yaml`, ejecute `generar_sidebar_desde_index.py` y `auditar_sidebar_vs_fs.py` para comprobar que no haya enlaces huérfanos.
5. **Mantener el repositorio versionado**
   - Incluya el índice YAML y los archivos procesados en control de versiones para poder revertir cambios si es necesario.
   - Documente en los commits cualquier ajuste manual aplicado al índice o a los slugs.

Seguir estas pautas ayuda a que el servicio de generación de la wiki sea consistente y rápido, evitando reprocesamientos innecesarios y minimizando los errores en los enlaces.

