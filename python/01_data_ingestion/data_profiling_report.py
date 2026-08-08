"""
============================================================
python/01_data_ingestion/data_profiling_report.py
============================================================
Generates a detailed data profiling report for each table.
Prints: row count, column types, null counts, unique values,
        min/max/mean for numeric columns.

Usage:
    py python/01_data_ingestion/data_profiling_report.py
============================================================
"""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
PROCESSED_DIR = Path("data/processed")

TABLES = {
    "Transactions": "transactions_clean.csv",
    "Customers":    "customers_clean.csv",
    "Products":     "products_clean.csv",
    "Stores":       "stores.csv",
    "Inventory":    "inventory_clean.csv",
    "Marketing":    "marketing_campaigns.csv",
}


def profile_column(series):
    dtype   = str(series.dtype)
    nulls   = int(series.isnull().sum())
    unique  = int(series.nunique())
    if pd.api.types.is_numeric_dtype(series):
        return {
            "dtype": dtype, "nulls": nulls, "unique": unique,
            "min": round(float(series.min()), 2),
            "max": round(float(series.max()), 2),
            "mean": round(float(series.mean()), 2),
        }
    else:
        top = series.value_counts().index[0] if len(series) > 0 else "—"
        return {
            "dtype": dtype, "nulls": nulls, "unique": unique,
            "min": "—", "max": "—", "mean": str(top)[:20],
        }


def profile_table(name, path):
    df = pd.read_csv(path, low_memory=False)
    console.print(Panel(f"[bold]{name}[/bold]  —  {len(df):,} rows × {len(df.columns)} cols",
                         style="cyan"))

    tbl = Table(show_lines=True, expand=False)
    tbl.add_column("Column",     style="bold white", min_width=20)
    tbl.add_column("Type",       style="yellow")
    tbl.add_column("Nulls",      style="red",    justify="right")
    tbl.add_column("Unique",     justify="right")
    tbl.add_column("Min",        justify="right")
    tbl.add_column("Max",        justify="right")
    tbl.add_column("Mean / Top", justify="right")

    for col in df.columns:
        p = profile_column(df[col])
        tbl.add_row(
            col,
            p["dtype"],
            str(p["nulls"]),
            str(p["unique"]),
            str(p["min"]),
            str(p["max"]),
            str(p["mean"]),
        )
    console.print(tbl)
    console.print()


def main():
    console.rule("[bold blue]Data Profiling Report — Retail Analytics[/bold blue]")
    for name, filename in TABLES.items():
        path = PROCESSED_DIR / filename
        if path.exists():
            profile_table(name, path)
        else:
            console.print(f"[yellow]SKIP: {filename} not found[/yellow]")

    console.rule("[bold green]Profiling Complete[/bold green]")


if __name__ == "__main__":
    main()
