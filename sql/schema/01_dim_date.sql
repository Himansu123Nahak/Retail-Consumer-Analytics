-- ============================================================
-- sql/schema/01_dim_date.sql
-- Date Dimension — full calendar with business attributes.
-- Covers 2016-01-01 through 2025-12-31.
-- ============================================================

DROP TABLE IF EXISTS dwh.dim_date;

CREATE TABLE dwh.dim_date (
    date_key        INTEGER      NOT NULL,          -- YYYYMMDD surrogate key
    full_date       DATE         NOT NULL,
    year            SMALLINT     NOT NULL,
    quarter         SMALLINT     NOT NULL,          -- 1-4
    quarter_name    CHAR(2)      NOT NULL,          -- Q1-Q4
    month           SMALLINT     NOT NULL,          -- 1-12
    month_name      VARCHAR(10)  NOT NULL,
    month_abbr      CHAR(3)      NOT NULL,
    week_of_year    SMALLINT     NOT NULL,
    day_of_month    SMALLINT     NOT NULL,
    day_of_week     SMALLINT     NOT NULL,          -- 1=Monday, 7=Sunday
    day_name        VARCHAR(10)  NOT NULL,
    day_abbr        CHAR(3)      NOT NULL,
    is_weekend      BOOLEAN      NOT NULL DEFAULT FALSE,
    is_month_start  BOOLEAN      NOT NULL DEFAULT FALSE,
    is_month_end    BOOLEAN      NOT NULL DEFAULT FALSE,
    is_quarter_start BOOLEAN     NOT NULL DEFAULT FALSE,
    is_quarter_end  BOOLEAN      NOT NULL DEFAULT FALSE,
    is_year_start   BOOLEAN      NOT NULL DEFAULT FALSE,
    is_year_end     BOOLEAN      NOT NULL DEFAULT FALSE,
    fiscal_year     SMALLINT     NOT NULL,          -- April fiscal start
    fiscal_quarter  SMALLINT     NOT NULL,
    fiscal_month    SMALLINT     NOT NULL,
    year_month      CHAR(7)      NOT NULL,          -- YYYY-MM
    year_quarter    CHAR(7)      NOT NULL,          -- YYYY-QN
    CONSTRAINT pk_dim_date PRIMARY KEY (date_key)
);

-- ── Populate dim_date via generate_series ──────────────────
INSERT INTO dwh.dim_date
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER                          AS date_key,
    d::DATE                                                   AS full_date,
    EXTRACT(YEAR  FROM d)::SMALLINT                           AS year,
    EXTRACT(QUARTER FROM d)::SMALLINT                         AS quarter,
    'Q' || EXTRACT(QUARTER FROM d)::TEXT                      AS quarter_name,
    EXTRACT(MONTH FROM d)::SMALLINT                           AS month,
    TO_CHAR(d, 'Month')                                       AS month_name,
    TO_CHAR(d, 'Mon')                                         AS month_abbr,
    EXTRACT(WEEK FROM d)::SMALLINT                            AS week_of_year,
    EXTRACT(DAY FROM d)::SMALLINT                             AS day_of_month,
    EXTRACT(ISODOW FROM d)::SMALLINT                          AS day_of_week,
    TO_CHAR(d, 'Day')                                         AS day_name,
    TO_CHAR(d, 'Dy')                                          AS day_abbr,
    EXTRACT(ISODOW FROM d) IN (6, 7)                          AS is_weekend,
    d = DATE_TRUNC('month', d)                                AS is_month_start,
    d = (DATE_TRUNC('month', d) + INTERVAL '1 month - 1 day') AS is_month_end,
    d = DATE_TRUNC('quarter', d)                              AS is_quarter_start,
    d = (DATE_TRUNC('quarter', d) + INTERVAL '3 months - 1 day') AS is_quarter_end,
    d = DATE_TRUNC('year', d)                                 AS is_year_start,
    d = DATE_TRUNC('year', d) + INTERVAL '1 year - 1 day'    AS is_year_end,
    -- Fiscal year: April start (FY2021 = Apr 2021 – Mar 2022)
    CASE WHEN EXTRACT(MONTH FROM d) >= 4
         THEN EXTRACT(YEAR FROM d)::SMALLINT
         ELSE (EXTRACT(YEAR FROM d) - 1)::SMALLINT
    END                                                        AS fiscal_year,
    CASE
        WHEN EXTRACT(MONTH FROM d) IN (4,5,6)   THEN 1
        WHEN EXTRACT(MONTH FROM d) IN (7,8,9)   THEN 2
        WHEN EXTRACT(MONTH FROM d) IN (10,11,12) THEN 3
        ELSE 4
    END::SMALLINT                                              AS fiscal_quarter,
    CASE
        WHEN EXTRACT(MONTH FROM d) >= 4
        THEN (EXTRACT(MONTH FROM d) - 3)::SMALLINT
        ELSE (EXTRACT(MONTH FROM d) + 9)::SMALLINT
    END                                                        AS fiscal_month,
    TO_CHAR(d, 'YYYY-MM')                                     AS year_month,
    TO_CHAR(d, 'YYYY') || '-Q' || EXTRACT(QUARTER FROM d)::TEXT AS year_quarter
FROM generate_series(
    '2016-01-01'::DATE,
    '2025-12-31'::DATE,
    '1 day'::INTERVAL
) AS g(d);

-- Indexes for common query patterns
CREATE INDEX idx_dim_date_year       ON dwh.dim_date (year);
CREATE INDEX idx_dim_date_year_month ON dwh.dim_date (year_month);
CREATE INDEX idx_dim_date_full_date  ON dwh.dim_date (full_date);

COMMENT ON TABLE dwh.dim_date IS 'Full calendar date dimension with business calendar attributes and Indian fiscal year (April start).';
