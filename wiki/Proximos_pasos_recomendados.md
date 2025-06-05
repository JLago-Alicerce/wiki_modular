# 6. Próximos pasos recomendados

# 6. Próximos pasos recomendados 

El principal hito pendiente identificado a corto-medio plazo es la **migración completa de las instancias actuales en MA SQL20142 (tanto SQL20142 como NECORANET) hacia una nueva instancia consolidada MA SQL20222 basada en SQL Server 2022**. Esta acción, alineada con las políticas de modernización tecnológica y soporte de plataforma, implicará una revisión exhaustiva de todo el entorno actual.

Dicha revisión debe incluir:

- **Análisis y validación de compatibilidad** de procedimientos almacenados, funciones, vistas y sinónimos actualmente en uso.

- **Revisión de flujos ETL, enlaces de servidor y servicios asociados** (como Reporting Services y Power BI).

- **Evaluación de vistas funcionales y refactorización de estructuras heredadas**, con el objetivo de simplificar lógicas innecesarias y mejorar el rendimiento global.

- **Homologación de estándares técnicos**: nombres de objetos, collation, agrupación de esquemas por rol funcional, etc.

- **Prueba completa de rendimiento comparado**, para asegurar que la nueva instancia mantiene o mejora los tiempos actuales, especialmente en vistas \_V, índices aplicados y llamadas desde Necor@.

Este proceso no solo permitirá abandonar entornos sin soporte y reducir riesgos operativos, sino que abrirá la puerta a **implementar buenas prácticas y optimizaciones** que en el estado actual están condicionadas por la necesidad de mantener compatibilidad hacia atrás.

Adicionalmente, se recomienda:

- Consolidar backups y planes de mantenimiento en entornos más robustos (Azure SQL Managed Instance en el medio plazo).

- Ampliar los mecanismos de alertas y trazabilidad, especialmente en entornos internacionales.

Estas acciones permitirán avanzar hacia una **plataforma unificada, segura y preparada para integraciones futuras**, cumpliendo con los requisitos operativos internos y externos de Navantia.
