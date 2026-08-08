-- ============================================================
-- sql/customer_analysis/03_repeat_vs_new.sql
-- Repeat vs one-time customer comparison.
-- Basic: subquery, GROUP BY, CASE
-- ============================================================

-- Classify customers as repeat or one-time
SELECT
    purchase_type,
    COUNT(customer_sk)               AS customer_count,
    ROUND(SUM(total_spent), 2)       AS total_revenue,
    ROUND(AVG(total_spent), 2)       AS avg_spend_per_customer,
    ROUND(AVG(order_count), 2)       AS avg_orders_per_customer
FROM (
    SELECT
        f.customer_sk,
        COUNT(f.sale_sk)             AS order_count,
        ROUND(SUM(f.net_revenue), 2) AS total_spent,
        CASE
            WHEN COUNT(f.sale_sk) = 1 THEN 'One-Time'
            ELSE 'Repeat'
        END                          AS purchase_type
    FROM dwh.fact_sales f
    GROUP BY f.customer_sk
) AS customer_summary
GROUP BY purchase_type
ORDER BY customer_count DESC;
