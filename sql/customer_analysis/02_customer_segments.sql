-- ============================================================
-- sql/customer_analysis/02_customer_segments.sql
-- Revenue and orders broken down by customer attributes.
-- Basic: JOIN, GROUP BY, ORDER BY
-- ============================================================

-- By gender
SELECT
    c.gender,
    COUNT(DISTINCT f.customer_sk)   AS total_customers,
    COUNT(f.sale_sk)                AS total_orders,
    ROUND(SUM(f.net_revenue), 2)    AS total_revenue,
    ROUND(AVG(f.net_revenue), 2)    AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.gender
ORDER BY total_revenue DESC;

-- By age group
SELECT
    c.age_group,
    COUNT(DISTINCT f.customer_sk)   AS total_customers,
    COUNT(f.sale_sk)                AS total_orders,
    ROUND(SUM(f.net_revenue), 2)    AS total_revenue,
    ROUND(AVG(f.net_revenue), 2)    AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.age_group
ORDER BY c.age_group;

-- By income segment
SELECT
    c.income_segment,
    COUNT(DISTINCT f.customer_sk)   AS total_customers,
    COUNT(f.sale_sk)                AS total_orders,
    ROUND(SUM(f.net_revenue), 2)    AS total_revenue,
    ROUND(AVG(f.net_revenue), 2)    AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.income_segment
ORDER BY total_revenue DESC;
