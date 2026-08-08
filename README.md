<div align="center">

<img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge" />
<img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/PostgreSQL-17-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" />
<img src="https://img.shields.io/badge/Excel-Workbook-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white" />
<img src="https://img.shields.io/badge/SQL-27%20Queries-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" />

# 🛒 Retail Consumer Intelligence & Business Analytics Platform

### *"How can a retail company use customer, transaction, product, store, and sales data to increase revenue, improve retention, optimize inventory, and make better business decisions?"*

<br/>

| 📊 200,000 Transactions | 👥 50,000 Customers | 📦 5,000 Products | 🏪 200 Stores | 📅 2021 – 2024 |
|:---:|:---:|:---:|:---:|:---:|

<br/>

</div>

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Key Business Findings](#-key-business-findings)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Analytics Modules](#-analytics-modules)
- [EDA Charts](#-eda-charts-28-total)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Excel Workbook](#-excel-workbook)
- [Database Schema](#-database-schema-star-schema)
- [Setup](#-quick-setup)
- [Author](#-author)

---

## 🎯 Project Overview

An **end-to-end retail analytics platform** simulating a real-world business intelligence project for a pan-India retail chain. Built to demonstrate strong Data Analyst skills across the complete analytics lifecycle:

```
Raw Data → ETL → Data Quality → PostgreSQL DWH → SQL Analytics
                                                      ↓
                                          Python EDA + RFM + CLV
                                                      ↓
                                         Excel KPI Workbook
                                                      ↓
                                         Power BI Dashboard
                                                      ↓
                                    Business Insights + Recommendations
```

> **Domain:** Retail Consumer Analytics  
> **Industry:** Indian Retail (modelled on Olist e-commerce patterns)  
> **Scale:** ~415,000 total records across 6 domain tables

---

## 📈 Key Business Findings

<div align="center">

| KPI | Value | Insight |
|:---|:---:|:---|
| 💰 **Total Revenue** | ₹873 Cr | Stable growth 2021→2024 |
| 📦 **Total Orders** | 2,00,000 | Avg 54K orders/year |
| 🧾 **Avg Order Value** | ₹43,659 | High-ticket categories drive this |
| 👥 **Unique Customers** | 46,981 | 84.3% are repeat buyers |
| 🔁 **Repeat Rate** | **84.3%** | Very strong customer loyalty |
| 🏆 **Top Category** | Groceries | ₹143.8 Cr revenue |
| ⚠️ **At Risk Customers** | 24,447 | ₹593 Cr revenue at risk |
| 📊 **Profit Margin** | ~24% | Category-level variation |

</div>

### 🔍 RFM Customer Segments

| Segment | Customers | Avg Spend | Revenue | Action |
|---|:---:|:---:|:---:|:---|
| 🔴 **At Risk** | 24,447 | ₹2.4L | ₹593 Cr | Win-back campaigns |
| 🟡 **Need Attention** | 17,575 | ₹1.3L | ₹235 Cr | Re-engagement offers |
| ⚫ **Lost Customers** | 4,950 | ₹70K | ₹34 Cr | Last-chance discount |
| 🟢 **Potential Loyalists** | 7 | ₹73.8L | ₹5.2 Cr | Loyalty program |
| 🥇 **Champions** | 1 | ₹2.86 Cr | ₹2.9 Cr | VIP treatment |

> **Biggest opportunity:** Re-engaging 24,447 "At Risk" customers could recover up to **₹593 Cr** in revenue.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   DATA SOURCES                          │
│   Synthetic retail data (transactions, customers,       │
│   products, stores, inventory, marketing)               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              PYTHON ETL PIPELINE                        │
│   augment_to_scale.py  →  clean_*.py  →  run_pipeline  │
│   Data Quality Report: 100% retention, 0 nulls          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           POSTGRESQL STAR SCHEMA (retail_analytics)     │
│                                                         │
│   dim_customer   dim_product   dim_store   dim_date     │
│              ↘       ↓       ↙                          │
│                 fact_sales                              │
│              ↗       ↑       ↖                          │
│   fact_inventory         fact_marketing                 │
│                                                         │
│   + 5 Analytical Views (analytics.*)                    │
└──────────┬────────────────────┬────────────────────────-┘
           │                    │
      ┌────▼─────┐         ┌────▼──────┐
      │  SQL     │         │  Python   │
      │ Analytics│         │ Analytics │
      │ 27 files │         │ RFM + CLV │
      └────┬─────┘         └────┬──────┘
           │                    │
           └──────────┬─────────┘
                      │
           ┌──────────▼─────────┐
           │   REPORTING LAYER  │
           │  Excel  │  Power BI│
           └────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---|:---:|:---|
| **Language** | Python 3.13 | ETL, EDA, analytics, automation |
| **Data Wrangling** | Pandas · NumPy | Cleaning, aggregation, segmentation |
| **Visualisation** | Matplotlib · Seaborn | 28 EDA charts |
| **Excel Automation** | openpyxl | Programmatic 6-sheet workbook |
| **Database** | PostgreSQL 17 | Star schema data warehouse |
| **SQL** | Standard SQL | JOINs, GROUP BY, HAVING, CASE, subqueries |
| **BI** | Power BI Desktop | 6-page interactive dashboard |
| **DAX** | Basic DAX | SUM, DIVIDE, DISTINCTCOUNT, IF |
| **Version Control** | Git · GitHub | Source control |
| **Reporting** | Markdown · HTML | Documentation + browser report |

---

## 📁 Project Structure

```
Retail-Consumer-Analytics/
│
├── 📄 README.md                     ← You are here
├── 📄 SETUP.md                      ← Complete setup guide
├── 📄 POSTGRESQL_SETUP.md           ← Database setup steps
├── 📄 requirements.txt
├── 📄 .gitignore
│
├── 🚀 run_pipeline.py               ← Run all Python analytics
├── 🗄️  setup_database.py            ← One-command DB setup
├── 📤 push_to_github_api.py         ← GitHub upload utility
│
├── 📂 data/processed/               ← Clean CSVs (generated)
│   ├── stores.csv                   (200 rows)
│   ├── products_clean.csv           (5,000 rows)
│   ├── rfm_segment_summary.csv      (6 segments)
│   ├── master_quality_report.csv
│   └── customer_clv.csv
│
├── 📂 python/
│   ├── 00_data_generation/          ← augment_to_scale.py
│   ├── 01_data_ingestion/           ← load + profiling scripts
│   ├── 02_data_cleaning/            ← 6 domain cleaners
│   ├── 03_eda/                      ← 5 EDA scripts → 28 charts
│   ├── 04_customer_analytics/       ← RFM + CLV analysis
│   ├── 07_statistical_analysis/     ← Correlation analysis
│   ├── build_excel.py               ← Excel workbook builder
│   └── build_html_report.py         ← HTML summary report
│
├── 📂 sql/
│   ├── schema/                      ← Star schema DDL (4 files)
│   ├── staging/                     ← CSV load + validations
│   ├── transformations/             ← Dims, facts, views
│   ├── sales_analysis/              ← 8 sales queries
│   ├── customer_analysis/           ← 5 customer queries
│   ├── product_analysis/            ← Product performance
│   ├── inventory_analysis/          ← Stockout analysis
│   └── marketing_analysis/          ← Campaign performance
│
├── 📂 excel/
│   └── Retail_Analysis.xlsx         ← 6-sheet workbook ✅
│
├── 📂 powerbi/
│   └── POWERBI_GUIDE.md             ← Full dashboard build guide
│
└── 📂 documentation/
    ├── business_requirements.md
    ├── data_dictionary.md
    ├── methodology.md
    ├── KPIs.md
    ├── insights.md                  ← Real findings from data
    └── recommendations.md
```

---

## 📊 Analytics Modules

### Module 1 — Executive Sales Analytics
> SQL + Power BI

- Total revenue ₹873 Cr, profit margin ~24%
- Monthly & annual revenue trends (2021–2024)
- Revenue by category, region, store type
- Discount impact analysis
- Top 10 products and stores

### Module 2 — Customer Analytics
> SQL + Python + Power BI

- **84.3% repeat customer rate** (39,615 of 46,981)
- Revenue by age group, gender, income segment
- New vs returning customer split
- Top customers by lifetime value

### Module 3 — RFM Segmentation
> Python (Pandas)

- Recency × Frequency × Monetary scoring
- 6 customer tiers: Champions → Lost Customers
- Segment-level revenue and avg spend
- Actionable re-engagement strategy per segment

### Module 4 — Product Analytics
> SQL + Python

- Revenue and units by category & sub-category
- Profit margin by category (Electronics highest)
- Top 10 products and brands
- High-revenue, low-margin flag for pricing review

### Module 5 — Store & Geography Analytics
> SQL + Power BI

- Revenue by region, state, city
- Store type performance (Flagship vs Express vs Online)
- Store size vs revenue correlation
- Top 50 stores ranked table

### Module 6 — Inventory Analytics
> SQL

- Avg closing stock by product category
- Stockout rate analysis
- Slow-moving vs fast-moving products

### Module 7 — Marketing Analytics
> SQL + Python EDA

- Campaign response rate by channel
- In-App (22%) vs Social Media (8%) gap
- Contacts vs responses by channel
- Top performing campaigns by name

---

## 📉 EDA Charts (28 Total)

<details>
<summary><b>📈 Sales Analysis (6 charts)</b></summary>

| Chart | Description |
|---|---|
| Monthly Revenue Trend | Line chart 2021–2024 |
| Annual Revenue | Bar chart by year |
| Revenue by Day of Week | Weekend uplift analysis |
| Payment Method Split | Pie chart |
| Discount Distribution | Histogram |
| Order Value Distribution | Histogram |

</details>

<details>
<summary><b>👥 Customer Analysis (7 charts)</b></summary>

| Chart | Description |
|---|---|
| Customer Signups by Year | New customers trend |
| Age Distribution | Histogram |
| Gender Split | Bar chart |
| Income Segment | Bar chart by revenue |
| Top 10 States by Customers | Horizontal bar |
| Orders per Customer | Distribution |
| Revenue by Age Group | Bar chart |

</details>

<details>
<summary><b>📦 Product Analysis (5 charts)</b></summary>

| Chart | Description |
|---|---|
| Revenue by Category | Horizontal bar |
| Units Sold by Category | Bar chart |
| Top 10 Products by Revenue | Bar chart |
| Margin by Category | Bar chart |
| Top 10 Brands | Horizontal bar |

</details>

<details>
<summary><b>🏪 Store & Geography (5 charts)</b></summary>

| Chart | Description |
|---|---|
| Revenue by Region | Bar chart |
| Top 10 Stores | Horizontal bar |
| Revenue by Store Type | Bar chart |
| Top 10 States by Revenue | Horizontal bar |
| Store Size vs Revenue | Scatter plot |

</details>

<details>
<summary><b>📦 Inventory & Marketing (5 charts)</b></summary>

| Chart | Description |
|---|---|
| Avg Stock by Category | Horizontal bar |
| Stock Level Distribution | Histogram |
| Response Rate by Channel | Bar chart (green/red coded) |
| Contacts vs Responses | Grouped bar chart |
| Responses by Campaign | Horizontal bar |

</details>

---

## 📊 Power BI Dashboard

> 6-page interactive dashboard connecting to `retail_analytics` PostgreSQL DB.

| Page | Title | Key Visuals |
|:---:|:---|:---|
| 1 | **Executive Summary** | Revenue KPI cards, YoY trend, profit gauge, top 5 category pie |
| 2 | **Sales Analysis** | Monthly line chart, category bar, region map, payment split |
| 3 | **Customer Insights** | RFM segment bar, age/gender/income charts, repeat rate card |
| 4 | **Store & Geography** | Map by city, store type bar, store rankings table |
| 5 | **Inventory** | Stockout rate card, category stockout bar, slow-movers table |
| 6 | **Marketing** | Response rate by channel, contacts vs responses, campaign ranking |

### Key DAX Measures
```dax
Total Revenue    = SUM(fact_sales[net_revenue])
Total Profit     = SUM(fact_sales[gross_profit])
Profit Margin %  = DIVIDE([Total Profit], [Total Revenue]) * 100
Avg Order Value  = DIVIDE([Total Revenue], [Total Orders])
Repeat Rate %    = DIVIDE([Repeat Customers], [Total Customers]) * 100
Response Rate %  = DIVIDE([Total Responses], [Total Contacts]) * 100
```

**➡️ Full step-by-step guide:** [`powerbi/POWERBI_GUIDE.md`](powerbi/POWERBI_GUIDE.md)

---

## 📋 Excel Workbook

6-sheet formatted workbook built with `openpyxl` using real data:

| Sheet | Contents |
|---|---|
| **Executive KPIs** | 8 color-coded KPI cards + revenue by year table |
| **Sales by Month** | 48-month revenue table + line chart |
| **Sales by Category** | Category revenue, profit, margin + bar chart |
| **Customer Analysis** | Age, gender, income segment tables + chart |
| **Store Performance** | Top 50 stores ranked by revenue |
| **KPI Validation** | Python vs SQL vs Excel vs Power BI reconciliation |

**File:** [`excel/Retail_Analysis.xlsx`](excel/Retail_Analysis.xlsx)

---

## 🗄️ Database Schema (Star Schema)

```sql
              ┌─────────────┐
              │  dim_date   │
              └──────┬──────┘
                     │
┌──────────────┐     │     ┌──────────────┐
│ dim_customer │     │     │ dim_product  │
└──────┬───────┘     │     └───────┬──────┘
       │             ▼             │
       └──────► fact_sales ◄───────┘
                     ▲
       ┌─────────────┘
       │
┌──────┴───────┐
│  dim_store   │
└──────────────┘

fact_inventory  ←── dim_store + dim_product + dim_date
fact_marketing  ←── dim_customer + dim_campaign + dim_date
```

**Tables:** 4 dimensions · 3 facts · 5 analytical views  
**Schema file:** [`sql/schema/`](sql/schema/)

---

## ⚡ Quick Setup

```powershell
# 1. Clone
git clone https://github.com/Himansu123Nahak/Retail-Consumer-Analytics.git
cd Retail-Consumer-Analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run full analytics pipeline
py run_pipeline.py

# 4. Build Excel workbook
py python/build_excel.py

# 5. Build HTML summary report
py python/build_html_report.py

# 6. Setup PostgreSQL database
Copy-Item .env.example .env      # add your DB_PASSWORD
py setup_database.py

# 7. Open Power BI → connect to retail_analytics
#    Follow: powerbi/POWERBI_GUIDE.md
```

Full instructions: [`SETUP.md`](SETUP.md)

---

## 📦 Requirements

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
openpyxl>=3.1
psycopg2-binary>=2.9
python-dotenv>=1.0
requests>=2.31
rich>=13.0
tqdm>=4.65
```

Install: `pip install -r requirements.txt`

---

## 👤 Author

<div align="center">

**Himanshu Nahak**

Data Analyst | Business Intelligence | Python · SQL · Power BI · Excel

[![GitHub](https://img.shields.io/badge/GitHub-Himansu123Nahak-181717?style=for-the-badge&logo=github)](https://github.com/Himansu123Nahak)

</div>

---

<div align="center">

⭐ **If this project helped you, please give it a star!** ⭐

*Built with Python, SQL, Excel, Power BI — and a lot of ☕*

</div>
