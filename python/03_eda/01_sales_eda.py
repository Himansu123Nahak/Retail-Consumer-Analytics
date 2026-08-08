"""
============================================================
python/03_eda/01_sales_eda.py
============================================================
Sales Exploratory Data Analysis
Charts: revenue by month, by day of week, by payment method,
        discount distribution, quantity distribution.
TECHNIQUES: pandas groupby, matplotlib bar/line charts
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

print("Loading transactions...")
txn = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv",
                   parse_dates=["transaction_date"])
txn["year"]        = txn["transaction_date"].dt.year
txn["month"]       = txn["transaction_date"].dt.month
txn["year_month"]  = txn["transaction_date"].dt.to_period("M").astype(str)
txn["day_of_week"] = txn["transaction_date"].dt.day_name()

print(f"  {len(txn):,} transactions loaded.\n")

# ── 1. Monthly Revenue Trend ─────────────────────────────────
monthly = txn.groupby("year_month")["total_amount"].sum().reset_index()
monthly.columns = ["year_month", "revenue"]

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly["year_month"], monthly["revenue"], marker="o", linewidth=2, color="#2196F3")
ax.fill_between(range(len(monthly)), monthly["revenue"], alpha=0.15, color="#2196F3")
ax.set_xticks(range(0, len(monthly), 3))
ax.set_xticklabels(monthly["year_month"].iloc[::3], rotation=45, ha="right")
ax.set_title("Monthly Revenue Trend (2021 – 2024)", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Total Revenue (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_monthly_revenue_trend.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 01_monthly_revenue_trend.png")

# ── 2. Revenue by Year ───────────────────────────────────────
yearly = txn.groupby("year")["total_amount"].sum().reset_index()

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(yearly["year"].astype(str), yearly["total_amount"],
              color=["#1565C0","#1976D2","#42A5F5","#90CAF9"], edgecolor="white", width=0.5)
for bar, val in zip(bars, yearly["total_amount"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + yearly["total_amount"].max()*0.01,
            f"₹{val/1e6:.1f}M", ha="center", fontsize=10, fontweight="bold")
ax.set_title("Annual Revenue (2021 – 2024)", fontsize=13, fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Revenue (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.0f}M"))
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_annual_revenue.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 02_annual_revenue.png")

# ── 3. Revenue by Day of Week ────────────────────────────────
DOW_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow = txn.groupby("day_of_week")["total_amount"].sum().reindex(DOW_ORDER).reset_index()
colors = ["#FF7043" if d in ("Saturday","Sunday") else "#42A5F5" for d in DOW_ORDER]

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(dow["day_of_week"], dow["total_amount"], color=colors, edgecolor="white")
ax.set_title("Revenue by Day of Week  (Orange = Weekend)", fontsize=13, fontweight="bold")
ax.set_xlabel("Day"); ax.set_ylabel("Revenue (₹)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
ax.tick_params(axis="x", rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_revenue_by_day.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 03_revenue_by_day.png")

# ── 4. Payment Method Distribution ──────────────────────────
pay = txn.groupby("payment_method")["total_amount"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 4))
wedges, texts, autotexts = ax.pie(
    pay.values, labels=pay.index,
    autopct="%1.1f%%", startangle=140,
    colors=sns.color_palette("Set2", len(pay))
)
ax.set_title("Revenue Share by Payment Method", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_payment_method.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 04_payment_method.png")

# ── 5. Discount Distribution ─────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(txn["discount"] * 100, bins=15, color="#7E57C2", edgecolor="white", rwidth=0.85)
ax.set_title("Distribution of Discounts Applied", fontsize=13, fontweight="bold")
ax.set_xlabel("Discount (%)"); ax.set_ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_discount_distribution.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 05_discount_distribution.png")

# ── 6. Order Value Distribution ──────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(txn["total_amount"].clip(upper=txn["total_amount"].quantile(0.99)),
         bins=40, color="#26A69A", edgecolor="white")
ax.set_title("Order Value Distribution (clipped at 99th percentile)",
              fontsize=13, fontweight="bold")
ax.set_xlabel("Order Value (₹)"); ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_order_value_dist.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 06_order_value_dist.png")

print("\nSales EDA complete. Charts saved to python/03_eda/charts/")
