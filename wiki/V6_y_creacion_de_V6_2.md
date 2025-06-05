### 3.1.3. V6 y creación de V6_2

### 3.1.3. V6 y creación de V6_2

La base de datos V6 contiene los datos de **Necor@V6** tras la migración. Durante el proceso, se detectó que algunas vistas aplicaban filtros que impedían consultar el histórico completo desde Necor@. Para solucionarlo:

- Se creó la base V6_2, réplica exacta de V6 sin filtros de migración.

- Se generaron nuevas vistas \_V sobre V6_2.

- Se reemplazaron los sinónimos en V6 para que apunten a estas vistas no filtradas.

- Las vistas originales se renombraron como \_BKP para permitir comparativas de rendimiento.

- Se reforzaron índices en tablas clave (BO12SQ, BO59SQ, BO80SQ, etc.) y se revisaron procedimientos (PR_NC_CONSULTA_OPERACIONES, etc.).

Esta estrategia permite que **Necor@V6 acceda al histórico completo sin afectar al código existente**, manteniendo la trazabilidad y cumpliendo requerimientos funcionales de Ingeniería y Auditoría.

.
