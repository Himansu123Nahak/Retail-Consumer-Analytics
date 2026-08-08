-- ============================================================
-- sql/product_analysis/01_product_performance.sql
-- Full product performance — revenue, units, margin, rank.
-- Basic: JOIN, GROUP BY, ORDER BY, CASE
-- ============================================================

-- Top 20 products by revenue
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    p.brand,
    COUNT(f.sale_sk)              AS total_orders,
    SUM(f.quantity)               AS total_units,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue,
    ROUND(SUM(f.gross_profit), 2) AS total_profit,
    ROUND(
        SUM(f.gross_profit) / NULLIF(SUM(f.net_revenue), 0) * 100, 2
    )                             AS margin_pct,
    ROUND(AVG(f.discount_pct) * 100, 2) AS avg_discount_pct
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.product_id, p.product_name, p.category,
         p.sub_category, p.brand
ORDER BY total_revenue DESC
LIMIT 20;

-- Bottom 10 products by revenue (potential candidates to discontinue)
SELECT
    p.product_name,
    p.category,
    COUNT(f.sale_sk)             AS total_orders,
    SUM(f.quantity)              AS total_units,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.product_name, p.category
ORDER BY total_revenue ASC
LIMIT 10;

-- Revenue by category and sub-category
SELECT
    p.category,
    p.sub_category,
    COUNT(f.sale_sk)              AS orders,
    SUM(f.quantity)               AS units,
    ROUND(SUM(f.net_revenue), 2)  AS revenue,
    ROUND(SUM(f.gross_profit), 2) AS profit,
    ROUND(
        SUM(f.gross_profit) / NULLIF(SUM(f.net_revenue), 0) * 100, 2
    )                             AS margin_pct
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.category, p.sub_category
ORDER BY p.category, revenue DESC;

-- High revenue, low margin products (pricing opportunity)
SELECT
    p.product_name,
    p.category,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    ROUND(
        SUM(f.gross_profit) / NULLIF(SUM(f.net_revenue), 0) * 100, 2
    )                            AS margin_pct,
    ROUND(AVG(f.discount_pct) * 100, 2) AS avg_discount_pct
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.product_name, p.category
HAVING SUM(f.net_revenue) > 50000
   AND SUM(f.gross_profit) / NULLIF(SUM(f.net_revenue), 0) < 0.20
ORDER BY revenue DESC
LIMIT 15;
