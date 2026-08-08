-- ============================================================
-- sql/sales_analysis/05_top_products.sql
-- Top 10 and bottom 10 products by revenue.
-- Basic: JOIN, GROUP BY, ORDER BY, LIMIT
-- ============================================================

-- Top 10 products by revenue
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    COUNT(f.sale_sk)             AS total_orders,
    SUM(f.quantity)              AS total_units,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue,
    ROUND(SUM(f.gross_profit),2) AS total_profit
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.product_id, p.product_name, p.category, p.brand
ORDER BY total_revenue DESC
LIMIT 10;

-- Bottom 10 products by revenue
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    COUNT(f.sale_sk)             AS total_orders,
    SUM(f.quantity)              AS total_units,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue,
    ROUND(SUM(f.gross_profit),2) AS total_profit
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.product_id, p.product_name, p.category, p.brand
ORDER BY total_revenue ASC
LIMIT 10;
