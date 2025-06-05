### 4.4.1. Integración ampliada del modelo funcional -- Foran \<-\> Windchill \<-\> SAP

### 4.4.1. Integración ampliada del modelo funcional -- Foran \<-\> Windchill \<-\> SAP

Dentro del modelo operativo ampliado para entornos de Ingeniería, se ha establecido una arquitectura de integración funcional entre los sistemas Foran, Windchill y SAP. Esta arquitectura automatiza la conversión, vinculación y sincronización de las estructuras de producto (EBOM/MBOM), documentos técnicos y órdenes planificadas, facilitando la trazabilidad y coherencia en todo el ciclo de vida del producto.

El flujo se articula en torno a los siguientes conceptos clave:

- **EBOM (Design View) y MBOM (Manufacturing View):** Generadas desde los módulos de Foran (FBUILDS, FDESIGN, FSYSD, FNEST), representan respectivamente la estructura de diseño y fabricación del producto.

- **Documentos IDD/IP:** Creación, gestión y aprobación dentro de Windchill, con trazabilidad detallada de revisiones y estados.

- **Publicación y vinculación automática:** Los materiales y documentos se publican desde Foran hacia Windchill, y posteriormente se sincronizan con SAP, garantizando la consistencia de la información.

- **Estructuras de planificación y órdenes previsionales:** Se transfieren a SAP (etapas OPrev1, OPrev2, OP1--OP6) para su ejecución y control en planta.

Además, el modelo incluye:

- **Reglas de conversión:** Adaptadas a cada producto y tipo documental, para asegurar la correcta transformación y mapeo entre sistemas.

- **Mecanismos de verificación:** Procesos ESI y MRP integrados en el momento de la sincronización con SAP, que validan la viabilidad técnica y de planificación.

- **Integración avanzada:** Control económico, subcontratación y gestión del cambio gestionados desde Windchill mediante ProjectLink, que asegura la coherencia administrativa y técnica.

Este flujo representa el marco general para la automatización documental y de ingeniería, y es fundamental para comprender los orígenes, destinos y relaciones de la información técnica que alimenta el ecosistema de bases de datos y reporting.

![](wiki/assets/media/image4.jpg){width="7.184722222222222in" height="2.8666666666666667in"}
