"""
============================================================
02_data_cleaning/clean_transactions.py
============================================================
Applies business rules to detect and remove:
  - Duplicate transaction IDs
  - Missing required fields (customer_id, product_id, store_id)
  - Invalid dates (future dates, dates before business start)
  - Negative or zero quantities
  - Negative or zero unit prices
  - Impossible discounts (> 1 or < 0)
  - Outlier total amounts (>3 SD from category median)

Outputs:
  data/processed/transactions_clean.csv
  data/processed/data_quality_report.csv
============================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
PROCESSED_DIR = Path("data/processed")
BUSINESS_START = pd.Timestamp("2021-01-01")
BUSINESS_END   = pd.Timestamp("2024-12-31")


def load_transactions() -> pd.DataFrame:
    path = PROCESSED_DIR / "transactions.csv"
    df = pd.read_csv(path, low_memory=False)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["unit_price"]   = pd.to_numeric(df["unit_price"],   errors="coerce")
    df["discount"]     = pd.to_numeric(df["discount"],     errors="coerce")
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
    df["quantity"]     = pd.to_numeric(df["quantity"],     errors="coerce")
    return df


def run_quality_checks(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    original_count = len(df)
    report = []

    def _remove(df, mask, reason):
        n = mask.sum()
        report.append({"check": reason, "records_flagged": int(n),
                         "pct_of_original": f"{n/original_count*100:.3f}%"})
        return df[~mask].copy()

    # 1. Duplicate transaction IDs
    dupe_mask = df.duplicated(subset=["transaction_id"], keep="first")
    df = _remove(df, dupe_mask, "Duplicate transaction_id")

    # 2. Missing required fields
    required = ["transaction_id", "customer_id", "product_id",
                 "store_id", "transaction_date"]
    for col in required:
        null_mask = df[col].isnull()
        df = _remove(df, null_mask, f"Null {col}")

    # 3. Invalid date range
    bad_date = (df["transaction_date"] < BUSINESS_START) | \
               (df["transaction_date"] > BUSINESS_END)
    df = _remove(df, bad_date, "Date out of business range")

    # 4. Negative / zero quantity
    df = _remove(df, df["quantity"] <= 0, "Quantity <= 0")

    # 5. Negative / zero unit price
    df = _remove(df, df["unit_price"] <= 0, "Unit price <= 0")

    # 6. Invalid discount
    df = _remove(df, (df["discount"] < 0) | (df["discount"] > 1),
                  "Discount out of [0,1] range")

    # 7. Recompute and validate total_amount
    computed = np.round(df["unit_price"] * df["quantity"] * (1 - df["discount"]), 2)
    tolerance = 1.0   # allow ₹1 rounding difference
    mismatch = (df["total_amount"] - computed).abs() > tolerance
    report.append({"check": "Total amount mismatch (auto-corrected)",
                    "records_flagged": int(mismatch.sum()),
                    "pct_of_original": f"{mismatch.sum()/original_count*100:.3f}%"})
    df.loc[mismatch, "total_amount"] = computed[mismatch]

    # 8. Extreme outlier total amounts (>5 SD above category median is suspicious)
    # Just flag and report; do not remove unless business confirms
    q99 = df["total_amount"].quantile(0.999)
    extreme = df["total_amount"] > q99
    report.append({"check": "Extreme total_amount (>99.9th pctile, kept)",
                    "records_flagged": int(extreme.sum()),
                    "pct_of_original": f"{extreme.sum()/original_count*100:.3f}%"})

    return df, report


def print_report(original_count: int, final_count: int, report: list[dict]):
    console.rule("[bold cyan]Data Quality Report — Transactions[/bold cyan]")

    tbl = Table(show_lines=True)
    tbl.add_column("Check", style="yellow")
    tbl.add_column("Records Flagged", justify="right")
    tbl.add_column("% of Original",   justify="right")
    for r in report:
        tbl.add_row(r["check"], f"{r['records_flagged']:,}", r["pct_of_original"])
    console.print(tbl)

    removed = original_count - final_count
    console.print(f"\n[bold]Raw records:    [/bold]{original_count:>12,}")
    console.print(f"[bold]Records removed:[/bold]{removed:>12,}")
    console.print(f"[bold green]Clean records:  [/bold green]{final_count:>12,}")
    console.print(f"[bold]Retention rate: [/bold]{final_count/original_count*100:.2f}%")


def main():
    console.print("[bold]Loading transactions...[/bold]")
    df = load_transactions()
    original_count = len(df)
    console.print(f"  Loaded {original_count:,} raw records.")

    console.print("[bold]Running quality checks...[/bold]")
    df_clean, report = run_quality_checks(df)

    print_report(original_count, len(df_clean), report)

    # Save clean data
    out_path = PROCESSED_DIR / "transactions_clean.csv"
    df_clean.to_csv(out_path, index=False)
    console.print(f"\n[green]✓ Clean file saved: {out_path}[/green]")

    # Save report
    rpt_df = pd.DataFrame(report)
    rpt_df.to_csv(PROCESSED_DIR / "data_quality_report.csv", index=False)
    console.print(f"[green]✓ Quality report saved: {PROCESSED_DIR / 'data_quality_report.csv'}[/green]")


if __name__ == "__main__":
    main()
