-- ============================================================
-- sql/sales_analysis/09_yoy_growth.sql
-- Year-over-Year revenue growth by category.
-- Shows which categories grew and which declined.
-- Basic SQL: GROUP BY, CASE, subquery
-- ============================================================

-- Annual revenue by category
SELECT
    p.category,
    d.year,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    COUNT(f.sale_sk)             AS orders
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
JOIN dwh.dim_date    d ON d.date_key    = f.date_key
GROUP BY p.category, d.year
ORDER BY p.category, d.year;

-- Total YoY revenue growth per year
SELECT
    d.year,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue,
    COUNT(f.sale_sk)               AS total_orders,
    COUNT(DISTINCT f.customer_sk)  AS unique_customers,
    ROUND(AVG(f.net_revenue), 2)   AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_date d ON d.date_key = f.date_key
GROUP BY d.year
ORDER BY d.year;

-- Monthly revenue with running total
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.net_revenue), 2)        AS monthly_revenue,
    ROUND(SUM(SUM(f.net_revenue))
          OVER (PARTITION BY d.year
                ORDER BY d.month), 2)   AS ytd_revenue
FROM dwh.fact_sales f
JOIN dwh.dim_date d ON d.date_key = f.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
