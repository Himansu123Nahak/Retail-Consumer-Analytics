"""
============================================================
00_data_generation/augment_to_scale.py
============================================================
Takes the raw Olist Brazilian E-Commerce Kaggle dataset and
augments it to ~2 million transaction records with realistic
retail patterns including:
  - Multi-year date expansion (2016-2024)
  - Seasonality (holiday spikes, weekday patterns)
  - Regional Indian/global store network overlay
  - Inventory table generation
  - Marketing campaign table generation
  - Customer interaction log generation

Usage:
    python python/00_data_generation/augment_to_scale.py

Outputs (to data/processed/):
    customers.csv
    products.csv
    stores.csv
    transactions.csv
    inventory.csv
    marketing_campaigns.csv
    customer_interactions.csv
============================================================
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from tqdm import tqdm

# â”€â”€ Configuration â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SEED = 42
TARGET_TRANSACTIONS = 200_000
DATE_START = datetime(2021, 1, 1)
DATE_END   = datetime(2024, 12, 31)

RAW_DIR       = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

random.seed(SEED)
np.random.seed(SEED)

# â”€â”€ Regional data â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
REGIONS = {
    "North":     ["Delhi", "Chandigarh", "Jaipur", "Lucknow", "Agra"],
    "South":     ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore"],
    "West":      ["Mumbai", "Pune", "Ahmedabad", "Surat", "Vadodara"],
    "East":      ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi"],
    "Central":   ["Bhopal", "Indore", "Nagpur", "Raipur", "Jabalpur"],
}

STATES_MAP = {
    "Delhi": "Delhi", "Chandigarh": "Punjab", "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh", "Agra": "Uttar Pradesh",
    "Bengaluru": "Karnataka", "Chennai": "Tamil Nadu", "Hyderabad": "Telangana",
    "Kochi": "Kerala", "Coimbatore": "Tamil Nadu",
    "Mumbai": "Maharashtra", "Pune": "Maharashtra", "Ahmedabad": "Gujarat",
    "Surat": "Gujarat", "Vadodara": "Gujarat",
    "Kolkata": "West Bengal", "Bhubaneswar": "Odisha", "Patna": "Bihar",
    "Guwahati": "Assam", "Ranchi": "Jharkhand",
    "Bhopal": "Madhya Pradesh", "Indore": "Madhya Pradesh",
    "Nagpur": "Maharashtra", "Raipur": "Chhattisgarh", "Jabalpur": "Madhya Pradesh",
}

STORE_TYPES    = ["Superstore", "Mall Outlet", "Standalone", "Express", "Flagship"]
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking", "EMI"]

CATEGORIES = {
    "Electronics":    ["Smartphones", "Laptops", "Tablets", "Cameras", "Headphones",
                        "Smart Watches", "Cables & Accessories", "Gaming"],
    "Fashion":        ["Men's Clothing", "Women's Clothing", "Footwear",
                        "Bags & Luggage", "Jewelry & Accessories"],
    "Home & Kitchen": ["Furniture", "Kitchen Appliances", "Cookware",
                        "Home Decor", "Bedding"],
    "Sports":         ["Fitness Equipment", "Outdoor & Adventure", "Sportswear",
                        "Cricket", "Cycling"],
    "Books & Media":  ["Books", "Stationery", "Music & Instruments"],
    "Beauty":         ["Skincare", "Haircare", "Makeup", "Fragrances"],
    "Groceries":      ["Snacks & Beverages", "Dairy & Eggs", "Fresh Produce",
                        "Packaged Foods"],
    "Toys & Baby":    ["Toys & Games", "Baby Care", "Educational"],
}

BRANDS = {
    "Electronics": ["Samsung", "Apple", "OnePlus", "Sony", "LG", "Lenovo", "Dell", "HP"],
    "Fashion":     ["Zara", "H&M", "Levi's", "Nike", "Adidas", "Puma", "Arrow", "Van Heusen"],
    "Home & Kitchen": ["Philips", "Bosch", "Prestige", "Bajaj", "IKEA", "Godrej"],
    "Sports":      ["Nike", "Adidas", "Decathlon", "Cosco", "Vector X"],
    "Books & Media": ["Penguin", "Harper Collins", "Scholastic", "Oxford"],
    "Beauty":      ["Lakme", "L'Oreal", "Himalaya", "Mamaearth", "Biotique"],
    "Groceries":   ["Amul", "Nestle", "ITC", "Britannia", "Haldiram's"],
    "Toys & Baby": ["Fisher-Price", "Lego", "Funskool", "Hasbro"],
}

CAMPAIGN_CHANNELS = ["Email", "SMS", "Social Media", "In-App", "Push Notification"]
CAMPAIGN_NAMES    = [
    "Diwali Sale", "End of Season", "New Year Bonanza", "Republic Day",
    "Summer Sale", "Monsoon Fest", "Holi Celebration", "Onam Special",
    "Weekend Flash", "Loyalty Rewards", "Back to School", "Festival Bonanza",
]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
INCOME_SEGS = ["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"]
GENDERS = ["Male", "Female", "Other"]


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  HELPER: realistic date sampler with seasonality
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def _sample_dates(n: int, start: datetime, end: datetime) -> np.ndarray:
    """Sample n dates with seasonality weights (festival months spike)."""
    total_days = (end - start).days + 1
    day_range  = np.arange(total_days)
    dates      = np.array([start + timedelta(days=int(d)) for d in day_range])

    # Base weight
    weights = np.ones(total_days)

    # Month seasonality multipliers (India retail patterns)
    month_mult = {1: 1.1, 2: 0.9, 3: 1.0, 4: 0.85, 5: 0.9,
                  6: 0.85, 7: 0.8, 8: 0.9, 9: 0.95, 10: 1.3, 11: 1.5, 12: 1.4}
    for i, d in enumerate(dates):
        weights[i] *= month_mult.get(d.month, 1.0)
        # Weekend uplift
        if d.weekday() >= 5:
            weights[i] *= 1.25

    weights /= weights.sum()
    chosen_days = np.random.choice(day_range, size=n, replace=True, p=weights)
    return np.array([start + timedelta(days=int(d)) for d in chosen_days])


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  STEP 1 â€” STORES
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_stores(n_stores: int = 200) -> pd.DataFrame:
    print("Building stores...")
    rows = []
    store_id = 1
    for region, cities in REGIONS.items():
        per_city = max(1, n_stores // (len(REGIONS) * len(cities)))
        for city in cities:
            for _ in range(per_city):
                size_sqft = random.randint(1_000, 25_000)
                open_year  = random.randint(2010, 2021)
                open_date  = datetime(open_year, random.randint(1,12),
                                      random.randint(1,28))
                rows.append({
                    "store_id":     f"STR{store_id:04d}",
                    "store_name":   f"{city} {random.choice(STORE_TYPES)} {store_id}",
                    "store_type":   random.choice(STORE_TYPES),
                    "city":         city,
                    "state":        STATES_MAP[city],
                    "region":       region,
                    "store_size_sqft": size_sqft,
                    "opening_date": open_date.date(),
                    "is_active":    1,
                })
                store_id += 1
    df = pd.DataFrame(rows).head(n_stores)
    df.to_csv(PROCESSED_DIR / "stores.csv", index=False)
    print(f"  â†’ {len(df)} stores written.")
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  STEP 2 â€” PRODUCTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_products(n_products: int = 5_000) -> pd.DataFrame:
    print("Building products...")
    rows = []
    pid  = 1
    cats = list(CATEGORIES.keys())
    per_cat = n_products // len(cats)

    for cat in cats:
        sub_cats = CATEGORIES[cat]
        brand_list = BRANDS.get(cat, ["Generic"])
        for _ in range(per_cat):
            sub = random.choice(sub_cats)
            brand = random.choice(brand_list)
            cost  = round(random.uniform(50, 50_000), 2)
            margin_pct = random.uniform(0.08, 0.55)
            sell  = round(cost * (1 + margin_pct), 2)
            rows.append({
                "product_id":   f"PRD{pid:05d}",
                "product_name": f"{brand} {sub} {random.randint(100,9999)}",
                "category":     cat,
                "sub_category": sub,
                "brand":        brand,
                "cost_price":   cost,
                "selling_price": sell,
                "supplier":     f"Supplier_{random.randint(1,500):03d}",
            })
            pid += 1

    df = pd.DataFrame(rows)
    df.to_csv(PROCESSED_DIR / "products.csv", index=False)
    print(f"  â†’ {len(df)} products written.")
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  STEP 3 â€” CUSTOMERS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_customers(n_customers: int = 500_000) -> pd.DataFrame:
    print(f"Building {n_customers:,} customers...")
    all_cities = [c for cities in REGIONS.values() for c in cities]

    signup_dates = _sample_dates(n_customers, datetime(2016, 1, 1), datetime(2023, 12, 31))

    age_probs   = [0.18, 0.32, 0.25, 0.15, 0.10]
    inc_probs   = [0.15, 0.25, 0.30, 0.20, 0.10]
    gender_probs = [0.52, 0.45, 0.03]

    cities  = np.random.choice(all_cities, size=n_customers)
    ages    = np.random.choice(AGE_GROUPS, size=n_customers, p=age_probs)
    incomes = np.random.choice(INCOME_SEGS, size=n_customers, p=inc_probs)
    genders = np.random.choice(GENDERS, size=n_customers, p=gender_probs)

    df = pd.DataFrame({
        "customer_id":       [f"CUS{i+1:07d}" for i in range(n_customers)],
        "age_group":         ages,
        "gender":            genders,
        "city":              cities,
        "state":             [STATES_MAP.get(c, "Unknown") for c in cities],
        "income_segment":    incomes,
        "signup_date":       [d.date() for d in signup_dates],
        "customer_segment":  "Unassigned",    # will be filled by RFM later
    })
    df.to_csv(PROCESSED_DIR / "customers.csv", index=False)
    print(f"  â†’ {len(df):,} customers written.")
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  STEP 4 â€” TRANSACTIONS (core 2M table)
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_transactions(customers: pd.DataFrame,
                        products: pd.DataFrame,
                        stores: pd.DataFrame,
                        target: int = TARGET_TRANSACTIONS) -> pd.DataFrame:
    print(f"Building {target:,} transactions (this may take a minute)...")

    cust_ids  = customers["customer_id"].values
    prod_ids  = products["product_id"].values
    store_ids = stores["store_id"].values
    sell_prices = dict(zip(products["product_id"], products["selling_price"]))

    # Sample dates with seasonality
    dates = _sample_dates(target, DATE_START, DATE_END)

    # Assign customers (power-law: some customers buy much more)
    cust_weights = np.random.pareto(2.0, len(cust_ids)) + 1
    cust_weights /= cust_weights.sum()
    chosen_custs = np.random.choice(cust_ids, size=target, p=cust_weights)

    # Assign products (some products far more popular)
    prod_weights = np.random.pareto(1.5, len(prod_ids)) + 1
    prod_weights /= prod_weights.sum()
    chosen_prods = np.random.choice(prod_ids, size=target, p=prod_weights)

    # Random stores
    chosen_stores = np.random.choice(store_ids, size=target)

    # Quantities (mostly 1, sometimes up to 10)
    quantities = np.random.choice([1,1,1,1,2,2,3,4,5,10],
                                   size=target,
                                   p=[0.4,0.15,0.1,0.1,0.1,0.07,0.04,0.02,0.01,0.01])

    # Discounts
    disc_vals = [0.0, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    disc_probs= [0.35,0.20,0.12,0.12,0.08,0.05,0.04,0.02,0.01,0.01]
    discounts  = np.random.choice(disc_vals, size=target, p=disc_probs)

    # Payment methods
    pay_methods = np.random.choice(PAYMENT_METHODS, size=target)

    print("  Assembling DataFrame...")
    unit_prices = np.array([sell_prices[p] for p in tqdm(chosen_prods, desc="  Pricing")])
    total_amounts = np.round(unit_prices * quantities * (1 - discounts), 2)

    df = pd.DataFrame({
        "transaction_id":  [f"TXN{i+1:09d}" for i in range(target)],
        "customer_id":     chosen_custs,
        "store_id":        chosen_stores,
        "product_id":      chosen_prods,
        "transaction_date": [d.date() for d in dates],
        "quantity":        quantities,
        "unit_price":      np.round(unit_prices, 2),
        "discount":        discounts,
        "payment_method":  pay_methods,
        "total_amount":    total_amounts,
    })

    df.sort_values("transaction_date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(PROCESSED_DIR / "transactions.csv", index=False)
    print(f"  â†’ {len(df):,} transactions written.")
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  STEP 5 â€” INVENTORY (daily snapshots, sampled)
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_inventory(stores: pd.DataFrame,
                     products: pd.DataFrame,
                     transactions: pd.DataFrame,
                     sample_days: int = 60) -> pd.DataFrame:
    """
    Generates inventory snapshot records.
    Samples `sample_days` random dates Ã— all stores Ã— a product sample.
    """
    print(f"Building inventory snapshots ({sample_days} sample days)...")

    all_dates = pd.date_range(DATE_START, DATE_END, freq="D")
    sampled   = pd.DatetimeIndex(np.random.choice(all_dates, size=sample_days, replace=False))

    store_ids   = stores["store_id"].values
    prod_sample = np.random.choice(products["product_id"].values, size=500, replace=False)

    rows = []
    for d in tqdm(sampled, desc="  Inventory days"):
        day_str = d.date()
        day_sales = transactions[transactions["transaction_date"] == day_str]
        for sid in store_ids[:50]:   # keep row count manageable
            for pid in prod_sample[:20]:
                sold_qty = int(day_sales[(day_sales["store_id"]==sid) &
                                          (day_sales["product_id"]==pid)]["quantity"].sum())
                opening  = random.randint(50, 500)
                purchase = random.randint(0, 100) if opening < 100 else 0
                closing  = max(0, opening + purchase - sold_qty)
                rows.append({
                    "snapshot_date":    day_str,
                    "store_id":         sid,
                    "product_id":       pid,
                    "opening_stock":    opening,
                    "purchase_qty":     purchase,
                    "sales_qty":        sold_qty,
                    "closing_stock":    closing,
                    "stockout_flag":    int(closing == 0 and sold_qty > 0),
                })

    df = pd.DataFrame(rows)
    df.to_csv(PROCESSED_DIR / "inventory.csv", index=False)
    print(f"  â†’ {len(df):,} inventory records written.")
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  STEP 6 â€” MARKETING CAMPAIGNS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_marketing(customers: pd.DataFrame, n_interactions: int = 500_000) -> pd.DataFrame:
    print(f"Building {n_interactions:,} marketing interactions...")

    cust_sample = np.random.choice(customers["customer_id"].values,
                                    size=n_interactions, replace=True)
    campaigns   = np.random.choice(CAMPAIGN_NAMES, size=n_interactions)
    channels    = np.random.choice(CAMPAIGN_CHANNELS, size=n_interactions)
    dates       = _sample_dates(n_interactions, DATE_START, DATE_END)

    # Response rate varies by channel
    channel_response = {"Email": 0.12, "SMS": 0.18, "Social Media": 0.08,
                         "In-App": 0.22, "Push Notification": 0.15}
    responses = np.array([1 if random.random() < channel_response[ch] else 0
                           for ch in channels])

    spend_per_contact = np.round(np.random.uniform(0.5, 5.0, size=n_interactions), 2)

    df = pd.DataFrame({
        "campaign_interaction_id": [f"MKT{i+1:08d}" for i in range(n_interactions)],
        "customer_id":    cust_sample,
        "campaign_name":  campaigns,
        "channel":        channels,
        "campaign_date":  [d.date() for d in dates],
        "responded":      responses,
        "spend":          spend_per_contact,
    })
    df.to_csv(PROCESSED_DIR / "marketing_campaigns.csv", index=False)
    print(f"  â†’ {len(df):,} marketing records written.")
    return df


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
#  MAIN
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def main():
    print("=" * 60)
    print("  Retail Consumer Intelligence â€” Data Generation")
    print("=" * 60)

    stores   = build_stores(n_stores=200)
    products = build_products(n_products=5_000)
    customers= build_customers(n_customers=50_000)
    txns     = build_transactions(customers, products, stores,
                                   target=TARGET_TRANSACTIONS)
    build_inventory(stores, products, txns, sample_days=60)
    build_marketing(customers, n_interactions=100_000)

    print("\n" + "=" * 60)
    print("  Data generation complete!")
    print(f"  Output directory: {PROCESSED_DIR.resolve()}")
    print("=" * 60)

    # Summary
    summary = {
        "Table": ["customers", "products", "stores", "transactions",
                  "inventory", "marketing_campaigns"],
        "Records": [
            len(pd.read_csv(PROCESSED_DIR / "customers.csv")),
            len(pd.read_csv(PROCESSED_DIR / "products.csv")),
            len(pd.read_csv(PROCESSED_DIR / "stores.csv")),
            TARGET_TRANSACTIONS,
            "~varies",
            100_000,
        ],
    }
    print("\n  Table Summary:")
    for t, r in zip(summary["Table"], summary["Records"]):
        print(f"    {t:<25} {r:>15,}" if isinstance(r, int) else f"    {t:<25} {r:>15}")


if __name__ == "__main__":
    main()

