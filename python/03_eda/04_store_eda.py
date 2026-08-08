"""
============================================================
python/03_eda/04_store_eda.py
============================================================
Store & Geography EDA
Charts: revenue by region, top 10 stores, store type revenue,
        stores by city, revenue vs store size scatter.
TECHNIQUES: pandas groupby/merge, bar charts, scatter plot
============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR    = Path("python/03_eda/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")

print("Loading data...")
txn    = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv")
stores = pd.read_csv(PROCESSED_DIR / "stores.csv")

df = txn.merge(stores[["store_id","store_name","store_type",
                          "city","state","region","store_size_sqft"]],
                on="store_id", how="left")
print(f"  {len(df):,} records loaded.\n")

# ── 1. Revenue by Region ─────────────────────────────────────
region_rev = df.groupby("region")["total_amount"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(region_rev.index, region_rev.values / 1e6,
               color=sns.color_palette("Set2", len(region_rev)), edgecolor="white", width=0.5)
for bar, v in zip(bars, region_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f"₹{v/1e6:.1f}M", ha="center", fontsize=10, fontweight="bold")
ax.set_title("Total Revenue by Region", fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (₹ Millions)"); ax.set_xlabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "19_revenue_by_region.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 19_revenue_by_region.png")

# ── 2. Top 10 Stores by Revenue ──────────────────────────────
store_rev = (df.groupby("store_name")["total_amount"]
               .sum().sort_values(ascending=False).head(10))

fig, ax = plt.subplots(figsize=(11, 5))
ax.barh(store_rev.index[::-1], store_rev.values[::-1] / 1e3,
         color="#42A5F5", edgecolor="white")
ax.set_title("Top 10 Stores by Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (₹ Thousands)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "20_top10_stores.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 20_top10_stores.png")

# ── 3. Revenue by Store Type ──────────────────────────────────
type_rev = df.groupby("store_type")["total_amount"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(type_rev.index, type_rev.values / 1e6,
        color="#FFA726", edgecolor="white", width=0.5)
ax.set_title("Revenue by Store Type", fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (₹ Millions)"); ax.set_xlabel("Store Type")
ax.tick_params(axis="x", rotation=15)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "21_revenue_by_store_type.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 21_revenue_by_store_type.png")

# ── 4. Revenue by State (Top 10) ─────────────────────────────
state_rev = (df.groupby("state")["total_amount"]
               .sum().sort_values(ascending=False).head(10))

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(state_rev.index[::-1], state_rev.values[::-1] / 1e6,
         color="#66BB6A", edgecolor="white")
ax.set_title("Top 10 States by Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (₹ Millions)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "22_revenue_by_state.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 22_revenue_by_state.png")

# ── 5. Store Size vs Revenue Scatter ─────────────────────────
store_summary = (df.groupby(["store_id","store_size_sqft"])["total_amount"]
                   .sum().reset_index())

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(store_summary["store_size_sqft"],
            store_summary["total_amount"] / 1e3,
            alpha=0.5, color="#7E57C2", s=50, edgecolors="white", linewidths=0.5)
ax.set_title("Store Size (sqft) vs Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Store Size (sqft)"); ax.set_ylabel("Revenue (₹ Thousands)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "23_store_size_vs_revenue.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 23_store_size_vs_revenue.png")

print("\nStore EDA complete. Charts in python/03_eda/charts/")
