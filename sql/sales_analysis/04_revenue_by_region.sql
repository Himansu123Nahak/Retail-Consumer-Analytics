-- ============================================================
-- sql/sales_analysis/04_revenue_by_region.sql
-- Revenue performance by region and state.
-- Basic: JOIN, GROUP BY, ORDER BY
-- ============================================================

-- By region
SELECT
    s.region,
    COUNT(f.sale_sk)             AS total_orders,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue,
    ROUND(SUM(f.gross_profit),2) AS total_profit,
    ROUND(AVG(f.net_revenue), 2) AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_store s ON s.store_sk = f.store_sk
GROUP BY s.region
ORDER BY total_revenue DESC;

-- By state
SELECT
    s.state,
    s.region,
    COUNT(f.sale_sk)             AS total_orders,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue,
    ROUND(SUM(f.gross_profit),2) AS total_profit
FROM dwh.fact_sales f
JOIN dwh.dim_store s ON s.store_sk = f.store_sk
GROUP BY s.state, s.region
ORDER BY total_revenue DESC;
