-- ============================================================
-- sql/inventory_analysis/02_stock_turnover.sql
-- Stock turnover analysis — how fast is inventory moving?
-- Identifies fast vs slow moving products.
-- Basic SQL: JOIN, GROUP BY, CASE, ORDER BY
-- ============================================================

-- Average stock levels and sales velocity by product
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(AVG(i.opening_stock), 1)   AS avg_opening_stock,
    ROUND(AVG(i.closing_stock), 1)   AS avg_closing_stock,
    ROUND(AVG(i.sales_qty), 2)       AS avg_daily_sales,
    ROUND(AVG(i.purchase_qty), 1)    AS avg_daily_purchase,
    CASE
        WHEN AVG(i.sales_qty) >= 3   THEN 'Fast Moving'
        WHEN AVG(i.sales_qty) >= 1   THEN 'Medium Moving'
        ELSE 'Slow Moving'
    END                              AS velocity_category
FROM dwh.fact_inventory i
JOIN dwh.dim_product    p ON p.product_sk = i.product_sk
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
ORDER BY avg_daily_sales DESC;

-- Slow-moving products (high stock, low sales)
SELECT
    p.product_name,
    p.category,
    ROUND(AVG(i.closing_stock), 1)  AS avg_closing_stock,
    ROUND(AVG(i.sales_qty), 2)      AS avg_daily_sales,
    COUNT(i.inventory_sk)           AS snapshot_days
FROM dwh.fact_inventory i
JOIN dwh.dim_product    p ON p.product_sk = i.product_sk
GROUP BY p.product_name, p.category
HAVING AVG(i.closing_stock) > 300
   AND AVG(i.sales_qty) < 1
ORDER BY avg_closing_stock DESC
LIMIT 20;

-- Stock summary by category
SELECT
    p.category,
    ROUND(AVG(i.opening_stock), 1)  AS avg_opening,
    ROUND(AVG(i.closing_stock), 1)  AS avg_closing,
    ROUND(AVG(i.purchase_qty), 1)   AS avg_daily_purchase,
    ROUND(AVG(i.sales_qty), 2)      AS avg_daily_sales,
    SUM(CASE WHEN i.stockout_flag = 1 THEN 1 ELSE 0 END) AS stockout_count
FROM dwh.fact_inventory i
JOIN dwh.dim_product    p ON p.product_sk = i.product_sk
GROUP BY p.category
ORDER BY avg_daily_sales DESC;
