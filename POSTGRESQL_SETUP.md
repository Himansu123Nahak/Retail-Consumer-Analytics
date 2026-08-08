# PostgreSQL Setup Guide

## Step 1 — Download & Install PostgreSQL

1. Go to: **https://www.postgresql.org/download/windows/**
2. Download PostgreSQL 16 (Windows x86-64)
3. Run the installer — keep all defaults
4. Set a password for the `postgres` user — **write it down**
5. Keep default port: **5432**
6. After install, add PostgreSQL to PATH:
   - Search Windows → "Environment Variables"
   - Under System Variables → `Path` → Edit → Add:
     ```
     C:\Program Files\PostgreSQL\16\bin
     ```
7. Open a new PowerShell and verify:
   ```powershell
   psql --version
   ```

---

## Step 2 — Create the Database

```powershell
# Open psql as postgres user
psql -U postgres

# Inside psql, create the database
CREATE DATABASE retail_analytics;

# Confirm it was created
\l

# Exit psql
\q
```

---

## Step 3 — Configure the Project

Copy the `.env.example` file to `.env`:
```powershell
Copy-Item .env.example .env
```

Open `.env` and update your password:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_analytics
DB_USER=postgres
DB_PASSWORD=your_password_here   ← change this
```

---

## Step 4 — Run the Schema Script

```powershell
psql -U postgres -d retail_analytics -f sql/schema/00_create_database.sql
psql -U postgres -d retail_analytics -f sql/schema/01_dim_date.sql
psql -U postgres -d retail_analytics -f sql/schema/02_dim_tables.sql
psql -U postgres -d retail_analytics -f sql/schema/03_fact_tables.sql
```

---

## Step 5 — Load All Data

```powershell
$env:PYTHONIOENCODING="utf-8"
py python/01_data_ingestion/load_to_postgres.py
```

This will:
- Load all staging tables from CSV
- Populate all dimension tables (dim_customer, dim_product, etc.)
- Populate all fact tables (fact_sales, fact_inventory, fact_marketing)

---

## Step 6 — Verify the Load

```powershell
psql -U postgres -d retail_analytics -f sql/exploratory_analysis/01_quick_overview.sql
```

Expected output:
```
 table_name    | row_count
---------------+-----------
 dim_customer  |    50,000
 dim_date      |     3,653
 dim_product   |     5,000
 dim_store     |       200
 fact_marketing|   100,000
 fact_sales    |   200,000
```

---

## Step 7 — Create Analytical Views

```powershell
psql -U postgres -d retail_analytics -f sql/transformations/create_analytical_views.sql
```

---

## Step 8 — Connect Power BI

1. Open **Power BI Desktop**
2. **Home → Get Data → PostgreSQL database**
3. Server: `localhost`
4. Database: `retail_analytics`
5. Select **Import** mode
6. Load all `dwh.*` tables and `analytics.*` views
7. Follow `powerbi/POWERBI_GUIDE.md` to build the dashboard

---

## Step 9 — Run SQL Analytics in pgAdmin

After installing PostgreSQL, **pgAdmin 4** is included.
Open pgAdmin → connect to `retail_analytics` → open and run any file from the `sql/` folder.
