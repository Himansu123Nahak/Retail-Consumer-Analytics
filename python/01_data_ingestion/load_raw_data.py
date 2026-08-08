"""
============================================================
01_data_ingestion/load_raw_data.py
============================================================
Loads all processed CSVs, prints schema/profile summary,
and validates basic expectations.
============================================================
"""

import os
import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
PROCESSED_DIR = Path("data/processed")

TABLES = {
    "customers":           "customers.csv",
    "products":            "products.csv",
    "stores":              "stores.csv",
    "transactions":        "transactions.csv",
    "inventory":           "inventory.csv",
    "marketing_campaigns": "marketing_campaigns.csv",
}

DTYPE_HINTS = {
    "transactions": {
        "transaction_date": "str",
        "unit_price":       "float64",
        "discount":         "float64",
        "total_amount":     "float64",
        "quantity":         "int64",
    },
    "inventory": {
        "snapshot_date":  "str",
        "opening_stock":  "int64",
        "purchase_qty":   "int64",
        "sales_qty":      "int64",
        "closing_stock":  "int64",
        "stockout_flag":  "int8",
    },
}


def load_table(name: str, filename: str) -> pd.DataFrame:
    path = PROCESSED_DIR / filename
    if not path.exists():
        console.print(f"[red]  ✗ File not found: {path}[/red]")
        return pd.DataFrame()

    dtype = DTYPE_HINTS.get(name, {})
    df = pd.read_csv(path, dtype=dtype, low_memory=False)

    # Parse date columns
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def profile_table(name: str, df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    return {
        "table":    name,
        "rows":     f"{len(df):,}",
        "cols":     len(df.columns),
        "nulls":    int(df.isnull().sum().sum()),
        "dupes":    int(df.duplicated().sum()),
        "mem_mb":   f"{df.memory_usage(deep=True).sum() / 1e6:.1f}",
    }


def main():
    console.rule("[bold cyan]Retail Analytics — Data Ingestion[/bold cyan]")

    dfs = {}
    profiles = []

    for name, filename in TABLES.items():
        console.print(f"\n[bold]Loading:[/] {filename}")
        df = load_table(name, filename)
        if not df.empty:
            dfs[name] = df
            profile = profile_table(name, df)
            profiles.append(profile)
            console.print(f"  [green]✓[/green] {len(df):,} rows × {len(df.columns)} cols")

    # Print summary table
    console.print("\n")
    table = Table(title="[bold]Dataset Summary[/bold]", show_lines=True)
    table.add_column("Table",   style="cyan bold")
    table.add_column("Rows",    justify="right")
    table.add_column("Cols",    justify="right")
    table.add_column("Nulls",   justify="right")
    table.add_column("Dupes",   justify="right")
    table.add_column("Mem (MB)",justify="right")

    for p in profiles:
        table.add_row(
            p["table"], p["rows"], str(p["cols"]),
            str(p["nulls"]), str(p["dupes"]), p["mem_mb"]
        )
    console.print(table)

    # Date range check for transactions
    if "transactions" in dfs:
        txn = dfs["transactions"]
        console.print(f"\n[bold]Transaction date range:[/] "
                       f"{txn['transaction_date'].min().date()} "
                       f"→ {txn['transaction_date'].max().date()}")

    console.print("\n[bold green]Data ingestion complete.[/bold green]")
    return dfs


if __name__ == "__main__":
    main()
