### 3.5.2. Contexto y dependencias

### 3.5.2. Contexto y dependencias

Esta instancia, basada en SQL Server 2022, da soporte a proyectos desplegados en Noruega y contiene su propia versión de Necor@AWD. Replica los datos de forma independiente desde el PDB general, asegurando autonomía y seguridad en la gestión de información.

El flujo ETL, pionero en validación completa, incorpora trazabilidad end-to-end desde las fuentes Coral hasta la explotación en Power BI, pasando por etapas de staging, validación y carga incremental.

Los procesos diarios están optimizados para manejar grandes volúmenes de datos ---más de 2 millones de registros por carga--- con tiempos inferiores a 40 minutos. El entorno dispone de alertas y logs que permiten monitorizar el estado de sincronización, errores y métricas clave.

Esta instancia es un referente técnico para futuros despliegues en entornos similares, demostrando la viabilidad de operaciones con réplicas distribuidas, controladas y auditables.

Actualmente, la base de datos que alimenta el PDB de Noruega está en fase de migración, en preparación para el apagado gradual de la instancia legacy MASQL2014\\SQLNORWAY.
