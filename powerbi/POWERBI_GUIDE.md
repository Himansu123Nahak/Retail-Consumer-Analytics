# Power BI Dashboard Guide
## Retail Consumer Intelligence Platform

> **Pre-requisite:** PostgreSQL is set up and loaded (`py setup_database.py` ran successfully).  
> **Tool:** Power BI Desktop (free) — download at https://powerbi.microsoft.com/desktop

---

## Part 1 — Connect to PostgreSQL

### Step 1: Open Power BI Desktop
- Click **Home → Get Data → More...**
- Search: `PostgreSQL`
- Select **PostgreSQL database** → Click **Connect**

### Step 2: Enter Connection Details
| Field | Value |
|---|---|
| Server | `localhost` |
| Database | `retail_analytics` |
| Data Connectivity mode | `Import` |

Click **OK** → Enter credentials:
- Username: `postgres`
- Password: *(your PostgreSQL password)*

### Step 3: Select Tables
In the Navigator, select all of the following:

**Dimension tables:**
- ✅ `dwh.dim_customer`
- ✅ `dwh.dim_date`
- ✅ `dwh.dim_product`
- ✅ `dwh.dim_store`

**Fact tables:**
- ✅ `dwh.fact_sales`
- ✅ `dwh.fact_inventory`
- ✅ `dwh.fact_marketing`

**Analytical views (optional but useful):**
- ✅ `analytics.vw_sales_summary`
- ✅ `analytics.vw_customer_rfm`

Click **Load**.

---

## Part 2 — Create Relationships (Model View)

Click the **Model** icon (left sidebar). Create these relationships:

| From (Many) | To (One) | Column |
|---|---|---|
| `fact_sales[date_key]` | `dim_date[date_key]` | date_key |
| `fact_sales[customer_sk]` | `dim_customer[customer_sk]` | customer_sk |
| `fact_sales[product_sk]` | `dim_product[product_sk]` | product_sk |
| `fact_sales[store_sk]` | `dim_store[store_sk]` | store_sk |
| `fact_inventory[date_key]` | `dim_date[date_key]` | date_key |
| `fact_inventory[product_sk]` | `dim_product[product_sk]` | product_sk |
| `fact_inventory[store_sk]` | `dim_store[store_sk]` | store_sk |
| `fact_marketing[date_key]` | `dim_date[date_key]` | date_key |
| `fact_marketing[customer_sk]` | `dim_customer[customer_sk]` | customer_sk |

---

## Part 3 — Create DAX Measures

Go to **Home → New Measure** for each measure below.  
Create a dedicated **Measures Table**: Home → Enter Data → name it `_Measures` → Load.

### Sales Measures
```dax
Total Revenue =
SUM(fact_sales[net_revenue])

Total Profit =
SUM(fact_sales[gross_profit])

Profit Margin % =
DIVIDE([Total Profit], [Total Revenue], 0) * 100

Total Orders =
COUNT(fact_sales[sale_sk])

Avg Order Value =
DIVIDE([Total Revenue], [Total Orders], 0)

Total Units Sold =
SUM(fact_sales[quantity])
```

### Customer Measures
```dax
Total Customers =
DISTINCTCOUNT(fact_sales[customer_sk])

Repeat Customers =
CALCULATE(
    DISTINCTCOUNT(fact_sales[customer_sk]),
    FILTER(
        VALUES(fact_sales[customer_sk]),
        CALCULATE(COUNT(fact_sales[sale_sk])) > 1
    )
)

Repeat Rate % =
DIVIDE([Repeat Customers], [Total Customers], 0) * 100
```

### Inventory Measures
```dax
Avg Closing Stock =
AVERAGE(fact_inventory[closing_stock])

Stockout Rate % =
DIVIDE(
    CALCULATE(COUNT(fact_inventory[inventory_sk]),
              fact_inventory[stockout_flag] = 1),
    COUNT(fact_inventory[inventory_sk]),
    0
) * 100
```

### Marketing Measures
```dax
Total Contacts =
COUNT(fact_marketing[marketing_sk])

Total Responses =
SUM(fact_marketing[responded])

Response Rate % =
DIVIDE([Total Responses], [Total Contacts], 0) * 100

Total Campaign Spend =
SUM(fact_marketing[spend])
```

---

## Part 4 — Build the Dashboard (6 Pages)

### 🔧 Global Settings (apply to ALL pages)
- Theme: **Modern** or **Executive** (View → Themes)
- Canvas size: **16:9**
- Background: Dark navy `#0D1B2A` or white `#FFFFFF`
- Font: **Segoe UI** throughout

---

### 📄 Page 1 — Executive Summary

**Page name:** `Executive Summary`

**Visuals to add:**

| Visual | Type | Fields | Position |
|---|---|---|---|
| Total Revenue | Card | `[Total Revenue]` | Top left |
| Total Profit | Card | `[Total Profit]` | Top |
| Profit Margin | Card | `[Profit Margin %]` | Top |
| Total Orders | Card | `[Total Orders]` | Top |
| Avg Order Value | Card | `[Avg Order Value]` | Top |
| Repeat Rate | Card | `[Repeat Rate %]` | Top right |
| Revenue Trend | Line Chart | dim_date[year_month] × [Total Revenue] | Centre |
| Revenue by Category | Donut Chart | dim_product[category] × [Total Revenue] | Bottom left |
| Revenue by Region | Bar Chart | dim_store[region] × [Total Revenue] | Bottom right |

