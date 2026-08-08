"""
============================================================
python/03_eda/03_product_eda.py
============================================================
Product Exploratory Data Analysis
Charts: revenue by category, top 10 products, margin by category,
        top brands, units sold by sub-category.
TECHNIQUES: pandas groupby/merge, horizontal bar charts
============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR    = Path("python/03_eda/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")

print("Loading data...")
txn  = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv")
prod = pd.read_csv(PROCESSED_DIR / "products_clean.csv")

# Merge product info onto transactions
df = txn.merge(prod[["product_id","product_name","category",
                       "sub_category","brand","margin_pct"]], on="product_id", how="left")
print(f"  {len(df):,} transaction records with product info\n")

# ── 1. Revenue by Category ───────────────────────────────────
cat_rev = df.groupby("category")["total_amount"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(cat_rev.index, cat_rev.values / 1e6,
                color=sns.color_palette("Set2", len(cat_rev)), edgecolor="white")
ax.set_title("Total Revenue by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (₹ Millions)")
for bar, v in zip(bars, cat_rev.values):
    ax.text(v/1e6 + 0.1, bar.get_y() + bar.get_height()/2,
            f"₹{v/1e6:.1f}M", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "14_revenue_by_category.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 14_revenue_by_category.png")

# ── 2. Units Sold by Category ────────────────────────────────
cat_units = df.groupby("category")["quantity"].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(cat_units.index, cat_units.values,
         color=sns.color_palette("Set3", len(cat_units)), edgecolor="white")
ax.set_title("Units Sold by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Total Units Sold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "15_units_by_category.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 15_units_by_category.png")

# ── 3. Top 10 Products by Revenue ───────────────────────────
top_products = (df.groupby("product_name")["total_amount"]
                  .sum().sort_values(ascending=False).head(10))

fig, ax = plt.subplots(figsize=(11, 5))
ax.barh(top_products.index[::-1], top_products.values[::-1] / 1e3,
         color="#42A5F5", edgecolor="white")
ax.set_title("Top 10 Products by Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Revenue (₹ Thousands)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "16_top10_products.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 16_top10_products.png")

# ── 4. Average Profit Margin by Category ────────────────────
cat_margin = prod.groupby("category")["margin_pct"].mean().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#EF5350" if v < 0.25 else "#66BB6A" for v in cat_margin.values]
ax.barh(cat_margin.index, cat_margin.values * 100, color=colors, edgecolor="white")
ax.axvline(25, color="gray", linestyle="--", linewidth=1, label="25% benchmark")
ax.set_title("Average Profit Margin % by Category\n(Red = below 25%)",
              fontsize=13, fontweight="bold")
ax.set_xlabel("Avg Margin (%)")
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "17_margin_by_category.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 17_margin_by_category.png")

# ── 5. Top 10 Brands by Revenue ──────────────────────────────
brand_rev = df.groupby("brand")["total_amount"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(brand_rev.index, brand_rev.values / 1e6,
        color="#FFA726", edgecolor="white")
ax.set_title("Top 10 Brands by Revenue", fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (₹ Millions)")
ax.tick_params(axis="x", rotation=35)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.1f}M"))
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "18_top10_brands.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 18_top10_brands.png")

print("\nProduct EDA complete. Charts in python/03_eda/charts/")
