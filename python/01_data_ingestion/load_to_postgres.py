"""
============================================================
python/01_data_ingestion/load_to_postgres.py
============================================================
Loads all clean CSV files from data/processed/ into the
PostgreSQL staging schema using psycopg2 COPY.

Then calls:
  - populate_dim_tables.sql
  - populate_fact_tables.sql

Usage:
    Set DB credentials in .env, then run:
    python python/01_data_ingestion/load_to_postgres.py
============================================================
"""

import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Config ───────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "dbname":   os.getenv("DB_NAME",     "retail_analytics"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

PROCESSED_DIR = Path("data/processed")
SQL_DIR       = Path("sql")

FILES = {
    "staging.stg_customers":    "customers_clean.csv",
    "staging.stg_products":     "products_clean.csv",
    "staging.stg_stores":       "stores.csv",
    "staging.stg_transactions": "transactions_clean.csv",
    "staging.stg_inventory":    "inventory.csv",
    "staging.stg_marketing":    "marketing_campaigns.csv",
}


def connect():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    print(f"  Connected to {DB_CONFIG['dbname']} @ {DB_CONFIG['host']}")
    return conn


def run_sql_file(conn, filepath: Path):
    print(f"  Running SQL: {filepath.name}")
    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def load_csv(conn, table: str, csv_path: Path):
    print(f"  Loading {csv_path.name} → {table}")
    with open(csv_path, "r", encoding="utf-8") as f:
        with conn.cursor() as cur:
            cur.copy_expert(
                f"COPY {table} FROM STDIN WITH CSV HEADER NULL ''",
                f
            )
    conn.commit()
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
    print(f"    ✓ {count:,} rows loaded")


def main():
    conn = connect()
    try:
        # Step 1 — create schemas and tables
        print("\n[Step 1] Creating schema and tables...")
        for sql_file in sorted((SQL_DIR / "schema").glob("*.sql")):
            run_sql_file(conn, sql_file)

        # Step 2 — load staging
        print("\n[Step 2] Loading staging tables...")
        run_sql_file(conn, SQL_DIR / "staging" / "load_staging_tables.sql")
        for table, filename in FILES.items():
            csv_path = PROCESSED_DIR / filename
            if csv_path.exists():
                load_csv(conn, table, csv_path)
            else:
                print(f"  [SKIP] File not found: {csv_path}")

        # Step 3 — populate dimensions
        print("\n[Step 3] Populating dimension tables...")
        run_sql_file(conn, SQL_DIR / "transformations" / "populate_dim_tables.sql")

        # Step 4 — populate facts
        print("\n[Step 4] Populating fact tables...")
        run_sql_file(conn, SQL_DIR / "transformations" / "populate_fact_tables.sql")

        print("\n✅ Database load complete!")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
