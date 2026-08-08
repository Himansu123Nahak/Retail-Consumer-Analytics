-- ============================================================
-- sql/customer_analysis/01_customer_overview.sql
-- Total customers, active customers, new customers by year.
-- Basic: JOIN, GROUP BY, COUNT DISTINCT
-- ============================================================

-- Overall customer counts
SELECT
    COUNT(DISTINCT f.customer_sk)  AS total_customers_with_purchase,
    COUNT(DISTINCT f.sale_sk)      AS total_orders,
    ROUND(SUM(f.net_revenue), 2)   AS total_revenue,
    ROUND(SUM(f.net_revenue)
          / NULLIF(COUNT(DISTINCT f.customer_sk), 0), 2)
                                   AS revenue_per_customer
FROM dwh.fact_sales f;

-- New customers per year (first purchase year)
SELECT
    d.year,
    COUNT(DISTINCT f.customer_sk) AS new_customers
FROM dwh.fact_sales f
JOIN dwh.dim_date d ON d.date_key = f.date_key
WHERE NOT EXISTS (
    -- Customer has no purchase before this year
    SELECT 1
    FROM dwh.fact_sales f2
    JOIN dwh.dim_date d2 ON d2.date_key = f2.date_key
    WHERE f2.customer_sk = f.customer_sk
      AND d2.year < d.year
)
GROUP BY d.year
ORDER BY d.year;
