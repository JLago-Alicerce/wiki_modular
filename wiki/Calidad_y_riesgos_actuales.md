# 5. Calidad y riesgos actuales

# 5. Calidad y riesgos actuales 

El sistema actual presenta un estado de operación estable, con mejoras sustanciales de rendimiento tras la consolidación de datos en instancias SQL Server modernas (2017--2022) y la reestructuración de vistas e índices. No obstante, existen **riesgos operativos y técnicos** que deben ser considerados:

- **Heterogeneidad tecnológica**: conviven versiones desde SQL Server 2008 R2 hasta 2022, lo que dificulta la unificación de estrategias de mantenimiento, backup y seguridad.

- **Instancias con soporte expirado** (MAHOST, SQL20142): aunque en modo sólo-lectura, siguen presentes en el entorno y requieren control hasta su decommission.

- **Riesgos de obsolescencia funcional**: ciertas dependencias en Necor@V6, ECADA o interfaces PEC siguen ancladas a estructuras heredadas, dificultando la modernización.

- **Puntos críticos sin HA (alta disponibilidad)**: algunas instancias claves no disponen de réplica o failover automático, lo que incrementa la exposición ante caídas no planificadas.

- **Dependencias manuales en flujos ETL**: aunque automatizados, los flujos de Turquía y Noruega aún dependen de comprobaciones visuales en ciertas etapas.

En cuanto a calidad, las mejoras en índices, sinónimos y vistas funcionales han permitido reducir los tiempos de respuesta entre un **30 % y 50 %** en procedimientos críticos. Se han implantado controles CRC y logs que aseguran trazabilidad, pero aún no existe una cobertura total de pruebas automatizadas ni de alertas proactivas de rendimiento. Se recomienda avanzar en esas áreas como parte del plan de evolución técnica.
