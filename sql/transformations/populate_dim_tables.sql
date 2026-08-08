-- ============================================================
-- sql/transformations/populate_dim_tables.sql
-- Moves data from staging → dwh dimension tables.
-- ============================================================

-- ── dim_customer ─────────────────────────────────────────────
INSERT INTO dwh.dim_customer (
    customer_id, age_group, gender, city, state, region,
    income_segment, signup_date, signup_date_key, customer_segment
)
SELECT
    s.customer_id,
    s.age_group,
    s.gender,
    s.city,
    s.state,
    -- Derive region from state
    CASE
        WHEN s.state IN ('Delhi','Punjab','Rajasthan','Uttar Pradesh','Haryana','Himachal Pradesh')
            THEN 'North'
        WHEN s.state IN ('Karnataka','Tamil Nadu','Telangana','Kerala','Andhra Pradesh')
            THEN 'South'
        WHEN s.state IN ('Maharashtra','Gujarat','Goa')
            THEN 'West'
        WHEN s.state IN ('West Bengal','Odisha','Bihar','Assam','Jharkhand')
            THEN 'East'
        ELSE 'Central'
    END AS region,
    s.income_segment,
    s.signup_date::DATE,
    TO_CHAR(s.signup_date::DATE, 'YYYYMMDD')::INTEGER,
    COALESCE(s.customer_segment, 'Unassigned')
FROM staging.stg_customers s
ON CONFLICT (customer_id) DO NOTHING;

-- ── dim_product ──────────────────────────────────────────────
INSERT INTO dwh.dim_product (
    product_id, product_name, category, sub_category,
    brand, cost_price, selling_price, margin_pct, supplier
)
SELECT
    s.product_id,
    s.product_name,
    s.category,
    s.sub_category,
    s.brand,
    s.cost_price::NUMERIC,
    s.selling_price::NUMERIC,
    s.margin_pct::NUMERIC,
    s.supplier
FROM staging.stg_products s
ON CONFLICT (product_id) DO NOTHING;

-- ── dim_store ────────────────────────────────────────────────
INSERT INTO dwh.dim_store (
    store_id, store_name, store_type, city, state, region,
    store_size_sqft, opening_date
)
SELECT
    s.store_id,
    s.store_name,
    s.store_type,
    s.city,
    s.state,
    s.region,
    NULLIF(s.store_size_sqft, '')::INTEGER,
    NULLIF(s.opening_date, '')::DATE
FROM staging.stg_stores s
ON CONFLICT (store_id) DO NOTHING;

-- ── dim_campaign ─────────────────────────────────────────────
INSERT INTO dwh.dim_campaign (campaign_name, channel)
SELECT DISTINCT campaign_name, channel
FROM staging.stg_marketing
ON CONFLICT (campaign_name, channel) DO NOTHING;
