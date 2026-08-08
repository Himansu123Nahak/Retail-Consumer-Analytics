-- ============================================================
-- sql/marketing_analysis/02_channel_roi.sql
-- Marketing channel ROI and campaign effectiveness analysis.
-- Basic SQL: GROUP BY, CASE, HAVING, subquery
-- ============================================================

-- Channel-level performance summary
SELECT
    channel,
    COUNT(marketing_sk)                           AS total_contacts,
    SUM(responded)                                AS total_responses,
    ROUND(SUM(responded) * 100.0
          / COUNT(marketing_sk), 2)               AS response_rate_pct,
    ROUND(SUM(spend), 2)                          AS total_spend,
    ROUND(SUM(spend) / NULLIF(SUM(responded), 0), 2) AS cost_per_response
FROM dwh.fact_marketing
GROUP BY channel
ORDER BY response_rate_pct DESC;

-- Campaign performance ranking
SELECT
    c.campaign_name,
    c.channel,
    COUNT(f.marketing_sk)                             AS total_contacts,
    SUM(f.responded)                                  AS total_responses,
    ROUND(SUM(f.responded) * 100.0
          / COUNT(f.marketing_sk), 2)                 AS response_rate_pct,
    ROUND(SUM(f.spend), 2)                            AS total_spend,
    ROUND(SUM(f.spend) / NULLIF(SUM(f.responded), 0), 2) AS cost_per_response
FROM dwh.fact_marketing f
JOIN dwh.dim_campaign   c ON c.campaign_sk = f.campaign_sk
GROUP BY c.campaign_name, c.channel
ORDER BY response_rate_pct DESC;

-- Best channel by customer segment
SELECT
    cu.income_segment,
    f.channel,
    COUNT(f.marketing_sk)   AS contacts,
    SUM(f.responded)        AS responses,
    ROUND(SUM(f.responded) * 100.0 / COUNT(f.marketing_sk), 2) AS response_rate_pct
FROM dwh.fact_marketing  f
JOIN dwh.dim_customer    cu ON cu.customer_sk = f.customer_sk
GROUP BY cu.income_segment, f.channel
ORDER BY cu.income_segment, response_rate_pct DESC;
