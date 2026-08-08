-- ============================================================
-- sql/sales_analysis/08_payment_analysis.sql
-- Revenue and order count split by payment method.
-- Shows which payment method is most popular and most valuable.
-- Basic: GROUP BY, ORDER BY, CASE
-- ============================================================

-- Revenue and orders by payment method
SELECT
    payment_method,
    COUNT(sale_sk)                AS total_orders,
    ROUND(SUM(net_revenue), 2)    AS total_revenue,
    ROUND(AVG(net_revenue), 2)    AS avg_order_value,
    ROUND(SUM(quantity), 0)       AS total_units
FROM dwh.fact_sales
GROUP BY payment_method
ORDER BY total_revenue DESC;

-- Payment method preference by year
SELECT
    d.year,
    f.payment_method,
    COUNT(f.sale_sk)           AS orders,
    ROUND(SUM(f.net_revenue), 2) AS revenue
FROM dwh.fact_sales f
JOIN dwh.dim_date d ON d.date_key = f.date_key
GROUP BY d.year, f.payment_method
ORDER BY d.year, revenue DESC;

-- Payment method by customer income segment
SELECT
    c.income_segment,
    f.payment_method,
    COUNT(f.sale_sk) AS orders
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.income_segment, f.payment_method
ORDER BY c.income_segment, orders DESC;
