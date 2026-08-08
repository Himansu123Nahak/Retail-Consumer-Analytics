"""
============================================================
python/02_data_cleaning/data_quality_report.py
============================================================
Generates a consolidated data quality summary report across
all tables. Prints a table and saves to:
  data/processed/master_quality_report.csv
============================================================
"""

import pandas as pd
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
PROCESSED_DIR = Path("data/processed")

FILES = {
    "transactions": "transactions_clean.csv",
    "customers":    "customers_clean.csv",
    "products":     "products_clean.csv",
    "stores":       "stores.csv",
    "inventory":    "inventory.csv",
    "marketing":    "marketing_campaigns.csv",
}

RAW_COUNTS = {
    "transactions": 200_000,
    "customers":    50_000,
    "products":     5_000,
    "stores":       200,
    "inventory":    60_000,
    "marketing":    100_000,
}


def profile(name, df):
    raw = RAW_COUNTS.get(name, len(df))
    nulls = int(df.isnull().sum().sum())
    dupes = int(df.duplicated().sum())
    return {
        "table":       name,
        "raw_records": raw,
        "clean_records": len(df),
        "removed":     raw - len(df),
        "retention_%": round(len(df) / raw * 100, 2),
        "null_cells":  nulls,
        "duplicate_rows": dupes,
    }


def main():
    console.rule("[bold cyan]Master Data Quality Report[/bold cyan]")
    results = []

    for name, fname in FILES.items():
        path = PROCESSED_DIR / fname
        if not path.exists():
            console.print(f"[yellow]  SKIP: {fname} not found[/yellow]")
            continue
        df = pd.read_csv(path, low_memory=False)
        results.append(profile(name, df))
        console.print(f"  [green]OK[/green] {name}: {len(df):,} records")

    # Print summary table
    tbl = Table(title="[bold]Data Quality Summary[/bold]", show_lines=True)
    cols = ["table","raw_records","clean_records","removed","retention_%","null_cells","duplicate_rows"]
    labels = ["Table","Raw","Clean","Removed","Retention %","Null Cells","Dupes"]
    for label in labels:
        tbl.add_column(label, justify="right" if label != "Table" else "left")

    for r in results:
        tbl.add_row(*[str(r[c]) for c in cols])

    console.print("\n")
    console.print(tbl)

    # Save
    out = PROCESSED_DIR / "master_quality_report.csv"
    pd.DataFrame(results).to_csv(out, index=False)
    console.print(f"\n[green]Report saved: {out}[/green]")


if __name__ == "__main__":
    main()
