### 3.1.5. Interfaces SSIS en entorno HOST consolidado (AWD/ALHD)

### 3.1.5. Interfaces SSIS en entorno HOST consolidado (AWD/ALHD)

En el marco del proyecto de migración del entorno HOST, se definieron y desplegaron múltiples paquetes SSIS bajo la codificación INTERFACES_AWD_ALHD_SSIS. Estos paquetes están orientados a la integración y consolidación de datos técnicos, documentos y órdenes asociadas a los sistemas heredados, facilitando la automatización de tareas críticas.

> **(a) Funciones de los Paquetes SSIS**

Los paquetes SSIS permiten la automatización de las siguientes tareas críticas:

- **Extracción y limpieza de datos:** Utilizando paquetes como \_AtributosConfig.dtsx y \_LimpiarLogs.dtsx, se asegura la integridad y calidad de los datos extraídos.

- **Actualización de estados en tablas funcionales:** El paquete \_StatusDeleted.dtsx gestiona la actualización de estados, asegurando que las tablas reflejen el estado actual de los registros.

- **Consolidación de documentos técnicos:** Paquetes como Documentos_tecnicos\_\*.dtsx consolidan documentos técnicos, garantizando que toda la información relevante esté centralizada y accesible.

- **Gestión documental completa:** Los paquetes Gestion_Documental\_\*.dtsx abarcan revisiones, anexos, secciones y ficheros, proporcionando una gestión integral de los documentos.

- **Interfaces con MEL y materiales:** Los paquetes MEL_LME\_\*.dtsx facilitan la integración con sistemas de materiales, asegurando que los datos estén alineados con los requerimientos técnicos.

- **Interfaces con el entorno EEA5:** Paquetes como EEA5.dtsx y EEA5_DB2.dtsx permiten la comunicación y sincronización con el entorno EEA5, asegurando que los datos sean consistentes y actualizados.

> **(b) Características Técnicas**

Los scripts SSIS incluyen lógica avanzada para:

- **Detección de registros huérfanos:** Identificación y manejo de registros que no tienen correspondencia en otras tablas, asegurando la integridad referencial.

- **Actualizaciones incrementales:** Implementación de actualizaciones que solo afectan a los registros modificados, optimizando el rendimiento y reduciendo la carga del sistema.

- **Verificación de consistencia:** Uso de checksum para asegurar que los campos clave mantienen su consistencia, evitando discrepancias en los datos.

- **Limpieza de registros obsoletos:** Eliminación de registros con estado status = \'DELETED\', asegurando que la base de datos no acumule información innecesaria.

Además, se emplea el objeto UpdateNotice como mecanismo de auditoría de ejecución para los procesos de carga diarios, proporcionando un registro detallado de las operaciones realizadas y facilitando el seguimiento y control de las mismas.
