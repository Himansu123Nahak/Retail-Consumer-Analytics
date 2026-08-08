"""
============================================================
python/02_data_cleaning/clean_inventory.py
============================================================
Cleans the inventory table:
  - Duplicate snapshot (date + store + product) combinations
  - Negative stock values (set to 0)
  - Closing stock math check: closing = opening + purchase - sales
  - Missing store_id or product_id
============================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from rich.console import Console

console = Console()
PROCESSED_DIR = Path("data/processed")


def main():
    console.rule("[bold cyan]Data Cleaning — Inventory[/bold cyan]")
    df = pd.read_csv(PROCESSED_DIR / "inventory.csv", low_memory=False)
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce")

    for col in ["opening_stock","purchase_qty","sales_qty","closing_stock"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    original = len(df)
    console.print(f"Loaded: {original:,} inventory records")

    # 1. Drop rows missing key IDs
    df = df.dropna(subset=["snapshot_date","store_id","product_id"])

    # 2. Dedup (same day + store + product)
    df = df.drop_duplicates(subset=["snapshot_date","store_id","product_id"], keep="first")

    # 3. Clip negative stock values to 0
    for col in ["opening_stock","purchase_qty","sales_qty","closing_stock"]:
        df[col] = df[col].clip(lower=0)

    # 4. Recompute closing stock where it doesn't match
    expected_closing = (df["opening_stock"] + df["purchase_qty"] - df["sales_qty"]).clip(lower=0)
    mismatch = (df["closing_stock"] - expected_closing).abs() > 2
    df.loc[mismatch, "closing_stock"] = expected_closing[mismatch]

    # 5. Recompute stockout flag
    df["stockout_flag"] = ((df["closing_stock"] == 0) & (df["sales_qty"] > 0)).astype(int)

    out = PROCESSED_DIR / "inventory_clean.csv"
    df.to_csv(out, index=False)
    console.print(f"\n[green]Saved {len(df):,} clean inventory records -> {out}[/green]")
    console.print(f"  Removed {original - len(df):,} records")
    console.print(f"  Stockout records: {df['stockout_flag'].sum():,}")


if __name__ == "__main__":
    main()
