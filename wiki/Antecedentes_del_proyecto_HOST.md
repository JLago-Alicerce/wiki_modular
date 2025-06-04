### 3.1.4. Antecedentes del proyecto HOST

### 3.1.4. Antecedentes del proyecto HOST

El proyecto HOST se concibió como una iniciativa de migración y mantenimiento de los sistemas legacy (DB2/VSAM), gestionándose bajo un modelo mixto que combina soporte y transferencia de conocimiento. En colaboración con Altia Consultores, se llevaron a cabo tareas de mantenimiento correctivo y adaptativo, así como procesos de migración escalonada.

Esta colaboración se alineó con las prácticas ITIL y los estándares ISO/IEC 20000, estableciendo una infraestructura de servicio que incluyó indicadores de calidad (SLA), herramientas de gestión, dedicación de recursos y mecanismos de seguimiento tanto semanal como mensual. Además, se garantizó una cobertura integral sobre aplicaciones críticas (Necora, Coral, ControlDoc, Brion, entre otras) mediante soporte de tercer nivel y supervisión de procesos en explotación.

El acuerdo contemplaba una planificación detallada de proyectos, atención 24x7 para casos críticos y controles de calidad periódicos. Se documentaron procedimientos para el análisis y resolución de incidentes, gestión de problemas y planificación de desarrollos, lo que permitió asegurar la continuidad del servicio durante la migración al entorno SQL Server (MASQL20171\\HOSTDB2) sin pérdida de operatividad.

El proyecto de migración HOST se inició el **12 de septiembre de 2019** y se estructuró en dos fases:

- **Fase I -- Migración técnica:** de septiembre de 2019 a julio de 2020.

- **Fase II -- Soporte y cierre definitivo:** de julio a diciembre de 2020.

**Objetivos del proyecto:**

- Eliminar el sistema HOST (z/OS + DB2 + VSAM).

- Garantizar la continuidad operativa en Necor@NET y PRYC.

- Mantener los interfaces activos con clientes externos.

- Migrar la información documental y estructural a un entorno soportado (SQL Server 2017).

**Logros y aspectos técnicos:**

- Más de **30 tablas y 4 ficheros VSAM** migrados utilizando IBM DataUnload.

- Pruebas de carga realizadas en el entorno staging (FESRV053) y New PRYC.

- Validación funcional con la obra 7564 (Turbinas) como proyecto piloto.

- Generación de documentación de procesos y reglas de negocio aplicadas a interfaces AWD.  Integración de cargas documentales desde Windchill.

**Riesgos abordados:**

- No disponibilidad del entorno HOST de desarrollo.

- Falta de programas COBOL (por ejemplo, PE46FV).

- Ausencia de estimación de tamaños de bases de datos debido a retrasos con VSAM.

- Problemas de permisos y catálogo con IBM.

- Recursos técnicos limitados (servidores, estaciones de trabajo, permisos).

**Participantes clave:**

**Área Personal asignado**

> Migración de datos DB2 Navantia: F. Amor, A. Rodríguez · Altia: J.R. Tubío, D. Vega, J. Díaz
>
> Interfaces Externos Navantia: Y. Castiñeira, F. Bordello · Altia: mismos Obra de Turbinas Navantia: F. Bordello · Altia: D. Vega

**Fechas clave:**

- Fin de migración técnica: **15 de julio de 2020**.

- Cierre del entorno HOST: **31 de diciembre de 2020**.

- Desactivación de IBM y licencias: **Q4 2020**.

![](wiki/assets/media/image3.jpg){width="6.3381944444444445in" height="1.3958333333333333in"}
