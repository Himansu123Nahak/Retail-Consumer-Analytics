-- ============================================================
-- sql/schema/create_all.sql
-- Master script — runs all schema creation in order.
-- Run this once on a fresh retail_analytics database:
--   psql -U postgres -d retail_analytics -f sql/schema/create_all.sql
-- ============================================================

\echo 'Creating schemas...'
\i sql/schema/00_create_database.sql

\echo 'Creating dim_date...'
\i sql/schema/01_dim_date.sql

\echo 'Creating dimension tables...'
\i sql/schema/02_dim_tables.sql

\echo 'Creating fact tables...'
\i sql/schema/03_fact_tables.sql

\echo 'Schema creation complete.'
