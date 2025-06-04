## 4.2. Interfaces de carga principales

## 4.2. Interfaces de carga principales

Las dos cargas operativas clave son:

+---------------------+-------------------------------------------+--------------------------------------------------------------------------------+
| > **Job**           | > **Instancia**                           | > **Descripción**                                                              |
+---------------------+-------------------------------------------+--------------------------------------------------------------------------------+
| > **Job 21: Carga** | > MASQL20142\\NECORANET.InterfacesAWD_PEC | > Integra información desde SAP, ECADAT y PRYC. Aplica validaciones iniciales. |
+---------------------+-------------------------------------------+--------------------------------------------------------------------------------+
| > **Job 22: Carga** | NAILInterfacesAWD                         | > Permite mantener consistencia en el modelo                                   |
+---------------------+-------------------------------------------+--------------------------------------------------------------------------------+
| > **Job**           | > **Instancia**                           | > **Descripción**                                                              |
+---------------------+-------------------------------------------+--------------------------------------------------------------------------------+
| **Nail PEC**        |                                           | > PEC, especializado para entornos AWD.                                        |
+=====================+===========================================+================================================================================+

Ambos jobs están planificados como procesos automáticos, bajo SQL Agent, con control de errores y trazabilidad mediante logs.
