"""
============================================================
python/04_customer_analytics/rfm_analysis.py
============================================================
RFM (Recency, Frequency, Monetary) analysis.
Scores each customer on a 1-5 scale per dimension, then
assigns simple business segments.

TECHNIQUES USED: pandas groupby, merge, cut, basic arithmetic
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import date

# ── Config ───────────────────────────────────────────────────
PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR    = Path("data/processed")
SNAPSHOT_DATE = date(2025, 1, 1)          # "today" relative to the dataset

# ── Load data ────────────────────────────────────────────────
print("Loading transactions...")
txn = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv",
                   parse_dates=["transaction_date"])

# ── Compute RFM per customer ─────────────────────────────────
print("Computing RFM metrics...")
snapshot = pd.Timestamp(SNAPSHOT_DATE)

rfm = (
    txn.groupby("customer_id")
       .agg(
           recency   = ("transaction_date", lambda x: (snapshot - x.max()).days),
           frequency = ("transaction_id",   "count"),
           monetary  = ("total_amount",     "sum"),
       )
       .reset_index()
)
rfm["monetary"] = rfm["monetary"].round(2)

# ── Score each dimension 1-5 (5 = best) ─────────────────────
# Recency: lower days = better = score 5
rfm["R_score"] = pd.cut(rfm["recency"],
                          bins=5, labels=[5, 4, 3, 2, 1]).astype(int)

# Frequency and Monetary: higher = better = score 5
rfm["F_score"] = pd.cut(rfm["frequency"],
                          bins=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M_score"] = pd.cut(rfm["monetary"],
                          bins=5, labels=[1, 2, 3, 4, 5]).astype(int)

rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

# ── Assign segments based on RFM total score ─────────────────
def assign_segment(score):
    if score >= 13:
        return "Champions"
    elif score >= 11:
        return "Loyal Customers"
    elif score >= 9:
        return "Potential Loyalists"
    elif score >= 7:
        return "At Risk"
    elif score >= 5:
        return "Need Attention"
    else:
        return "Lost Customers"

rfm["segment"] = rfm["RFM_score"].apply(assign_segment)

# ── Summary ──────────────────────────────────────────────────
segment_summary = (
    rfm.groupby("segment")
       .agg(
           customer_count = ("customer_id", "count"),
           avg_recency    = ("recency",    "mean"),
           avg_frequency  = ("frequency",  "mean"),
           avg_monetary   = ("monetary",   "mean"),
           total_revenue  = ("monetary",   "sum"),
       )
       .round(2)
       .reset_index()
)
print("\nRFM Segment Summary:")
print(segment_summary.to_string(index=False))

# ── Save output ──────────────────────────────────────────────
rfm.to_csv(OUTPUT_DIR / "rfm_scores.csv", index=False)
segment_summary.to_csv(OUTPUT_DIR / "rfm_segment_summary.csv", index=False)
print(f"\nSaved: rfm_scores.csv, rfm_segment_summary.csv")

# ── Basic visualisations ─────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("RFM Customer Segmentation", fontsize=14, fontweight="bold")

# Segment distribution — bar chart
seg_counts = rfm["segment"].value_counts()
axes[0].bar(seg_counts.index, seg_counts.values, color="steelblue", edgecolor="white")
axes[0].set_title("Customers per Segment")
axes[0].set_xlabel("Segment")
axes[0].set_ylabel("Number of Customers")
axes[0].tick_params(axis="x", rotation=30)

# Revenue by segment — bar chart
rev_by_seg = rfm.groupby("segment")["monetary"].sum().sort_values(ascending=False)
axes[1].bar(rev_by_seg.index, rev_by_seg.values, color="coral", edgecolor="white")
axes[1].set_title("Revenue by Segment")
axes[1].set_xlabel("Segment")
axes[1].set_ylabel("Total Revenue (₹)")
axes[1].tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("python/04_customer_analytics/rfm_segments.png", dpi=120, bbox_inches="tight")
plt.show()
print("Chart saved: rfm_segments.png")
