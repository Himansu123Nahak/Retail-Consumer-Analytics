-- ============================================================
-- sql/sales_analysis/01_total_revenue_profit.sql
-- Overall business performance summary.
-- Basic: SELECT, SUM, COUNT, GROUP BY, ORDER BY
-- ============================================================

-- Total revenue, profit and orders overall
SELECT
    COUNT(sale_sk)                   AS total_orders,
    ROUND(SUM(net_revenue), 2)       AS total_revenue,
    ROUND(SUM(gross_profit), 2)      AS total_profit,
    ROUND(SUM(gross_profit) / NULLIF(SUM(net_revenue), 0) * 100, 2)
                                     AS profit_margin_pct,
    ROUND(SUM(net_revenue) / NULLIF(COUNT(sale_sk), 0), 2)
                                     AS avg_order_value
FROM dwh.fact_sales;
