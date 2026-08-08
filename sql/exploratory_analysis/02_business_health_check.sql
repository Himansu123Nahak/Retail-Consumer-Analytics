-- ============================================================
-- sql/exploratory_analysis/02_business_health_check.sql
-- Quick business health dashboard — run after loading data
-- to validate all key metrics in one query.
-- Basic SQL: COUNT, SUM, AVG, GROUP BY
-- ============================================================

-- Full business snapshot
SELECT 'Total Revenue (INR)'            AS metric,
       CAST(ROUND(SUM(net_revenue), 0) AS TEXT) AS value
FROM dwh.fact_sales
UNION ALL
SELECT 'Total Orders',      CAST(COUNT(sale_sk) AS TEXT)               FROM dwh.fact_sales
UNION ALL
SELECT 'Total Customers',   CAST(COUNT(DISTINCT customer_sk) AS TEXT)  FROM dwh.fact_sales
UNION ALL
SELECT 'Avg Order Value',   CAST(ROUND(AVG(net_revenue), 2) AS TEXT)   FROM dwh.fact_sales
UNION ALL
SELECT 'Total Units Sold',  CAST(SUM(quantity) AS TEXT)                FROM dwh.fact_sales
UNION ALL
SELECT 'Total Profit',      CAST(ROUND(SUM(gross_profit), 0) AS TEXT)  FROM dwh.fact_sales
UNION ALL
SELECT 'Distinct Products', CAST(COUNT(DISTINCT product_sk) AS TEXT)   FROM dwh.fact_sales
UNION ALL
SELECT 'Distinct Stores',   CAST(COUNT(DISTINCT store_sk) AS TEXT)     FROM dwh.fact_sales
UNION ALL
SELECT 'Date Range Start',  CAST(MIN(d.full_date) AS TEXT)
  FROM dwh.fact_sales f JOIN dwh.dim_date d ON d.date_key = f.date_key
UNION ALL
SELECT 'Date Range End',    CAST(MAX(d.full_date) AS TEXT)
  FROM dwh.fact_sales f JOIN dwh.dim_date d ON d.date_key = f.date_key;

-- Row counts per table
SELECT table_name,
       CAST(row_count AS TEXT) AS rows
FROM (
    SELECT 'dim_customer'   AS table_name, COUNT(*) AS row_count FROM dwh.dim_customer
    UNION ALL
    SELECT 'dim_product',                  COUNT(*)              FROM dwh.dim_product
    UNION ALL
    SELECT 'dim_store',                    COUNT(*)              FROM dwh.dim_store
    UNION ALL
    SELECT 'dim_date',                     COUNT(*)              FROM dwh.dim_date
    UNION ALL
    SELECT 'fact_sales',                   COUNT(*)              FROM dwh.fact_sales
    UNION ALL
    SELECT 'fact_inventory',               COUNT(*)              FROM dwh.fact_inventory
    UNION ALL
    SELECT 'fact_marketing',               COUNT(*)              FROM dwh.fact_marketing
) counts
ORDER BY table_name;
