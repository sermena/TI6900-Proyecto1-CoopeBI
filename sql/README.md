# sql

| Carpeta | Contenido |
|---|---|
| `oltp/` | DDL e inserción de datos de la base transaccional (clientes, créditos, pagos, agencias). |
| `dw/` | DDL del Data Warehouse: dimensiones (`dim_*`) y tablas de hechos (`fact_*`). |
| `consultas/` | Consultas de validación de la carga y consultas que responden BQ-01 a BQ-05. |

Los scripts se numeran en el orden en que deben ejecutarse: `01_crear_esquema.sql`, `02_...`.
Las consultas de respuesta se nombran por pregunta: `bq01_montos_colocados.sql`, `bq02_morosidad.sql`, etc.
