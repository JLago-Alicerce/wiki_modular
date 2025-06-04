### 3.6.2. Funciones y contexto

### 3.6.2. Funciones y contexto

- **Integración:** Hospeda el WebService NecoraMQ (NecoraWebIntegrator.svc), que expone operaciones SOAP y REST para consulta y validación de materiales, órdenes y hojas de catálogo. Las peticiones se comunican con HOSTDB2 vía ODBC configurado con puerto TCP fijo 1452, garantizando seguridad mediante TLS 1.2 y autenticación por token renovable anualmente.

- **Gestión documental:** Mantiene el almacén físico de documentos digitales (PDFs, hojas técnicas, planos) usados por aplicaciones Necor@AWD, Necor@NC y otras, compartidos vía SMB para acceso interno.

- **Migración:** Resultado de la migración parcial desde el antiguo servidor MANECNET, apagado en octubre de 2024. Se trasladaron únicamente componentes documentales y servicios de integración, descartando la migración completa de Necor@V6.

3.6.3. Cronología de migración y normalización

![](wiki/assets/media/image1.jpg){width="7.184722222222222in" height="1.7840277777777778in"}

Figura 3.6-2 presenta la cronología del proceso de migración desde MANECNET a MASERVF9 y la estabilización del flujo de materiales, que se desarrolló entre el 23 de octubre de 2024 y el 8 de enero de 2025.
