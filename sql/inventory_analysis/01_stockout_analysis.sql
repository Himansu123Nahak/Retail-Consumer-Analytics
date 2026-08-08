-- ============================================================
-- sql/inventory_analysis/01_stockout_analysis.sql
-- Stockout rate and slow-moving products.
-- Basic: JOIN, GROUP BY, HAVING, ORDER BY
-- ============================================================

-- Stockout rate by product
SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(i.inventory_sk)                 AS total_snapshots,
    SUM(CASE WHEN i.stockout_flag THEN 1 ELSE 0 END)
                                          AS stockout_days,
    ROUND(
        SUM(CASE WHEN i.stockout_flag THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(i.inventory_sk), 0) * 100, 2
    )                                     AS stockout_rate_pct,
    ROUND(AVG(i.closing_stock), 0)        AS avg_closing_stock
FROM dwh.fact_inventory i
JOIN dwh.dim_product p ON p.product_sk = i.product_sk
GROUP BY p.product_id, p.product_name, p.category
ORDER BY stockout_rate_pct DESC
LIMIT 20;

-- Slow-moving products (very low sales qty vs high stock)
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(AVG(i.opening_stock), 0)  AS avg_opening_stock,
    ROUND(AVG(i.sales_qty), 2)      AS avg_daily_sales,
    ROUND(AVG(i.closing_stock), 0)  AS avg_closing_stock
FROM dwh.fact_inventory i
JOIN dwh.dim_product p ON p.product_sk = i.product_sk
GROUP BY p.product_id, p.product_name, p.category
HAVING AVG(i.sales_qty) < 2 AND AVG(i.closing_stock) > 100
ORDER BY avg_closing_stock DESC
LIMIT 20;
