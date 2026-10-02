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
\ir ../../data/datos_region.sql
\ir ../../data/datos_ubicacion.sql
\ir ../../data/datos_segmento.sql
\ir ../../data/datos_cliente.sql
\ir ../../data/datos_tipo_credito.sql
\ir ../../data/datos_producto_credito.sql
\ir ../../data/datos_agencia.sql
\ir ../../data/datos_credito.sql
\ir ../../data/datos_canal_pago.sql
\ir ../../data/datos_rango_atraso.sql
\ir ../../data/datos_tipo_comision.sql
\ir ../../data/datos_pago.sql
\ir ../../data/datos_interes.sql
\ir ../../data/datos_comision.sql
\ir ../../data/datos_morosidad.sql

\echo 'Carga terminada.'
