-- ============================================================
-- sql/staging/staging_validations.sql
-- Row count checks after loading staging tables.
-- Run after load_staging_tables.sql + CSV copy commands.
-- ============================================================

-- Row counts per staging table
SELECT 'stg_customers'    AS table_name, COUNT(*) AS row_count FROM staging.stg_customers
UNION ALL
SELECT 'stg_products',    COUNT(*) FROM staging.stg_products
UNION ALL
SELECT 'stg_stores',      COUNT(*) FROM staging.stg_stores
UNION ALL
SELECT 'stg_transactions',COUNT(*) FROM staging.stg_transactions
UNION ALL
SELECT 'stg_inventory',   COUNT(*) FROM staging.stg_inventory
UNION ALL
SELECT 'stg_marketing',   COUNT(*) FROM staging.stg_marketing
ORDER BY table_name;

-- Check: any transaction customer_ids not in customers?
SELECT COUNT(*) AS orphan_customer_transactions
FROM staging.stg_transactions t
WHERE NOT EXISTS (
    SELECT 1 FROM staging.stg_customers c
    WHERE c.customer_id = t.customer_id
);

-- Check: any transaction product_ids not in products?
SELECT COUNT(*) AS orphan_product_transactions
FROM staging.stg_transactions t
WHERE NOT EXISTS (
    SELECT 1 FROM staging.stg_products p
    WHERE p.product_id = t.product_id
);

-- Check: any transaction store_ids not in stores?
SELECT COUNT(*) AS orphan_store_transactions
FROM staging.stg_transactions t
WHERE NOT EXISTS (
    SELECT 1 FROM staging.stg_stores s
    WHERE s.store_id = t.store_id
);
