-- ============================================================
-- sql/schema/00_create_database.sql
-- Creates the retail_analytics database and schemas.
-- Run as superuser BEFORE all other SQL scripts.
-- ============================================================

-- Create database (run from psql as postgres)
-- CREATE DATABASE retail_analytics;
-- \c retail_analytics

-- Schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dwh;
CREATE SCHEMA IF NOT EXISTS analytics;

COMMENT ON SCHEMA staging   IS 'Raw loaded data before transformations';
COMMENT ON SCHEMA dwh       IS 'Star schema — dimension and fact tables';
COMMENT ON SCHEMA analytics IS 'Pre-built analytical views for BI / reporting';
