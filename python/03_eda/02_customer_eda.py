"""
============================================================
python/03_eda/02_customer_eda.py
============================================================
Customer Exploratory Data Analysis
Charts: signups by year, age group distribution, gender split,
        income segment, region distribution, orders per customer.
TECHNIQUES: pandas groupby, bar charts, pie chart
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
cust = pd.read_csv(PROCESSED_DIR / "customers_clean.csv",
                    parse_dates=["signup_date"])
txn  = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv")

print(f"  {len(cust):,} customers | {len(txn):,} transactions\n")

# ── 1. Customer Signups by Year ──────────────────────────────
cust["signup_year"] = cust["signup_date"].dt.year
signups = cust.groupby("signup_year").size().reset_index(name="new_customers")

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(signups["signup_year"].astype(str), signups["new_customers"],
        color="#42A5F5", edgecolor="white", width=0.5)
ax.set_title("New Customer Signups by Year", fontsize=13, fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("New Customers")
for i, v in enumerate(signups["new_customers"]):
    ax.text(i, v + 50, f"{v:,}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "07_customer_signups.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 07_customer_signups.png")

# ── 2. Age Group Distribution ────────────────────────────────
AGE_ORDER = ["18-24", "25-34", "35-44", "45-54", "55+"]
age_dist  = cust["age_group"].value_counts().reindex(AGE_ORDER)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(age_dist.index, age_dist.values, color="#FF7043", edgecolor="white", width=0.5)
ax.set_title("Customer Count by Age Group", fontsize=13, fontweight="bold")
ax.set_xlabel("Age Group"); ax.set_ylabel("Customers")
for i, v in enumerate(age_dist.values):
    ax.text(i, v + 50, f"{v:,}", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "08_age_distribution.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 08_age_distribution.png")

# ── 3. Gender Split ──────────────────────────────────────────
gender_dist = cust["gender"].value_counts()

fig, ax = plt.subplots(figsize=(6, 5))
ax.pie(gender_dist.values, labels=gender_dist.index,
        autopct="%1.1f%%", startangle=90,
        colors=["#42A5F5","#FF7043","#AB47BC"])
ax.set_title("Customer Gender Distribution", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "09_gender_split.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 09_gender_split.png")

# ── 4. Income Segment Distribution ──────────────────────────
INC_ORDER = ["Low","Lower-Middle","Middle","Upper-Middle","High"]
inc_dist  = cust["income_segment"].value_counts().reindex(INC_ORDER)

fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.barh(inc_dist.index, inc_dist.values, color="#66BB6A", edgecolor="white")
ax.set_title("Customers by Income Segment", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Customers")
for bar, v in zip(bars, inc_dist.values):
    ax.text(v + 50, bar.get_y() + bar.get_height()/2,
            f"{v:,}", va="center", fontsize=10)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "10_income_segment.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 10_income_segment.png")

# ── 5. Customers by Region ───────────────────────────────────
region_dist = cust["state"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 4))
ax.barh(region_dist.index[::-1], region_dist.values[::-1],
         color="#AB47BC", edgecolor="white")
ax.set_title("Top 10 States by Customer Count", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Customers")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "11_customers_by_state.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 11_customers_by_state.png")

# ── 6. Orders per Customer Distribution ─────────────────────
orders_per_cust = txn.groupby("customer_id")["transaction_id"].count()

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(orders_per_cust.clip(upper=20), bins=20,
         color="#26C6DA", edgecolor="white", rwidth=0.9)
ax.set_title("Orders per Customer Distribution (capped at 20)",
              fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Orders"); ax.set_ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "12_orders_per_customer.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 12_orders_per_customer.png")

# ── 7. Revenue by Age Group ──────────────────────────────────
txn_cust = txn.merge(cust[["customer_id","age_group"]], on="customer_id", how="left")
age_rev  = txn_cust.groupby("age_group")["total_amount"].sum().reindex(AGE_ORDER)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(age_rev.index, age_rev.values / 1e6, color="#FFA726", edgecolor="white", width=0.5)
ax.set_title("Total Revenue by Age Group", fontsize=13, fontweight="bold")
ax.set_xlabel("Age Group"); ax.set_ylabel("Revenue (₹ Millions)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "13_revenue_by_age.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 13_revenue_by_age.png")

print("\nCustomer EDA complete. Charts in python/03_eda/charts/")
