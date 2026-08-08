-- ============================================================
-- sql/sales_analysis/07_discount_analysis.sql
-- How discounts affect revenue and profit.
-- Basic: GROUP BY with CASE buckets, HAVING
-- ============================================================

-- Revenue and profit by discount bucket
SELECT
    CASE
        WHEN discount_pct = 0          THEN 'No Discount'
        WHEN discount_pct <= 0.10      THEN '1-10%'
        WHEN discount_pct <= 0.20      THEN '11-20%'
        WHEN discount_pct <= 0.30      THEN '21-30%'
        ELSE '31%+'
    END                              AS discount_band,
    COUNT(sale_sk)                   AS total_orders,
    SUM(quantity)                    AS total_units,
    ROUND(SUM(net_revenue),  2)      AS total_revenue,
    ROUND(SUM(gross_profit), 2)      AS total_profit,
    ROUND(AVG(net_revenue),  2)      AS avg_order_value,
    ROUND(SUM(gross_profit)
          / NULLIF(SUM(net_revenue),0) * 100, 2) AS profit_margin_pct
FROM dwh.fact_sales
GROUP BY discount_band
ORDER BY total_revenue DESC;

-- Average discount by category
SELECT
    p.category,
    ROUND(AVG(f.discount_pct) * 100, 2) AS avg_discount_pct,
    ROUND(SUM(f.net_revenue), 2)         AS total_revenue,
    ROUND(SUM(f.gross_profit), 2)        AS total_profit
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.category
ORDER BY avg_discount_pct DESC;
