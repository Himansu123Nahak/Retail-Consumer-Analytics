"""
============================================================
python/07_statistical_analysis/basic_correlations.py
============================================================
Simple correlation and trend analysis between key business
variables — using only basic pandas and matplotlib.

Analyses:
  1. Discount % vs quantity sold
  2. Store size vs revenue
  3. Day of week vs revenue

TECHNIQUES USED: pandas groupby, corr(), basic scatter/bar plots
============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

# ── Load data ────────────────────────────────────────────────
print("Loading data...")
txn    = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv",
                      parse_dates=["transaction_date"])
stores = pd.read_csv(PROCESSED_DIR / "stores.csv")

# ── 1. Discount % vs Average Quantity Sold ───────────────────
print("\nAnalysis 1: Discount vs Quantity Sold")
disc_qty = (
    txn.groupby("discount")
       .agg(avg_quantity = ("quantity", "mean"),
             order_count = ("transaction_id", "count"))
       .reset_index()
       .query("order_count >= 10")        # only discount levels with enough data
)
corr_val = disc_qty["discount"].corr(disc_qty["avg_quantity"])
print(f"  Correlation (discount vs avg qty): {corr_val:.3f}")

plt.figure(figsize=(8, 5))
plt.scatter(disc_qty["discount"] * 100, disc_qty["avg_quantity"],
            alpha=0.6, color="steelblue", s=60)
plt.title(f"Discount % vs Average Quantity Sold\n(Correlation = {corr_val:.3f})")
plt.xlabel("Discount (%)")
plt.ylabel("Average Quantity per Order")
plt.tight_layout()
plt.savefig("python/07_statistical_analysis/discount_vs_quantity.png",
            dpi=120, bbox_inches="tight")
plt.show()

# ── 2. Store Size vs Revenue ─────────────────────────────────
print("\nAnalysis 2: Store Size vs Revenue")
store_rev = (
    txn.groupby("store_id")["total_amount"]
       .sum()
       .reset_index()
       .rename(columns={"total_amount": "total_revenue"})
)
store_merged = store_rev.merge(stores[["store_id","store_size_sqft"]], on="store_id", how="left")
store_merged = store_merged.dropna(subset=["store_size_sqft"])

corr_size = store_merged["store_size_sqft"].corr(store_merged["total_revenue"])
print(f"  Correlation (store size vs revenue): {corr_size:.3f}")

plt.figure(figsize=(8, 5))
plt.scatter(store_merged["store_size_sqft"], store_merged["total_revenue"],
            alpha=0.5, color="coral", s=40)
plt.title(f"Store Size (sqft) vs Total Revenue\n(Correlation = {corr_size:.3f})")
plt.xlabel("Store Size (sqft)")
plt.ylabel("Total Revenue (₹)")
plt.tight_layout()
plt.savefig("python/07_statistical_analysis/store_size_vs_revenue.png",
            dpi=120, bbox_inches="tight")
plt.show()

# ── 3. Day of Week vs Revenue ────────────────────────────────
print("\nAnalysis 3: Day of Week vs Revenue")
txn["day_of_week"] = txn["transaction_date"].dt.day_name()
DOW_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

dow_revenue = (
    txn.groupby("day_of_week")["total_amount"]
       .sum()
       .reindex(DOW_ORDER)
       .reset_index()
)
plt.figure(figsize=(9, 5))
plt.bar(dow_revenue["day_of_week"], dow_revenue["total_amount"],
        color=["#4CAF50" if d in ("Saturday","Sunday") else "#2196F3"
               for d in dow_revenue["day_of_week"]])
plt.title("Total Revenue by Day of Week\n(Green = Weekend)")
plt.xlabel("Day of Week")
plt.ylabel("Total Revenue (₹)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("python/07_statistical_analysis/revenue_by_day.png",
            dpi=120, bbox_inches="tight")
plt.show()

print("\nAll analyses saved to python/07_statistical_analysis/")
