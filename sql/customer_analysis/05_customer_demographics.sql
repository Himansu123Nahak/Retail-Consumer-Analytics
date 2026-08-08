-- ============================================================
-- sql/customer_analysis/05_customer_demographics.sql
-- Revenue and orders by customer demographics.
-- Age group, gender, income segment, region breakdowns.
-- Basic: JOIN, GROUP BY, ORDER BY
-- ============================================================

-- Revenue by age group
SELECT
    c.age_group,
    COUNT(DISTINCT f.customer_sk)  AS unique_customers,
    COUNT(f.sale_sk)               AS total_orders,
    ROUND(SUM(f.net_revenue), 2)   AS total_revenue,
    ROUND(AVG(f.net_revenue), 2)   AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.age_group
ORDER BY total_revenue DESC;

-- Revenue by gender
SELECT
    c.gender,
    COUNT(DISTINCT f.customer_sk) AS unique_customers,
    COUNT(f.sale_sk)              AS total_orders,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue,
    ROUND(AVG(f.net_revenue), 2)  AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.gender
ORDER BY total_revenue DESC;

-- Revenue by income segment
SELECT
    c.income_segment,
    COUNT(DISTINCT f.customer_sk) AS unique_customers,
    COUNT(f.sale_sk)              AS total_orders,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue,
    ROUND(AVG(f.net_revenue), 2)  AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.income_segment
ORDER BY total_revenue DESC;

-- Revenue by customer region
SELECT
    c.region,
    COUNT(DISTINCT f.customer_sk) AS unique_customers,
    COUNT(f.sale_sk)              AS total_orders,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.region
ORDER BY total_revenue DESC;
