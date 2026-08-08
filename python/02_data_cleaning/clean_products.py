"""
============================================================
02_data_cleaning/clean_products.py
============================================================
Cleans the products table:
  - Duplicate product IDs
  - Negative / zero cost or selling price
  - Selling price < cost price (margin < 0)
  - Missing category or sub_category
  - Standardise category values
============================================================
"""

import pandas as pd
from pathlib import Path
from rich.console import Console

console = Console()
PROCESSED_DIR = Path("data/processed")


def main():
    console.rule("[bold cyan]Data Cleaning — Products[/bold cyan]")
    df = pd.read_csv(PROCESSED_DIR / "products.csv", low_memory=False)
    df["cost_price"]    = pd.to_numeric(df["cost_price"],    errors="coerce")
    df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce")
    original = len(df)
    console.print(f"Loaded: {original:,} products")

    # 1. Dedup
    df = df.drop_duplicates(subset=["product_id"], keep="first")

    # 2. Invalid prices
    df = df[(df["cost_price"] > 0) & (df["selling_price"] > 0)]

    # 3. Selling price must exceed cost
    df = df[df["selling_price"] >= df["cost_price"]]

    # 4. Fill missing categoricals
    df["category"]     = df["category"].fillna("Uncategorised")
    df["sub_category"] = df["sub_category"].fillna("General")
    df["brand"]        = df["brand"].fillna("Unknown Brand")
    df["supplier"]     = df["supplier"].fillna("Unknown Supplier")

    # 5. Computed margin
    df["margin_pct"] = ((df["selling_price"] - df["cost_price"]) / df["selling_price"]).round(4)

    out = PROCESSED_DIR / "products_clean.csv"
    df.to_csv(out, index=False)
    console.print(f"\n[green]✓ Saved {len(df):,} clean products → {out}[/green]")
    console.print(f"  Removed {original - len(df):,} records")


if __name__ == "__main__":
    main()
