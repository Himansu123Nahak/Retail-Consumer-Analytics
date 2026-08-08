-- ============================================================
-- sql/transformations/populate_fact_tables.sql
-- Moves data from staging into dwh fact tables.
-- Basic JOINs to resolve surrogate keys.
-- ============================================================

-- ── fact_sales ───────────────────────────────────────────────
INSERT INTO dwh.fact_sales (
    transaction_id,
    date_key,
    customer_sk,
    product_sk,
    store_sk,
    quantity,
    unit_price,
    discount_pct,
    discount_amount,
    gross_revenue,
    net_revenue,
    cost,
    gross_profit,
    payment_method
)
SELECT
    t.transaction_id,
    TO_CHAR(t.transaction_date::DATE, 'YYYYMMDD')::INTEGER   AS date_key,
    c.customer_sk,
    p.product_sk,
    s.store_sk,
    t.quantity::INTEGER,
    t.unit_price::NUMERIC,
    t.discount::NUMERIC                                        AS discount_pct,
    ROUND(t.unit_price::NUMERIC * t.quantity::INTEGER * t.discount::NUMERIC, 2)
                                                               AS discount_amount,
    ROUND(t.unit_price::NUMERIC * t.quantity::INTEGER, 2)      AS gross_revenue,
    t.total_amount::NUMERIC                                    AS net_revenue,
    ROUND(p.cost_price * t.quantity::INTEGER, 2)               AS cost,
    ROUND(t.total_amount::NUMERIC - p.cost_price * t.quantity::INTEGER, 2)
                                                               AS gross_profit,
    t.payment_method
FROM staging.stg_transactions t
JOIN dwh.dim_customer c ON c.customer_id = t.customer_id
JOIN dwh.dim_product  p ON p.product_id  = t.product_id
JOIN dwh.dim_store    s ON s.store_id    = t.store_id
ON CONFLICT (transaction_id) DO NOTHING;

-- ── fact_inventory ───────────────────────────────────────────
INSERT INTO dwh.fact_inventory (
    date_key, store_sk, product_sk,
    opening_stock, purchase_qty, sales_qty, closing_stock,
    stockout_flag, inventory_value
)
SELECT
    TO_CHAR(i.snapshot_date::DATE, 'YYYYMMDD')::INTEGER AS date_key,
    s.store_sk,
    p.product_sk,
    i.opening_stock::INTEGER,
    i.purchase_qty::INTEGER,
    i.sales_qty::INTEGER,
    i.closing_stock::INTEGER,
    i.stockout_flag::INTEGER::BOOLEAN,
    ROUND(i.closing_stock::INTEGER * p.cost_price, 2)   AS inventory_value
FROM staging.stg_inventory i
JOIN dwh.dim_store   s ON s.store_id   = i.store_id
JOIN dwh.dim_product p ON p.product_id = i.product_id;

-- ── fact_marketing ───────────────────────────────────────────
INSERT INTO dwh.fact_marketing (
    campaign_interaction_id, date_key, customer_sk, campaign_sk,
    responded, spend
)
SELECT
    m.campaign_interaction_id,
    TO_CHAR(m.campaign_date::DATE, 'YYYYMMDD')::INTEGER AS date_key,
    c.customer_sk,
    cam.campaign_sk,
    m.responded::INTEGER::BOOLEAN,
    m.spend::NUMERIC
FROM staging.stg_marketing m
JOIN dwh.dim_customer c   ON c.customer_id   = m.customer_id
JOIN dwh.dim_campaign cam ON cam.campaign_name = m.campaign_name
                         AND cam.channel       = m.channel
ON CONFLICT (campaign_interaction_id) DO NOTHING;
