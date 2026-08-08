-- ============================================================
-- sql/transformations/create_analytical_views.sql
-- Pre-built views in the analytics schema for Power BI / Excel.
-- These make queries simpler by pre-joining dims to facts.
-- ============================================================

-- ── View 1: Sales with full dimension context ────────────────
CREATE OR REPLACE VIEW analytics.vw_sales_detail AS
SELECT
    f.sale_sk,
    f.transaction_id,
    d.full_date          AS sale_date,
    d.year,
    d.month,
    d.month_name,
    d.year_month,
    d.quarter,
    d.day_name,
    d.is_weekend,
    c.customer_id,
    c.age_group,
    c.gender,
    c.city               AS customer_city,
    c.state              AS customer_state,
    c.region             AS customer_region,
    c.income_segment,
    c.customer_segment,
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    p.brand,
    s.store_id,
    s.store_name,
    s.store_type,
    s.city               AS store_city,
    s.state              AS store_state,
    s.region             AS store_region,
    f.quantity,
    f.unit_price,
    f.discount_pct,
    f.discount_amount,
    f.gross_revenue,
    f.net_revenue,
    f.cost,
    f.gross_profit,
    f.payment_method
FROM dwh.fact_sales f
JOIN dwh.dim_date     d ON d.date_key    = f.date_key
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
JOIN dwh.dim_product  p ON p.product_sk  = f.product_sk
JOIN dwh.dim_store    s ON s.store_sk    = f.store_sk;

-- ── View 2: Monthly KPI summary ──────────────────────────────
CREATE OR REPLACE VIEW analytics.vw_monthly_kpi AS
SELECT
    d.year,
    d.month,
    d.month_name,
    d.year_month,
    COUNT(f.sale_sk)              AS total_orders,
    COUNT(DISTINCT f.customer_sk) AS unique_customers,
    SUM(f.quantity)               AS total_units,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue,
    ROUND(SUM(f.gross_profit), 2) AS total_profit,
    ROUND(AVG(f.net_revenue), 2)  AS avg_order_value,
    ROUND(SUM(f.discount_amount),2) AS total_discount_given
FROM dwh.fact_sales f
JOIN dwh.dim_date d ON d.date_key = f.date_key
GROUP BY d.year, d.month, d.month_name, d.year_month;

-- ── View 3: Category KPI summary ─────────────────────────────
CREATE OR REPLACE VIEW analytics.vw_category_kpi AS
SELECT
    p.category,
    p.sub_category,
    COUNT(f.sale_sk)              AS total_orders,
    SUM(f.quantity)               AS total_units,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue,
    ROUND(SUM(f.gross_profit), 2) AS total_profit,
    ROUND(SUM(f.gross_profit)
          / NULLIF(SUM(f.net_revenue),0) * 100, 2) AS margin_pct,
    ROUND(AVG(f.discount_pct)*100, 2) AS avg_discount_pct
FROM dwh.fact_sales f
JOIN dwh.dim_product p ON p.product_sk = f.product_sk
GROUP BY p.category, p.sub_category;

-- ── View 4: Store performance summary ────────────────────────
CREATE OR REPLACE VIEW analytics.vw_store_kpi AS
SELECT
    s.store_id,
    s.store_name,
    s.store_type,
    s.city,
    s.state,
    s.region,
    s.store_size_sqft,
    COUNT(f.sale_sk)              AS total_orders,
    COUNT(DISTINCT f.customer_sk) AS unique_customers,
    ROUND(SUM(f.net_revenue), 2)  AS total_revenue,
    ROUND(SUM(f.gross_profit), 2) AS total_profit,
    ROUND(AVG(f.net_revenue), 2)  AS avg_order_value,
    ROUND(SUM(f.gross_profit)
          / NULLIF(SUM(f.net_revenue),0) * 100, 2) AS margin_pct
FROM dwh.fact_sales f
JOIN dwh.dim_store s ON s.store_sk = f.store_sk
GROUP BY s.store_id, s.store_name, s.store_type,
         s.city, s.state, s.region, s.store_size_sqft;

-- ── View 5: Customer summary (for RFM / CLV) ─────────────────
CREATE OR REPLACE VIEW analytics.vw_customer_summary AS
SELECT
    c.customer_id,
    c.age_group,
    c.gender,
    c.city,
    c.state,
    c.region,
    c.income_segment,
    c.customer_segment,
    COUNT(f.sale_sk)              AS total_orders,
    SUM(f.quantity)               AS total_units,
    ROUND(SUM(f.net_revenue), 2)  AS total_spent,
    ROUND(AVG(f.net_revenue), 2)  AS avg_order_value,
    MIN(d.full_date)              AS first_purchase_date,
    MAX(d.full_date)              AS last_purchase_date
FROM dwh.fact_sales f
JOIN dwh.dim_customer c ON c.customer_sk = f.customer_sk
JOIN dwh.dim_date     d ON d.date_key    = f.date_key
GROUP BY c.customer_id, c.age_group, c.gender,
         c.city, c.state, c.region, c.income_segment, c.customer_segment;
