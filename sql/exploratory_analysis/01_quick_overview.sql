-- ============================================================
-- sql/exploratory_analysis/01_quick_overview.sql
-- Run these first after loading data to sanity-check the DWH.
-- ============================================================

-- 1. Row counts in all DWH tables
SELECT 'dim_date'        AS table_name, COUNT(*) AS rows FROM dwh.dim_date
UNION ALL SELECT 'dim_customer',  COUNT(*) FROM dwh.dim_customer
UNION ALL SELECT 'dim_product',   COUNT(*) FROM dwh.dim_product
UNION ALL SELECT 'dim_store',     COUNT(*) FROM dwh.dim_store
UNION ALL SELECT 'dim_campaign',  COUNT(*) FROM dwh.dim_campaign
UNION ALL SELECT 'fact_sales',    COUNT(*) FROM dwh.fact_sales
UNION ALL SELECT 'fact_inventory',COUNT(*) FROM dwh.fact_inventory
UNION ALL SELECT 'fact_marketing',COUNT(*) FROM dwh.fact_marketing
ORDER BY table_name;

-- 2. Overall sales summary
SELECT
    COUNT(*)                         AS total_transactions,
    COUNT(DISTINCT customer_sk)      AS unique_customers,
    COUNT(DISTINCT product_sk)       AS unique_products,
    COUNT(DISTINCT store_sk)         AS unique_stores,
    MIN(date_key)                    AS earliest_sale,
    MAX(date_key)                    AS latest_sale,
    ROUND(SUM(net_revenue), 2)       AS total_revenue,
    ROUND(SUM(gross_profit), 2)      AS total_profit,
    ROUND(AVG(net_revenue), 2)       AS avg_order_value
FROM dwh.fact_sales;

-- 3. Top 5 categories by revenue (quick check)
SELECT
    p.category,
    ROUND(SUM(f.net_revenue), 2) AS revenue
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.category
ORDER BY revenue DESC
LIMIT 5;

-- 4. Revenue by year
SELECT
    d.year,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    COUNT(*) AS orders
FROM dwh.fact_sales f
JOIN dwh.dim_date d ON d.date_key = f.date_key
GROUP BY d.year
ORDER BY d.year;

-- 5. Payment method split
SELECT
    payment_method,
    COUNT(*)                           AS orders,
    ROUND(COUNT(*) * 100.0
          / SUM(COUNT(*)) OVER (), 2)  AS pct_of_orders
FROM dwh.fact_sales
GROUP BY payment_method
ORDER BY orders DESC;
