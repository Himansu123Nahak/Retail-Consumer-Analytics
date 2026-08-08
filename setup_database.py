"""
============================================================
setup_database.py
============================================================
Automated PostgreSQL database setup script.
Run AFTER installing PostgreSQL and setting DB_PASSWORD in .env

Usage:
    py setup_database.py

What it does:
  1. Creates the retail_analytics database (if not exists)
  2. Runs all schema SQL scripts (schemas, dims, facts)
  3. Creates staging tables
  4. Loads all clean CSVs into staging
  5. Populates dimension tables from staging
  6. Populates fact tables from staging
  7. Creates analytical views
  8. Prints row count verification

============================================================
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────
HOST     = os.getenv("DB_HOST",     "localhost")
PORT     = int(os.getenv("DB_PORT", 5432))
DB_NAME  = os.getenv("DB_NAME",     "retail_analytics")
USER     = os.getenv("DB_USER",     "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "")

PROCESSED_DIR = Path("data/processed")
SQL_DIR       = Path("sql")

# Map staging table → clean CSV file
CSV_MAP = {
    "staging.stg_customers":    "customers_clean.csv",
    "staging.stg_products":     "products_clean.csv",
    "staging.stg_stores":       "stores.csv",
    "staging.stg_transactions": "transactions_clean.csv",
    "staging.stg_inventory":    "inventory_clean.csv",
    "staging.stg_marketing":    "marketing_campaigns.csv",
}

# SQL scripts to run in order
SQL_SCRIPTS = [
    SQL_DIR / "schema"          / "00_create_database.sql",
    SQL_DIR / "schema"          / "01_dim_date.sql",
    SQL_DIR / "schema"          / "02_dim_tables.sql",
    SQL_DIR / "schema"          / "03_fact_tables.sql",
    SQL_DIR / "staging"         / "load_staging_tables.sql",
    SQL_DIR / "transformations" / "populate_dim_tables.sql",
    SQL_DIR / "transformations" / "populate_fact_tables.sql",
    SQL_DIR / "transformations" / "create_analytical_views.sql",
]


def banner(text):
    print(f"\n{'='*55}")
    print(f"  {text}")
    print(f"{'='*55}")


def step(text):
    print(f"\n  >> {text}")


def ok(text):
    print(f"     OK  {text}")


def create_database():
    """Create the retail_analytics database if it doesn't exist."""
    step("Creating database...")
    conn = psycopg2.connect(host=HOST, port=PORT, user=USER,
                             password=PASSWORD, dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
    if cur.fetchone():
        ok(f"Database '{DB_NAME}' already exists.")
    else:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        ok(f"Database '{DB_NAME}' created.")
    cur.close()
    conn.close()


def connect_db():
    return psycopg2.connect(host=HOST, port=PORT, user=USER,
                              password=PASSWORD, dbname=DB_NAME)


def run_sql_file(conn, path: Path):
    step(f"Running: {path.name}")
    with open(path, encoding="utf-8") as f:
        sql_text = f.read()
    # Skip psql meta-commands (\i, \echo, \copy, \l, \q etc.)
    lines = [l for l in sql_text.splitlines()
             if not l.strip().startswith("\\")]
    cleaned = "\n".join(lines)
    if cleaned.strip():
        with conn.cursor() as cur:
            cur.execute(cleaned)
        conn.commit()
    ok(f"{path.name} done.")


def load_csv_to_staging(conn, table: str, csv_path: Path):
    step(f"Loading {csv_path.name} -> {table}")
    with open(csv_path, encoding="utf-8") as f:
        with conn.cursor() as cur:
            cur.copy_expert(
                f"COPY {table} FROM STDIN WITH CSV HEADER NULL ''",
                f
            )
    conn.commit()
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        n = cur.fetchone()[0]
    ok(f"{n:,} rows loaded.")


def verify_counts(conn):
    step("Verifying row counts...")
    tables = ["dwh.dim_customer","dwh.dim_product","dwh.dim_store",
               "dwh.dim_date","dwh.fact_sales","dwh.fact_inventory",
               "dwh.fact_marketing"]
    print()
    print(f"  {'Table':<28} {'Rows':>10}")
    print(f"  {'-'*28} {'-'*10}")
    with conn.cursor() as cur:
        for tbl in tables:
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            n = cur.fetchone()[0]
            print(f"  {tbl:<28} {n:>10,}")


def main():
    banner("Retail Analytics — Database Setup")

    if not PASSWORD:
        print("\n  ERROR: DB_PASSWORD is not set in .env file.")
        print("  Copy .env.example to .env and set your PostgreSQL password.")
        sys.exit(1)

    # Step 1 — Create database
    create_database()

    # Step 2 — Connect to retail_analytics
    conn = connect_db()
    conn.autocommit = False

    try:
        # Step 3 — Run all schema scripts
        for script in SQL_SCRIPTS[:5]:  # schema + staging DDL
            run_sql_file(conn, script)

        # Step 4 — Load CSVs into staging
        step("Loading CSV files into staging tables...")
        for table, filename in CSV_MAP.items():
            csv_path = PROCESSED_DIR / filename
            if csv_path.exists():
                load_csv_to_staging(conn, table, csv_path)
            else:
                print(f"     SKIP: {filename} not found.")

        # Step 5 — Populate dims and facts
        for script in SQL_SCRIPTS[5:]:
            run_sql_file(conn, script)

        # Step 6 — Verify
        verify_counts(conn)

        banner("Setup Complete!")
        print("  Connect Power BI to:")
        print(f"  Server: {HOST}:{PORT}")
        print(f"  Database: {DB_NAME}")
        print("  Follow: powerbi/POWERBI_GUIDE.md")

    except Exception as e:
        conn.rollback()
        print(f"\n  ERROR: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
