"""
============================================================
python/03_eda/05_inventory_marketing_eda.py
============================================================
Inventory & Marketing EDA
Charts: stockout rate, stock levels, campaign channels,
        response rate, spend distribution.
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

print("Loading inventory...")
inv  = pd.read_csv(PROCESSED_DIR / "inventory_clean.csv")
mkt  = pd.read_csv(PROCESSED_DIR / "marketing_campaigns.csv")
prod = pd.read_csv(PROCESSED_DIR / "products_clean.csv")

# ── 1. Average Closing Stock by Product Category ─────────────
inv_prod = inv.merge(prod[["product_id","category"]], on="product_id", how="left")
cat_stock = inv_prod.groupby("category")["closing_stock"].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(cat_stock.index[::-1], cat_stock.values[::-1],
         color="#42A5F5", edgecolor="white")
ax.set_title("Average Closing Stock by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Avg Closing Stock (Units)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "24_avg_stock_by_category.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 24_avg_stock_by_category.png")

# ── 2. Stock Level Distribution ───────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(inv["closing_stock"], bins=30, color="#66BB6A", edgecolor="white", rwidth=0.9)
ax.set_title("Closing Stock Level Distribution", fontsize=13, fontweight="bold")
ax.set_xlabel("Closing Stock Units")
ax.set_ylabel("Frequency")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "25_stock_level_distribution.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 25_stock_level_distribution.png")

# ── 3. Marketing — Campaign Response Rate by Channel ─────────
channel_stats = (mkt.groupby("channel")
                    .agg(contacts=("responded","count"),
                         responses=("responded","sum"))
                    .reset_index())
channel_stats["response_rate"] = (
    channel_stats["responses"] / channel_stats["contacts"] * 100
).round(1)

fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(channel_stats["channel"], channel_stats["response_rate"],
               color=["#EF5350" if r < 15 else "#66BB6A"
                      for r in channel_stats["response_rate"]],
               edgecolor="white", width=0.5)
for bar, v in zip(bars, channel_stats["response_rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{v}%", ha="center", fontweight="bold", fontsize=10)
ax.set_title("Campaign Response Rate by Channel  (Green = above 15%)",
              fontsize=13, fontweight="bold")
ax.set_xlabel("Channel"); ax.set_ylabel("Response Rate (%)")
ax.tick_params(axis="x", rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "26_response_rate_by_channel.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 26_response_rate_by_channel.png")

# ── 4. Campaign Contacts & Responses ─────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))
x = range(len(channel_stats))
width = 0.35
ax.bar([i - width/2 for i in x], channel_stats["contacts"],
        width=width, label="Total Contacts", color="#42A5F5", edgecolor="white")
ax.bar([i + width/2 for i in x], channel_stats["responses"],
        width=width, label="Responses", color="#FF7043", edgecolor="white")
ax.set_xticks(list(x)); ax.set_xticklabels(channel_stats["channel"], rotation=15)
ax.set_title("Campaign Contacts vs Responses by Channel", fontsize=13, fontweight="bold")
ax.set_ylabel("Count"); ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "27_contacts_vs_responses.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 27_contacts_vs_responses.png")

# ── 5. Top Campaigns by Response Count ───────────────────────
camp_stats = (mkt.groupby("campaign_name")
                 .agg(contacts=("responded","count"),
                       responses=("responded","sum"))
                 .reset_index()
                 .sort_values("responses", ascending=True))

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(camp_stats["campaign_name"], camp_stats["responses"],
         color="#AB47BC", edgecolor="white")
ax.set_title("Responses by Campaign Name", fontsize=13, fontweight="bold")
ax.set_xlabel("Total Responses")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "28_responses_by_campaign.png", dpi=120, bbox_inches="tight")
plt.close()
print("Saved: 28_responses_by_campaign.png")

print("\nInventory & Marketing EDA complete — charts 24-28 saved.")
