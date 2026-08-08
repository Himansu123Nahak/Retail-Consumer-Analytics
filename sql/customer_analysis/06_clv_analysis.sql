-- ============================================================
-- sql/customer_analysis/06_clv_analysis.sql
-- Customer Lifetime Value (CLV) analysis using SQL.
-- Segments customers into value tiers based on total spend.
-- Basic SQL: GROUP BY, CASE, ORDER BY
-- ============================================================

-- Customer-level lifetime summary
SELECT
    c.customer_id,
    c.customer_name,
    c.age_group,
    c.gender,
    c.income_segment,
    c.region,
    COUNT(f.sale_sk)             AS total_orders,
    SUM(f.quantity)              AS total_units,
    ROUND(SUM(f.net_revenue), 2) AS total_revenue,
    ROUND(AVG(f.net_revenue), 2) AS avg_order_value,
    MIN(d.full_date)             AS first_purchase,
    MAX(d.full_date)             AS last_purchase,
    CASE
        WHEN SUM(f.net_revenue) >= 500000 THEN 'Platinum'
        WHEN SUM(f.net_revenue) >= 200000 THEN 'Gold'
        WHEN SUM(f.net_revenue) >= 75000  THEN 'Silver'
        ELSE 'Bronze'
    END AS clv_tier
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
JOIN dwh.dim_date     d ON d.date_key    = f.date_key
GROUP BY c.customer_id, c.customer_name, c.age_group,
         c.gender, c.income_segment, c.region
ORDER BY total_revenue DESC;

-- CLV tier summary
SELECT
    clv_tier,
    COUNT(*)                      AS customers,
    ROUND(AVG(total_revenue), 2)  AS avg_clv,
    ROUND(SUM(total_revenue), 2)  AS tier_revenue
FROM (
    SELECT
        c.customer_id,
        SUM(f.net_revenue) AS total_revenue,
        CASE
            WHEN SUM(f.net_revenue) >= 500000 THEN 'Platinum'
            WHEN SUM(f.net_revenue) >= 200000 THEN 'Gold'
            WHEN SUM(f.net_revenue) >= 75000  THEN 'Silver'
            ELSE 'Bronze'
        END AS clv_tier
    FROM dwh.fact_sales f
    JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
    GROUP BY c.customer_id
) sub
GROUP BY clv_tier
ORDER BY avg_clv DESC;
