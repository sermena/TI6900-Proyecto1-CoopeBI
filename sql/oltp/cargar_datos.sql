-- =====================================================================
-- Proyecto 1 BI: Carga completa
-- Crea las tablas y carga los datos generados
-- =====================================================================

\set ON_ERROR_STOP on
\encoding UTF8

CREATE SCHEMA IF NOT EXISTS coopebi;
SET search_path TO coopebi;

\echo 'Creando tablas...'
\ir tablas.sql

\echo 'Cargando datos...'
\ir ../../data/raw/datos_region.sql
\ir ../../data/raw/datos_ubicacion.sql
\ir ../../data/raw/datos_segmento.sql
\ir ../../data/raw/datos_cliente.sql
\ir ../../data/raw/datos_tipo_credito.sql
\ir ../../data/raw/datos_producto_credito.sql
\ir ../../data/raw/datos_agencia.sql
\ir ../../data/raw/datos_credito.sql
\ir ../../data/raw/datos_canal_pago.sql
\ir ../../data/raw/datos_rango_atraso.sql
\ir ../../data/raw/datos_tipo_comision.sql
\ir ../../data/raw/datos_pago.sql
\ir ../../data/raw/datos_interes.sql
\ir ../../data/raw/datos_comision.sql
\ir ../../data/raw/datos_morosidad.sql

\echo 'Carga terminada.'
