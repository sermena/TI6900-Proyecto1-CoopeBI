-- =====================================================================
-- Proyecto 1 BI: Script maestro
-- Crea la base de datos, el esquema, las tablas y carga los datos
-- =====================================================================

\set ON_ERROR_STOP on
\encoding UTF8

-- Base de datos (solo se crea si no existe)
\echo 'Creando base de datos...'
SELECT 'CREATE DATABASE proyecto_1_bi'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'proyecto_1_bi')
\gexec

\c proyecto_1_bi

-- Esquema
\echo 'Creando esquema...'
CREATE SCHEMA IF NOT EXISTS coopebi;
SET search_path TO coopebi;

-- Tablas, llaves e índices
\echo 'Creando tablas...'
\ir tablas.sql

-- Datos
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

-- Resumen de la carga
\echo 'Filas cargadas por tabla:'
SELECT 'region' AS tabla, COUNT(*) AS filas FROM region
UNION ALL SELECT 'ubicacion', COUNT(*) FROM ubicacion
UNION ALL SELECT 'segmento', COUNT(*) FROM segmento
UNION ALL SELECT 'cliente', COUNT(*) FROM cliente
UNION ALL SELECT 'tipo_credito', COUNT(*) FROM tipo_credito
UNION ALL SELECT 'producto_credito', COUNT(*) FROM producto_credito
UNION ALL SELECT 'agencia', COUNT(*) FROM agencia
UNION ALL SELECT 'credito', COUNT(*) FROM credito
UNION ALL SELECT 'canal_pago', COUNT(*) FROM canal_pago
UNION ALL SELECT 'rango_atraso', COUNT(*) FROM rango_atraso
UNION ALL SELECT 'tipo_comision', COUNT(*) FROM tipo_comision
UNION ALL SELECT 'pago', COUNT(*) FROM pago
UNION ALL SELECT 'interes', COUNT(*) FROM interes
UNION ALL SELECT 'comision', COUNT(*) FROM comision
UNION ALL SELECT 'morosidad', COUNT(*) FROM morosidad;

\echo 'Base de datos lista.'
