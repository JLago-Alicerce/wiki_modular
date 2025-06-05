### 3.1.2. Contenido migrado

### 3.1.2. Contenido migrado

MASQL20171\\HOSTDB2 almacena la información consolidada desde tres orígenes principales:

+--------------+------------------------------------+-----------------------------------------------------------------------------------------------+
| > **Origen** | > **Destino en SQL Server**        | > **Descripción**                                                                             |
+--------------+------------------------------------+-----------------------------------------------------------------------------------------------+
| HOST DB2     | > DB2T / DB2P                      | > Copia exacta de tablas fuente dentro del alcance. Carga vía paquete MoveDataDB2ToSQLServer. |
+--------------+------------------------------------+-----------------------------------------------------------------------------------------------+
| FESRV014     | > HOSTDB2 (diversos esquemas)      | > Bases de datos ControlDoc, ControlAsuntos, etc. Job: MoveAppAuxToNewNecor@.                 |
+--------------+------------------------------------+-----------------------------------------------------------------------------------------------+
| MAHOST       | > HOSTDB2.DB2T (esquema a esquema) | > Bases DBFERR, DBCART, DBMADR, DBSFER. Job: PackageMAHOST_a_DB2T.dtsx.                       |
+==============+====================================+===============================================================================================+
