-- ============================================================
-- sql/marketing_analysis/01_campaign_performance.sql
-- Campaign response rates and spend by channel.
-- Basic: JOIN, GROUP BY, ORDER BY
-- ============================================================

-- Overall campaign performance by channel
SELECT
    c.channel,
    COUNT(f.marketing_sk)                   AS total_contacts,
    SUM(CASE WHEN f.responded THEN 1 ELSE 0 END)
                                            AS total_responses,
    ROUND(
        SUM(CASE WHEN f.responded THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(f.marketing_sk), 0) * 100, 2
    )                                       AS response_rate_pct,
    ROUND(SUM(f.spend), 2)                  AS total_spend,
    ROUND(AVG(f.spend), 2)                  AS cost_per_contact
FROM dwh.fact_marketing f
JOIN dwh.dim_campaign c ON c.campaign_sk = f.campaign_sk
GROUP BY c.channel
ORDER BY response_rate_pct DESC;

-- Campaign performance by campaign name
SELECT
    c.campaign_name,
    COUNT(f.marketing_sk)                   AS total_contacts,
    SUM(CASE WHEN f.responded THEN 1 ELSE 0 END)
                                            AS total_responses,
    ROUND(
        SUM(CASE WHEN f.responded THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(f.marketing_sk), 0) * 100, 2
    )                                       AS response_rate_pct,
    ROUND(SUM(f.spend), 2)                  AS total_spend
FROM dwh.fact_marketing f
JOIN dwh.dim_campaign c ON c.campaign_sk = f.campaign_sk
GROUP BY c.campaign_name
ORDER BY total_responses DESC;