**Slicers:**
- `dim_date[year]` — Year slicer (top right)

**Formatting tips:**
- Cards: large font (28–36pt), bold, with trend arrows
- Line chart: smooth lines, markers on, data labels off
- Donut: legend below, percentage labels

---

### 📄 Page 2 — Sales Analysis

**Page name:** `Sales Analysis`

| Visual | Type | Fields |
|---|---|---|
| Monthly Revenue | Line Chart | dim_date[month_name] × [Total Revenue] (by year) |
| Revenue by Category | Horizontal Bar | dim_product[category] × [Total Revenue] |
| Revenue by Sub-Category | Treemap | dim_product[sub_category] × [Total Revenue] |
| Discount Analysis | Clustered Bar | dim_product[category] × AVG(fact_sales[discount_pct]) |
| Payment Method | Pie Chart | fact_sales[payment_method] × [Total Orders] |
| Revenue by Store Type | Bar Chart | dim_store[store_type] × [Total Revenue] |

**Slicers:**
- `dim_date[year]`
- `dim_product[category]`

**Interactions:** Enable cross-filtering between all charts.

---

### 📄 Page 3 — Customer Insights

**Page name:** `Customer Insights`

| Visual | Type | Fields |
|---|---|---|
| Total Customers | Card | `[Total Customers]` |
| Repeat Rate % | Card | `[Repeat Rate %]` |
| Revenue by Age Group | Bar Chart | dim_customer[age_group] × [Total Revenue] |
| Revenue by Gender | Donut Chart | dim_customer[gender] × [Total Revenue] |
| Revenue by Income | Bar Chart | dim_customer[income_segment] × [Total Revenue] |
| RFM Segments | Bar Chart | analytics.vw_customer_rfm[segment] × COUNT |
| Top 10 Customers | Table | customer_name, [Total Revenue], [Total Orders] |

**Slicers:**
- `dim_customer[age_group]`
- `dim_customer[gender]`
- `dim_customer[income_segment]`

---

### 📄 Page 4 — Store & Geography

**Page name:** `Store & Geography`

| Visual | Type | Fields |
|---|---|---|
| Revenue by Region | Bar Chart | dim_store[region] × [Total Revenue] |
| Revenue by State | Horizontal Bar | dim_store[state] × [Total Revenue] (top 10) |
| Store Type Comparison | Clustered Bar | dim_store[store_type] × [Total Revenue], [Total Orders] |
| Map | Filled Map / Bubble Map | dim_store[state] × [Total Revenue] |
| Store Rankings | Table | store_name, city, region, [Total Revenue], Rank |

**Slicers:**
- `dim_store[region]`
- `dim_store[store_type]`

**Tip:** For the map, use dim_store[state] with Power BI's India state names — enable Map visual under Security settings if needed.

---

### 📄 Page 5 — Inventory

**Page name:** `Inventory`

| Visual | Type | Fields |
|---|---|---|
| Avg Closing Stock | Card | `[Avg Closing Stock]` |
| Stockout Rate % | Card | `[Stockout Rate %]` |
| Avg Stock by Category | Horizontal Bar | dim_product[category] × [Avg Closing Stock] |
| Stock Over Time | Line Chart | dim_date[month_name] × [Avg Closing Stock] |
| Slow Movers Table | Table | product_name, avg_closing_stock, sales_qty |

**Slicers:**
- `dim_store[store_name]`
- `dim_product[category]`

---

### 📄 Page 6 — Marketing

**Page name:** `Marketing`

| Visual | Type | Fields |
|---|---|---|
| Total Campaign Spend | Card | `[Total Campaign Spend]` |
| Total Contacts | Card | `[Total Contacts]` |
| Response Rate % | Card | `[Response Rate %]` |
| Response Rate by Channel | Bar Chart | dim_campaign[channel] × [Response Rate %] |
| Contacts vs Responses | Clustered Bar | dim_campaign[channel] × [Total Contacts], [Total Responses] |
| Campaign Rankings | Bar Chart | dim_campaign[campaign_name] × [Total Responses] |
| Spend by Channel | Donut Chart | dim_campaign[channel] × [Total Campaign Spend] |

**Slicers:**
- `dim_campaign[channel]`
- `dim_date[year]`

---

## Part 5 — Publish & Share

### Option A — Publish to Power BI Service (Online)
1. **Home → Publish**
2. Select workspace: **My workspace**
3. Visit: https://app.powerbi.com
4. Find your report → Share → Copy link

### Option B — Export as PDF
1. **File → Export → Export to PDF**
2. Includes all 6 pages as a PDF report

### Option C — Embed in GitHub README
1. Publish to Power BI Service
2. **File → Embed report → Website or portal**
3. Copy the iframe HTML or the share link
4. Add to README.md:
```markdown
[View Live Dashboard →](your-powerbi-link)
```

---

## Quick Reference — Page Summary

| Page | KPI Cards | Charts | Slicers |
|---|:---:|:---:|:---:|
| Executive Summary | 6 | 3 | 1 |
| Sales Analysis | 0 | 6 | 2 |
| Customer Insights | 2 | 5 | 3 |
| Store & Geography | 0 | 5 | 2 |
| Inventory | 2 | 3 | 2 |
| Marketing | 3 | 4 | 2 |
| **Total** | **13** | **26** | **12** |
