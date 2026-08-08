"""
============================================================
02_data_cleaning/clean_customers.py
============================================================
Cleans the customers table:
  - Duplicate customer IDs
  - Invalid signup dates
  - Standardise gender/income_segment values
  - Fill missing city/state
  - Remove impossible age groups
============================================================
"""

import pandas as pd
from pathlib import Path
from rich.console import Console

console = Console()
PROCESSED_DIR = Path("data/processed")

VALID_GENDERS  = {"Male", "Female", "Other"}
VALID_INCOMES  = {"Low", "Lower-Middle", "Middle", "Upper-Middle", "High"}
VALID_AGES     = {"18-24", "25-34", "35-44", "45-54", "55+"}


def main():
    console.rule("[bold cyan]Data Cleaning — Customers[/bold cyan]")
    df = pd.read_csv(PROCESSED_DIR / "customers.csv", low_memory=False)
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    original = len(df)
    console.print(f"Loaded: {original:,} customers")

    # 1. Dedup
    df = df.drop_duplicates(subset=["customer_id"], keep="first")
    console.print(f"  After dedup: {len(df):,}")

    # 2. Invalid signup dates
    df = df[df["signup_date"].between("2010-01-01", "2024-12-31")]
    console.print(f"  After date filter: {len(df):,}")

    # 3. Standardise categoricals
    df["gender"]         = df["gender"].where(df["gender"].isin(VALID_GENDERS), "Other")
    df["income_segment"] = df["income_segment"].where(df["income_segment"].isin(VALID_INCOMES), "Middle")
    df["age_group"]      = df["age_group"].where(df["age_group"].isin(VALID_AGES), "25-34")

    # 4. Fill missing city/state
    df["city"]  = df["city"].fillna("Unknown")
    df["state"] = df["state"].fillna("Unknown")

    out = PROCESSED_DIR / "customers_clean.csv"
    df.to_csv(out, index=False)
    console.print(f"\n[green]✓ Saved {len(df):,} clean customers → {out}[/green]")
    console.print(f"  Removed {original - len(df):,} records ({(original-len(df))/original*100:.2f}%)")


if __name__ == "__main__":
    main()
