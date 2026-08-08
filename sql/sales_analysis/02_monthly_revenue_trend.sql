-- ============================================================
-- sql/sales_analysis/02_monthly_revenue_trend.sql
-- Revenue and orders by year and month.
-- Basic: JOIN, GROUP BY, ORDER BY
-- ============================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    d.year_month,
    COUNT(f.sale_sk)             AS total_orders,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue,
    ROUND(SUM(f.gross_profit),2) AS total_profit,
    ROUND(AVG(f.net_revenue), 2) AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_date d ON d.date_key = f.date_key
GROUP BY d.year, d.month, d.month_name, d.year_month
ORDER BY d.year, d.month;
