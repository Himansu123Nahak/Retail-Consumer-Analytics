-- ============================================================
-- sql/sales_analysis/06_store_performance.sql
-- Revenue and profit by store.
-- Basic: JOIN, GROUP BY, ORDER BY
-- ============================================================

SELECT
    s.store_id,
    s.store_name,
    s.store_type,
    s.city,
    s.state,
    s.region,
    s.store_size_sqft,
    COUNT(f.sale_sk)             AS total_orders,
    SUM(f.quantity)              AS total_units,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue,
    ROUND(SUM(f.gross_profit),2) AS total_profit,
    ROUND(AVG(f.net_revenue), 2) AS avg_order_value,
    ROUND(SUM(f.gross_profit)
          / NULLIF(SUM(f.net_revenue),0) * 100, 2) AS profit_margin_pct
FROM dwh.fact_sales f
JOIN dwh.dim_store s ON s.store_sk = f.store_sk
GROUP BY
    s.store_id, s.store_name, s.store_type,
    s.city, s.state, s.region, s.store_size_sqft
ORDER BY total_revenue DESC;
