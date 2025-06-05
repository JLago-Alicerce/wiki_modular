### 3.6.5. Lecciones aprendidas y recomendaciones

### 3.6.5. Lecciones aprendidas y recomendaciones

- Documentar exhaustivamente las dependencias de puertos SQL, evitando asignaciones dinámicas.

- Validar cambios en entornos espejo o pre-producción antes de desactivar sistemas legados.

- Automatizar pruebas E2E (SOAP-UI CLI + SQL ping) tras cada modificación infraestructural.

- Configurar alertas Centreon para códigos HTTP 5xx en el servicio NecoraWebIntegrator.
