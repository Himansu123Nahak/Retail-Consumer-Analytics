-- ============================================================
-- sql/staging/load_staging_tables.sql
-- Loads clean CSVs from data/processed/ into staging schema.
-- Run with psql \copy or Python psycopg2 COPY FROM.
-- ============================================================

-- Drop and recreate staging tables
DROP TABLE IF EXISTS staging.stg_customers;
DROP TABLE IF EXISTS staging.stg_products;
DROP TABLE IF EXISTS staging.stg_stores;
DROP TABLE IF EXISTS staging.stg_transactions;
DROP TABLE IF EXISTS staging.stg_inventory;
DROP TABLE IF EXISTS staging.stg_marketing;

CREATE TABLE staging.stg_customers (
    customer_id      TEXT, age_group TEXT, gender TEXT,
    city TEXT, state TEXT, income_segment TEXT,
    signup_date TEXT, customer_segment TEXT
);

CREATE TABLE staging.stg_products (
    product_id TEXT, product_name TEXT, category TEXT, sub_category TEXT,
    brand TEXT, cost_price TEXT, selling_price TEXT, margin_pct TEXT, supplier TEXT
);

CREATE TABLE staging.stg_stores (
    store_id TEXT, store_name TEXT, store_type TEXT,
    city TEXT, state TEXT, region TEXT,
    store_size_sqft TEXT, opening_date TEXT, is_active TEXT
);

CREATE TABLE staging.stg_transactions (
    transaction_id TEXT, customer_id TEXT, store_id TEXT, product_id TEXT,
    transaction_date TEXT, quantity TEXT, unit_price TEXT,
    discount TEXT, payment_method TEXT, total_amount TEXT
);

CREATE TABLE staging.stg_inventory (
    snapshot_date TEXT, store_id TEXT, product_id TEXT,
    opening_stock TEXT, purchase_qty TEXT, sales_qty TEXT,
    closing_stock TEXT, stockout_flag TEXT
);

CREATE TABLE staging.stg_marketing (
    campaign_interaction_id TEXT, customer_id TEXT, campaign_name TEXT,
    channel TEXT, campaign_date TEXT, responded TEXT, spend TEXT
);

-- Load via psql \copy (adjust paths as needed):
-- \copy staging.stg_customers    FROM 'data/processed/customers_clean.csv'    CSV HEADER;
-- \copy staging.stg_products     FROM 'data/processed/products_clean.csv'     CSV HEADER;
-- \copy staging.stg_stores       FROM 'data/processed/stores.csv'             CSV HEADER;
-- \copy staging.stg_transactions FROM 'data/processed/transactions_clean.csv' CSV HEADER;
-- \copy staging.stg_inventory    FROM 'data/processed/inventory.csv'          CSV HEADER;
-- \copy staging.stg_marketing    FROM 'data/processed/marketing_campaigns.csv'CSV HEADER;
