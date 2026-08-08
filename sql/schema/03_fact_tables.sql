-- ============================================================
-- sql/schema/03_fact_tables.sql
-- Fact tables: fact_sales, fact_inventory, fact_marketing
-- ============================================================

-- ── FACT: SALES ──────────────────────────────────────────────
DROP TABLE IF EXISTS dwh.fact_sales;

CREATE TABLE dwh.fact_sales (
    sale_sk            BIGSERIAL     NOT NULL,
    transaction_id     VARCHAR(15)   NOT NULL,
    date_key           INTEGER       NOT NULL,   -- FK dim_date
    customer_sk        INTEGER       NOT NULL,   -- FK dim_customer
    product_sk         INTEGER       NOT NULL,   -- FK dim_product
    store_sk           INTEGER       NOT NULL,   -- FK dim_store
    -- Measures
    quantity           INTEGER       NOT NULL,
    unit_price         NUMERIC(12,2) NOT NULL,
    discount_pct       NUMERIC(5,4)  NOT NULL,   -- e.g. 0.15 = 15%
    discount_amount    NUMERIC(12,2) NOT NULL,
    gross_revenue      NUMERIC(14,2) NOT NULL,   -- qty × unit_price
    net_revenue        NUMERIC(14,2) NOT NULL,   -- gross - discount
    cost               NUMERIC(14,2) NOT NULL,   -- qty × cost_price (from dim_product)
    gross_profit       NUMERIC(14,2) NOT NULL,   -- net_revenue - cost
    payment_method     VARCHAR(20),
    CONSTRAINT pk_fact_sales PRIMARY KEY (sale_sk),
    CONSTRAINT uq_fact_sales_txn UNIQUE (transaction_id),
    CONSTRAINT fk_fact_sales_date     FOREIGN KEY (date_key)    REFERENCES dwh.dim_date    (date_key),
    CONSTRAINT fk_fact_sales_customer FOREIGN KEY (customer_sk) REFERENCES dwh.dim_customer(customer_sk),
    CONSTRAINT fk_fact_sales_product  FOREIGN KEY (product_sk)  REFERENCES dwh.dim_product (product_sk),
    CONSTRAINT fk_fact_sales_store    FOREIGN KEY (store_sk)    REFERENCES dwh.dim_store   (store_sk)
);

-- Composite indexes for common analytical access patterns
CREATE INDEX idx_fact_sales_date        ON dwh.fact_sales (date_key);
CREATE INDEX idx_fact_sales_customer    ON dwh.fact_sales (customer_sk);
CREATE INDEX idx_fact_sales_product     ON dwh.fact_sales (product_sk);
CREATE INDEX idx_fact_sales_store       ON dwh.fact_sales (store_sk);
CREATE INDEX idx_fact_sales_date_store  ON dwh.fact_sales (date_key, store_sk);
CREATE INDEX idx_fact_sales_date_prod   ON dwh.fact_sales (date_key, product_sk);

COMMENT ON TABLE dwh.fact_sales IS 'Line-item sales fact table. All monetary amounts in INR (₹).';

-- ── FACT: INVENTORY ───────────────────────────────────────────
DROP TABLE IF EXISTS dwh.fact_inventory;

CREATE TABLE dwh.fact_inventory (
    inventory_sk     BIGSERIAL     NOT NULL,
    date_key         INTEGER       NOT NULL,   -- FK dim_date
    store_sk         INTEGER       NOT NULL,   -- FK dim_store
    product_sk       INTEGER       NOT NULL,   -- FK dim_product
    opening_stock    INTEGER       NOT NULL,
    purchase_qty     INTEGER       NOT NULL,
    sales_qty        INTEGER       NOT NULL,
    closing_stock    INTEGER       NOT NULL,
    stockout_flag    BOOLEAN       NOT NULL DEFAULT FALSE,
    inventory_value  NUMERIC(14,2),            -- closing_stock × cost_price
    CONSTRAINT pk_fact_inventory PRIMARY KEY (inventory_sk),
    CONSTRAINT fk_fact_inv_date    FOREIGN KEY (date_key)   REFERENCES dwh.dim_date   (date_key),
    CONSTRAINT fk_fact_inv_store   FOREIGN KEY (store_sk)   REFERENCES dwh.dim_store  (store_sk),
    CONSTRAINT fk_fact_inv_product FOREIGN KEY (product_sk) REFERENCES dwh.dim_product(product_sk)
);

CREATE INDEX idx_fact_inv_date       ON dwh.fact_inventory (date_key);
CREATE INDEX idx_fact_inv_store      ON dwh.fact_inventory (store_sk);
CREATE INDEX idx_fact_inv_product    ON dwh.fact_inventory (product_sk);
CREATE INDEX idx_fact_inv_stockout   ON dwh.fact_inventory (stockout_flag) WHERE stockout_flag = TRUE;

COMMENT ON TABLE dwh.fact_inventory IS 'Daily inventory snapshot per store × product.';

-- ── FACT: MARKETING ───────────────────────────────────────────
DROP TABLE IF EXISTS dwh.fact_marketing;

CREATE TABLE dwh.fact_marketing (
    marketing_sk               BIGSERIAL     NOT NULL,
    campaign_interaction_id    VARCHAR(15)   NOT NULL,
    date_key                   INTEGER       NOT NULL,   -- FK dim_date
    customer_sk                INTEGER       NOT NULL,   -- FK dim_customer
    campaign_sk                INTEGER       NOT NULL,   -- FK dim_campaign
    responded                  BOOLEAN       NOT NULL DEFAULT FALSE,
    spend                      NUMERIC(10,2) NOT NULL,
    CONSTRAINT pk_fact_marketing PRIMARY KEY (marketing_sk),
    CONSTRAINT uq_fact_marketing_id UNIQUE (campaign_interaction_id),
    CONSTRAINT fk_fact_mkt_date     FOREIGN KEY (date_key)    REFERENCES dwh.dim_date    (date_key),
    CONSTRAINT fk_fact_mkt_customer FOREIGN KEY (customer_sk) REFERENCES dwh.dim_customer(customer_sk),
    CONSTRAINT fk_fact_mkt_campaign FOREIGN KEY (campaign_sk) REFERENCES dwh.dim_campaign(campaign_sk)
);

CREATE INDEX idx_fact_mkt_date     ON dwh.fact_marketing (date_key);
CREATE INDEX idx_fact_mkt_customer ON dwh.fact_marketing (customer_sk);
CREATE INDEX idx_fact_mkt_campaign ON dwh.fact_marketing (campaign_sk);

COMMENT ON TABLE dwh.fact_marketing IS 'Marketing campaign interaction fact — one row per customer × campaign contact.';
