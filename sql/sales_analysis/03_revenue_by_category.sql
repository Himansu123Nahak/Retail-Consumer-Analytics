-- ============================================================
-- sql/sales_analysis/03_revenue_by_category.sql
-- Revenue, profit and orders broken down by product category.
-- Basic: JOIN, GROUP BY, ORDER BY
-- ============================================================

SELECT
    p.category,
    COUNT(f.sale_sk)                        AS total_orders,
    SUM(f.quantity)                         AS total_units_sold,
    ROUND(SUM(f.net_revenue), 2)            AS total_revenue,
    ROUND(SUM(f.gross_profit), 2)           AS total_profit,
    ROUND(SUM(f.gross_profit)
          / NULLIF(SUM(f.net_revenue),0) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.net_revenue), 2)            AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.category
ORDER BY total_revenue DESC;
