# Retail Consumer Intelligence & Business Analytics Platform

> **"How can a retail company use customer, transaction, product, store, and sales data to increase revenue, improve customer retention, optimize inventory, and make better business decisions?"**

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?logo=powerbi)
![Excel](https://img.shields.io/badge/Excel-Workbook-217346?logo=microsoftexcel)

---

## Project Overview

An **end-to-end retail analytics platform** demonstrating Data Analyst competencies across the full analytics lifecycle — from data generation and ETL to SQL analytics, Python EDA, customer segmentation, Excel reporting, and Power BI dashboards.

| Dimension | Details |
|---|---|
| **Data** | Synthetic retail data modelled on Indian retail (2021–2024) |
| **Scale** | 200,000 transactions · 50,000 customers · 5,000 products · 200 stores |
| **Database** | PostgreSQL 17 — Star Schema (4 dims, 3 facts, 5 analytical views) |
| **Tools** | Python · SQL · Excel · Power BI |

---

## Key Business Findings

| KPI | Value |
|---|---|
| **Total Revenue** | ₹873 Cr |
| **Total Orders** | 2,00,000 |
| **Average Order Value** | ₹43,659 |
| **Unique Customers** | 46,981 |
| **Repeat Customer Rate** | **84.3%** |
| **Top Revenue Category** | Groceries (₹143.8 Cr) |
| **Revenue Growth (2021→2024)** | +1.4% YoY |
| **Biggest Opportunity** | 24,447 "At Risk" customers — ₹593 Cr revenue at risk |

> Full findings: [`documentation/insights.md`](documentation/insights.md)

---

## Architecture

```
  Synthetic Data Generation (Python)
             │
             ▼
  Python ETL & Data Cleaning
  [clean_transactions / customers / products / stores / inventory]
             │
             ▼
  Data Quality Report ─── 100% retention across all 6 tables
             │
             ▼
  PostgreSQL Star Schema (retail_analytics)
  ┌──────────────────────────────────────────┐
  │  dim_date  dim_customer  dim_product      │
  │  dim_store  dim_campaign                  │
  │  fact_sales  fact_inventory               │
  │  fact_marketing                           │
  └──────────────────────────────────────────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
  SQL      Python    Excel
Analytics  EDA+RFM   KPIs
    └────────┼────────┘
             ▼
        Power BI (6-Page Dashboard)
             │
             ▼
    Business Insights & Recommendations
```

---

## Technology Stack

| Area | Technology | Usage |
|---|---|---|
| Language | Python 3.13 | ETL, EDA, analytics |
| Data Manipulation | Pandas, NumPy | Cleaning, aggregation, RFM |
| Visualisation | Matplotlib, Seaborn | 23 EDA charts |
| Database | PostgreSQL 17 | Star schema data warehouse |
| SQL | Standard SQL | JOINs, GROUP BY, CASE, HAVING |
| Business Reporting | Excel (openpyxl) | 6-sheet workbook with charts |
| BI Dashboard | Power BI Desktop | 6-page interactive dashboard |
| DAX | Basic DAX | SUM, DIVIDE, DISTINCTCOUNT |
| Version Control | Git / GitHub | Source code management |
| Documentation | Markdown | All project docs |

---

## Project Structure

```
Retail-Consumer-Analytics/
│
├── run_pipeline.py              ← Run all Python analytics
├── setup_database.py            ← One-command DB setup
├── build_excel.py               ← (moved to python/)
├── SETUP.md                     ← Complete setup guide
├── POSTGRESQL_SETUP.md          ← PostgreSQL setup details
├── requirements.txt
├── .gitignore
│
├── data/processed/              ← All clean CSVs (generated)
│   ├── transactions_clean.csv   (200,000 rows)
│   ├── customers_clean.csv      (50,000 rows)
│   ├── products_clean.csv       (5,000 rows)
│   ├── stores.csv               (200 rows)
│   ├── inventory_clean.csv      (60,000 rows)
│   ├── marketing_campaigns.csv  (100,000 rows)
│   ├── rfm_scores.csv           (RFM per customer)
│   ├── customer_clv.csv         (CLV tiers)
│   └── master_quality_report.csv
│
├── python/
│   ├── 00_data_generation/      ← augment_to_scale.py
│   ├── 01_data_ingestion/       ← load_raw_data, load_to_postgres
│   ├── 02_data_cleaning/        ← 6 cleaners + quality report
│   ├── 03_eda/                  ← 4 EDA scripts → 23 charts
│   ├── 04_customer_analytics/   ← RFM + CLV analysis
│   ├── 07_statistical_analysis/ ← correlations
│   └── build_excel.py           ← Excel workbook generator
│
├── sql/
│   ├── schema/                  ← Star schema DDL
│   ├── staging/                 ← CSV load + validation
│   ├── transformations/         ← Dim/fact + analytical views
│   ├── sales_analysis/          ← 7 sales queries
│   ├── customer_analysis/       ← 4 customer queries
│   ├── inventory_analysis/      ← Stockout analysis
│   ├── marketing_analysis/      ← Campaign performance
│   └── exploratory_analysis/    ← Quick sanity check queries
│
├── excel/
│   └── Retail_Analysis.xlsx     ← 6-sheet workbook (built)
│
├── powerbi/
│   └── POWERBI_GUIDE.md         ← Step-by-step dashboard guide
│
└── documentation/
    ├── business_requirements.md
    ├── data_dictionary.md
    ├── methodology.md
    ├── KPIs.md
    ├── insights.md              ← Real findings from the data
    └── recommendations.md
```

---

## Analytical Modules

### 1 — Sales Analytics (SQL + Power BI)
- Total revenue, profit, profit margin
- Monthly and annual revenue trends (2021–2024)
- Revenue by category, region, store type
- Discount impact analysis
- Top 10 products and stores

### 2 — Customer Analytics (SQL + Python)
- New vs repeat customer analysis (84.3% repeat rate)
- Revenue by age group, gender, income segment
- RFM segmentation — 6 customer tiers
- Historical Customer Lifetime Value (CLV) — 4 value tiers

### 3 — Product Analytics (SQL + Python)
- Revenue and units by category
- Profit margin by category
- Top 10 products and brands by revenue
- Category sub-category drill-down

### 4 — Store & Geography Analytics (SQL + Power BI)
- Revenue by region, state, city
- Store type performance comparison
- Store size vs revenue correlation
- Top 50 stores ranked table

### 5 — Inventory Analytics (SQL)
- Stockout rate by product and category
- Slow-moving product identification
- Average closing stock analysis

### 6 — Marketing Analytics (SQL)
- Campaign response rate by channel
- Campaign performance by name
- Cost per contact and total spend analysis

---

## Setup (Quick Start)

```powershell
# 0. Clone the repo
git clone https://github.com/Himansu123Nahak/Retail-Consumer-Analytics.git
cd Retail-Consumer-Analytics

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Data is already generated — or regenerate:
py python/00_data_generation/augment_to_scale.py

# 3. Run full cleaning + EDA + analytics pipeline
py run_pipeline.py

# 4. Build Excel workbook
py python/build_excel.py

# 5. Build HTML summary report (open in browser)
py python/build_html_report.py

# 6. Install PostgreSQL (via winget), then:
Copy-Item .env.example .env   # set DB_PASSWORD
py setup_database.py

# 7. Open Power BI → follow powerbi/POWERBI_GUIDE.md

```

Full instructions: [`SETUP.md`](SETUP.md)

---

## Charts Generated

| Module | Charts |
|---|---|
| Sales EDA | Monthly trend, annual revenue, day-of-week, payment method, discount distribution, order value |
| Customer EDA | Signups by year, age group, gender split, income segment, top states, orders per customer, revenue by age |
| Product EDA | Revenue by category, units by category, top 10 products, margin by category, top 10 brands |
| Store EDA | Revenue by region, top 10 stores, store type, top 10 states, size vs revenue scatter |
| Customer Analytics | RFM segments bar, revenue by segment, CLV tier revenue |
| Statistical | Discount vs quantity scatter, store size vs revenue, revenue by day of week |

---

## Author

**Himanshu Nahak**  
Data Analyst  
[GitHub](https://github.com/Himansu123Nahak) | [LinkedIn](https://linkedin.com)
