"""
============================================================
python/02_data_cleaning/clean_stores.py
============================================================
Cleans the stores table:
  - Duplicate store IDs
  - Missing required fields (store_type, city, region)
  - Invalid store size (negative)
  - Standardise store_type values
============================================================
"""

import pandas as pd
from pathlib import Path
from rich.console import Console

console = Console()
PROCESSED_DIR = Path("data/processed")

VALID_STORE_TYPES = {"Superstore", "Mall Outlet", "Standalone", "Express", "Flagship"}
VALID_REGIONS     = {"North", "South", "West", "East", "Central"}


def main():
    console.rule("[bold cyan]Data Cleaning — Stores[/bold cyan]")
    df = pd.read_csv(PROCESSED_DIR / "stores.csv", low_memory=False)
    df["opening_date"] = pd.to_datetime(df["opening_date"], errors="coerce")
    original = len(df)
    console.print(f"Loaded: {original:,} stores")

    # 1. Dedup
    df = df.drop_duplicates(subset=["store_id"], keep="first")

    # 2. Standardise store_type
    df["store_type"] = df["store_type"].where(
        df["store_type"].isin(VALID_STORE_TYPES), "Standalone"
    )

    # 3. Standardise region
    df["region"] = df["region"].where(
        df["region"].isin(VALID_REGIONS), "Central"
    )

    # 4. Invalid store size
    df["store_size_sqft"] = df["store_size_sqft"].where(
        df["store_size_sqft"] > 0, None
    )

    # 5. Fill missing city/state
    df["city"]  = df["city"].fillna("Unknown")
    df["state"] = df["state"].fillna("Unknown")

    out = PROCESSED_DIR / "stores_clean.csv"
    df.to_csv(out, index=False)
    console.print(f"\n[green]Saved {len(df):,} clean stores -> {out}[/green]")


if __name__ == "__main__":
    main()
