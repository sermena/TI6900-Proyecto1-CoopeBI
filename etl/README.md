# etl

Proyecto de **Apache Hop** que lleva los datos del OLTP al Data Warehouse.

- `apache-hop/pipelines/` — transformaciones (`.hpl`), una por dimensión o tabla de hechos: `carga_dim_agencia.hpl`, `carga_fact_credito.hpl`.
- `apache-hop/workflows/` — orquestación (`.hwf`). El workflow principal `wf_carga_dw.hwf` ejecuta primero las dimensiones y después los hechos.

Las conexiones a PostgreSQL se definen con variables de entorno de Hop (`${PG_HOST}`, `${PG_USER}`, `${PG_PASSWORD}`); no se guardan contraseñas en el repositorio.
