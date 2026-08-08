-- ============================================================
-- sql/customer_analysis/04_top_customers.sql
-- Top 10 customers by revenue and orders.
-- Basic: JOIN, GROUP BY, ORDER BY, LIMIT
-- ============================================================

-- Top 10 customers by total spend
SELECT
    c.customer_id,
    c.age_group,
    c.gender,
    c.city,
    c.region,
    c.income_segment,
    COUNT(f.sale_sk)             AS total_orders,
    ROUND(SUM(f.net_revenue), 2) AS total_spent,
    ROUND(AVG(f.net_revenue), 2) AS avg_order_value
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY
    c.customer_id, c.age_group, c.gender,
    c.city, c.region, c.income_segment
ORDER BY total_spent DESC
LIMIT 10;

-- Revenue contribution: top 20% of customers vs rest
SELECT
    customer_tier,
    COUNT(*)                         AS customer_count,
    ROUND(SUM(total_spent), 2)       AS total_revenue,
    ROUND(AVG(total_spent), 2)       AS avg_spend
FROM (
    SELECT
        f.customer_sk,
        SUM(f.net_revenue)           AS total_spent,
        CASE
            WHEN SUM(f.net_revenue) >= (
                SELECT PERCENTILE_CONT(0.80) WITHIN GROUP (ORDER BY sub.rev)
                FROM (SELECT SUM(f2.net_revenue) AS rev
                      FROM dwh.fact_sales f2 GROUP BY f2.customer_sk) sub
            ) THEN 'Top 20%'
            ELSE 'Bottom 80%'
        END                          AS customer_tier
    FROM dwh.fact_sales f
    GROUP BY f.customer_sk
) t
GROUP BY customer_tier;
