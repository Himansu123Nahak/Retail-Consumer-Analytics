-- ============================================================
-- sql/schema/02_dim_customer.sql
-- Customer dimension table.
-- ============================================================

DROP TABLE IF EXISTS dwh.dim_customer;

CREATE TABLE dwh.dim_customer (
    customer_sk      SERIAL       NOT NULL,   -- surrogate key
    customer_id      VARCHAR(10)  NOT NULL,   -- business key
    age_group        VARCHAR(10)  NOT NULL,
    gender           VARCHAR(10)  NOT NULL,
    city             VARCHAR(60)  NOT NULL,
    state            VARCHAR(60)  NOT NULL,
    region           VARCHAR(20),             -- derived from city/state
    income_segment   VARCHAR(20)  NOT NULL,
    signup_date      DATE         NOT NULL,
    signup_date_key  INTEGER      NOT NULL,   -- FK to dim_date
    customer_segment VARCHAR(30)  NOT NULL DEFAULT 'Unassigned',  -- RFM segment
    is_active        BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_dim_customer PRIMARY KEY (customer_sk),
    CONSTRAINT uq_dim_customer_id UNIQUE (customer_id)
);

CREATE INDEX idx_dim_customer_id      ON dwh.dim_customer (customer_id);
CREATE INDEX idx_dim_customer_region  ON dwh.dim_customer (region);
CREATE INDEX idx_dim_customer_segment ON dwh.dim_customer (customer_segment);

COMMENT ON TABLE dwh.dim_customer IS 'Customer master dimension. customer_segment is updated by the RFM Python pipeline.';


-- ============================================================
-- sql/schema/03_dim_product.sql
-- Product dimension table.
-- ============================================================

DROP TABLE IF EXISTS dwh.dim_product;

CREATE TABLE dwh.dim_product (
    product_sk     SERIAL        NOT NULL,
    product_id     VARCHAR(10)   NOT NULL,
    product_name   VARCHAR(200)  NOT NULL,
    category       VARCHAR(50)   NOT NULL,
    sub_category   VARCHAR(50)   NOT NULL,
    brand          VARCHAR(80)   NOT NULL,
    cost_price     NUMERIC(12,2) NOT NULL,
    selling_price  NUMERIC(12,2) NOT NULL,
    margin_pct     NUMERIC(6,4)  NOT NULL,   -- (sell - cost) / sell
    supplier       VARCHAR(100),
    is_active      BOOLEAN       NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_dim_product PRIMARY KEY (product_sk),
    CONSTRAINT uq_dim_product_id UNIQUE (product_id)
);

CREATE INDEX idx_dim_product_id       ON dwh.dim_product (product_id);
CREATE INDEX idx_dim_product_category ON dwh.dim_product (category);
CREATE INDEX idx_dim_product_brand    ON dwh.dim_product (brand);

COMMENT ON TABLE dwh.dim_product IS 'Product master dimension with category hierarchy and margin attributes.';


-- ============================================================
-- sql/schema/04_dim_store.sql
-- Store dimension table.
-- ============================================================

DROP TABLE IF EXISTS dwh.dim_store;

CREATE TABLE dwh.dim_store (
    store_sk         SERIAL       NOT NULL,
    store_id         VARCHAR(10)  NOT NULL,
    store_name       VARCHAR(150) NOT NULL,
    store_type       VARCHAR(30)  NOT NULL,
    city             VARCHAR(60)  NOT NULL,
    state            VARCHAR(60)  NOT NULL,
    region           VARCHAR(20)  NOT NULL,
    store_size_sqft  INTEGER,
    opening_date     DATE,
    is_active        BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_dim_store PRIMARY KEY (store_sk),
    CONSTRAINT uq_dim_store_id UNIQUE (store_id)
);

CREATE INDEX idx_dim_store_id     ON dwh.dim_store (store_id);
CREATE INDEX idx_dim_store_region ON dwh.dim_store (region);
CREATE INDEX idx_dim_store_type   ON dwh.dim_store (store_type);

COMMENT ON TABLE dwh.dim_store IS 'Store master dimension with geographic and physical attributes.';


-- ============================================================
-- sql/schema/05_dim_campaign.sql
-- Marketing campaign dimension.
-- ============================================================

DROP TABLE IF EXISTS dwh.dim_campaign;

CREATE TABLE dwh.dim_campaign (
    campaign_sk    SERIAL       NOT NULL,
    campaign_name  VARCHAR(100) NOT NULL,
    channel        VARCHAR(50)  NOT NULL,
    CONSTRAINT pk_dim_campaign PRIMARY KEY (campaign_sk),
    CONSTRAINT uq_dim_campaign UNIQUE (campaign_name, channel)
);

COMMENT ON TABLE dwh.dim_campaign IS 'Marketing campaign dimension — one row per campaign × channel combination.';
