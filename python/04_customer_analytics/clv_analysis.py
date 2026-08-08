"""
============================================================
python/04_customer_analytics/clv_analysis.py
============================================================
Customer Lifetime Value — historical CLV calculation.
Simple approach: total spend per customer over the full period.
Also calculates average purchase value and purchase frequency.

TECHNIQUES USED: pandas groupby, merge, basic arithmetic
============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

# ── Load data ────────────────────────────────────────────────
print("Loading data...")
txn  = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv",
                    parse_dates=["transaction_date"])
cust = pd.read_csv(PROCESSED_DIR / "customers_clean.csv",
                    parse_dates=["signup_date"])

# ── Historical CLV per customer ──────────────────────────────
clv = (
    txn.groupby("customer_id")
       .agg(
           total_orders    = ("transaction_id", "count"),
           total_revenue   = ("total_amount",   "sum"),
           avg_order_value = ("total_amount",   "mean"),
           first_purchase  = ("transaction_date","min"),
           last_purchase   = ("transaction_date","max"),
       )
       .reset_index()
)
clv["total_revenue"]   = clv["total_revenue"].round(2)
clv["avg_order_value"] = clv["avg_order_value"].round(2)

# Days active = last purchase - first purchase
clv["days_active"] = (clv["last_purchase"] - clv["first_purchase"]).dt.days
clv["days_active"] = clv["days_active"].clip(lower=1)

# ── CLV tier ─────────────────────────────────────────────────
percentiles = clv["total_revenue"].quantile([0.25, 0.50, 0.75])

def clv_tier(revenue):
    if revenue >= percentiles[0.75]:
        return "High Value"
    elif revenue >= percentiles[0.50]:
        return "Mid Value"
    elif revenue >= percentiles[0.25]:
        return "Low Value"
    else:
        return "Very Low Value"

clv["clv_tier"] = clv["total_revenue"].apply(clv_tier)

# ── Merge with customer demographics ─────────────────────────
clv_full = clv.merge(
    cust[["customer_id", "age_group", "gender", "income_segment", "region"]],
    on="customer_id", how="left"
)

# ── Summary by tier ──────────────────────────────────────────
tier_summary = (
    clv_full.groupby("clv_tier")
            .agg(
                customer_count  = ("customer_id",    "count"),
                avg_clv         = ("total_revenue",  "mean"),
                total_revenue   = ("total_revenue",  "sum"),
                avg_orders      = ("total_orders",   "mean"),
            )
            .round(2)
            .reset_index()
)
print("\nCLV Tier Summary:")
print(tier_summary.to_string(index=False))

# ── Save ─────────────────────────────────────────────────────
clv_full.to_csv(PROCESSED_DIR / "customer_clv.csv", index=False)
print("\nSaved: customer_clv.csv")

# ── Chart: CLV distribution by tier ──────────────────────────
plt.figure(figsize=(10, 5))
tier_rev = tier_summary.set_index("clv_tier")["total_revenue"]
plt.bar(tier_rev.index, tier_rev.values, color=["#2196F3","#4CAF50","#FF9800","#F44336"])
plt.title("Total Revenue Contribution by CLV Tier", fontweight="bold")
plt.xlabel("CLV Tier")
plt.ylabel("Total Revenue (₹)")
plt.tight_layout()
plt.savefig("python/04_customer_analytics/clv_tiers.png", dpi=120, bbox_inches="tight")
plt.show()
print("Chart saved: clv_tiers.png")
