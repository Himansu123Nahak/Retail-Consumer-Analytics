# Methodology

## Overview

This project follows a standard end-to-end analytics lifecycle:

```
Raw Data → Cleaning → SQL Database → Analysis → Visualisation → Insights
```

## Step 1 — Data Generation

Synthetic retail data was generated using Python (`augment_to_scale.py`) to simulate a realistic retail business operating across India from 2021 to 2024.

| Table | Records |
|---|---|
| Customers | 50,000 |
| Products | 5,000 |
| Stores | 200 |
| Transactions | 200,000 |
| Inventory snapshots | 60,000 |
| Marketing interactions | 100,000 |

Realistic patterns built in:
- Seasonal sales peaks (October–December: Diwali, Christmas)
- Weekend uplift (~25% higher sales)
- Power-law customer purchase distribution (some customers buy far more)
- Regional distribution across 5 regions and 25 cities

## Step 2 — Data Cleaning

Each table was cleaned using Python (`02_data_cleaning/`):

| Check | Description |
|---|---|
| Duplicate IDs | Removed duplicate primary keys |
| Null required fields | Flagged and removed missing transaction/customer/product IDs |
| Date range validation | Transactions must fall within 2021–2024 |
| Price validation | Unit price and cost must be positive |
| Discount validation | Discount must be between 0 and 1 (0–100%) |
| Amount reconciliation | `total_amount` verified against `qty × price × (1-discount)` |

**Result: 100% data retained — all 200,000 transactions passed quality checks.**

## Step 3 — SQL Data Model

A star schema was designed in PostgreSQL:

- **4 Dimension tables**: dim_customer, dim_product, dim_store, dim_date
- **3 Fact tables**: fact_sales, fact_inventory, fact_marketing
- Dimension keys used as foreign keys in fact tables

This model allows fast aggregation queries across any combination of dimensions.

## Step 4 — SQL Analytics

Business questions were answered using SQL queries organised by domain:

- **Sales**: Revenue trends, category performance, regional breakdown, store rankings
- **Customers**: New vs repeat, demographic segments, top customers
- **Inventory**: Stockout rates, slow-moving products
- **Marketing**: Channel response rates, campaign performance

## Step 5 — Python EDA

Exploratory Data Analysis charts were produced using `matplotlib` and `seaborn` to visually confirm patterns in the data before building the final dashboard.

## Step 6 — Customer Analytics (Python)

- **RFM Analysis**: Customers scored 1-5 on Recency, Frequency, Monetary. Total score used to assign segments: Champions, Loyal, Potential Loyalists, At Risk, Need Attention, Lost.
- **CLV Analysis**: Historical Customer Lifetime Value calculated as total spend per customer. Customers classified into High/Mid/Low/Very Low value tiers.

## Step 7 — Excel Workbook

Key KPIs independently calculated in Excel using Pivot Tables and SUMIF/COUNTIF formulas. Results compared against SQL and Power BI to confirm consistency.

## Step 8 — Power BI Dashboard

Six-page interactive dashboard built on top of the PostgreSQL star schema with basic DAX measures for all KPIs. Slicers allow filtering by year, category, region, and store.
