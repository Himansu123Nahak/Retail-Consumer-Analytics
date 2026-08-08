# Complete Setup Guide

## Quick Start — 5 Steps to Full Project

```
Step 1  → Generate data          (already done)
Step 2  → Install PostgreSQL     (run winget command below)
Step 3  → Load database          (run setup_database.py)
Step 4  → Open Excel workbook    (already built)
Step 5  → Connect Power BI       (follow POWERBI_GUIDE.md)
```

---

## Step 1 — Data is Already Generated ✅

All data is in `data/processed/`:

| File | Records |
|---|---|
| `transactions_clean.csv` | 200,000 |
| `customers_clean.csv` | 50,000 |
| `products_clean.csv` | 5,000 |
| `stores.csv` | 200 |
| `inventory_clean.csv` | 60,000 |
| `marketing_campaigns.csv` | 100,000 |

---

## Step 2 — Install PostgreSQL

Open PowerShell and run:

```powershell
winget install --id PostgreSQL.PostgreSQL.17 -e --accept-package-agreements --accept-source-agreements
```

> **When it finishes:** A UAC popup will appear — click **Yes** to allow installation.  
> Set a password for the `postgres` user when prompted — **remember it**.

Also install pgAdmin (SQL query tool):
```powershell
winget install --id PostgreSQL.pgAdmin --accept-package-agreements --accept-source-agreements
```

---

## Step 3 — Configure the .env File

```powershell
Copy-Item .env.example .env
```

Open `.env` and set your PostgreSQL password:
```
DB_PASSWORD=your_password_here
```

---

## Step 4 — Load the Database (One Command)

```powershell
$env:PYTHONIOENCODING="utf-8"
py setup_database.py
```

This runs everything automatically:
- Creates `retail_analytics` database
- Creates star schema (dims + facts)
- Loads all CSVs into PostgreSQL
- Creates analytical views

**Expected output:**
```
  Table                        Rows
  dim_customer               50,000
  dim_product                 5,000
  dim_store                     200
  dim_date                    3,653
  fact_sales                200,000
  fact_inventory             60,000
  fact_marketing            100,000
```

---

## Step 5 — Open the Excel Workbook ✅

File is already built:
```
excel/Retail_Analysis.xlsx
```

Contains 6 sheets:
- **Executive KPIs** — headline numbers with color-coded KPI cards
- **Sales by Month** — monthly revenue table + line chart
- **Sales by Category** — category breakdown + bar chart
- **Customer Analysis** — age/gender/income segments + chart
- **Store Performance** — top 50 stores ranked by revenue
- **KPI Validation** — reconciliation across Python, SQL, Power BI

---

## Step 6 — Build Power BI Dashboard

1. Install Power BI Desktop (free): https://powerbi.microsoft.com/desktop
2. Open Power BI → **Get Data → PostgreSQL database**
3. Server: `localhost` | Database: `retail_analytics`
4. Load all `dwh.*` tables
5. Follow `powerbi/POWERBI_GUIDE.md` step by step

---

## Step 7 — Run All EDA Charts

```powershell
$env:PYTHONIOENCODING="utf-8"
py run_pipeline.py
```

Generates 23 charts in `python/03_eda/charts/` covering:
- Sales trends (monthly, annual, day-of-week)
- Customer demographics (age, gender, income, region)
- Product performance (category, brand, margin)
- Store analysis (region, store type, size vs revenue)

---

## Step 8 — Set Up Git & GitHub

Install Git:
```powershell
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements
```

After installation, open a **new** PowerShell window:
```powershell
cd "C:\Users\himan\OneDrive\Desktop\project\Retail-Consumer-Analytics"
git init
git add .
git commit -m "Initial commit: Retail Consumer Intelligence Platform"
```

Push to GitHub:
1. Create a new repo on github.com
2. Copy the remote URL
3. Run:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/Retail-Consumer-Analytics.git
git branch -M main
git push -u origin main
```

---

## Project Structure at a Glance

```
Retail-Consumer-Analytics/
├── run_pipeline.py          ← Run all Python analytics
├── setup_database.py        ← One-command DB setup
├── SETUP.md                 ← This file
├── POSTGRESQL_SETUP.md      ← Detailed PostgreSQL guide
├── README.md                ← Project overview
├── requirements.txt
├── .gitignore
│
├── data/processed/          ← All clean CSVs (generated)
├── python/
│   ├── 00_data_generation/  ← augment_to_scale.py
│   ├── 01_data_ingestion/   ← load + profile scripts
│   ├── 02_data_cleaning/    ← 6 cleaners + quality report
│   ├── 03_eda/              ← 4 EDA scripts → 23 charts
│   ├── 04_customer_analytics/ ← RFM + CLV analysis
│   ├── 07_statistical_analysis/ ← correlations
│   └── build_excel.py       ← Excel workbook generator
│
├── sql/
│   ├── schema/              ← Star schema DDL (4 files)
│   ├── staging/             ← CSV load + validations
│   ├── transformations/     ← Dim/fact populate + views
│   ├── sales_analysis/      ← 7 sales SQL queries
│   ├── customer_analysis/   ← 4 customer SQL queries
│   ├── inventory_analysis/  ← Stockout analysis
│   └── marketing_analysis/  ← Campaign performance
│
├── excel/
│   └── Retail_Analysis.xlsx ← 6-sheet workbook (built)
│
├── powerbi/
│   └── POWERBI_GUIDE.md     ← Dashboard build guide
│
└── documentation/
    ├── business_requirements.md
    ├── data_dictionary.md
    ├── methodology.md
    ├── KPIs.md
    ├── insights.md          ← Real findings from data
    └── recommendations.md
```

---

## Key Business Findings

| Metric | Value |
|---|---|
| Total Revenue | **₹873 Cr** |
| Total Orders | **2,00,000** |
| Avg Order Value | **₹43,659** |
| Unique Customers | **46,981** |
| Repeat Customer Rate | **84.3%** |
| Top Category | **Groceries** (₹143.8 Cr) |
| Biggest Opportunity | **24,447 "At Risk" customers** — ₹593 Cr revenue at risk |
