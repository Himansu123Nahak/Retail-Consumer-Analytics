# Power BI — Dashboard Guide

## Connection

Connect Power BI Desktop to PostgreSQL:

1. **Get Data → Database → PostgreSQL Database**
2. Server: `localhost`
3. Database: `retail_analytics`
4. Import tables from the `dwh` schema:
   - `dim_date`, `dim_customer`, `dim_product`, `dim_store`, `dim_campaign`
   - `fact_sales`, `fact_inventory`, `fact_marketing`

---

## Data Model (Relationships)

Set up the following relationships in **Model View**:

| From | To | Column |
|---|---|---|
| fact_sales → dim_date | date_key → date_key | Many to One |
| fact_sales → dim_customer | customer_sk → customer_sk | Many to One |
| fact_sales → dim_product | product_sk → product_sk | Many to One |
| fact_sales → dim_store | store_sk → store_sk | Many to One |
| fact_inventory → dim_date | date_key → date_key | Many to One |
| fact_inventory → dim_store | store_sk → store_sk | Many to One |
| fact_inventory → dim_product | product_sk → product_sk | Many to One |
| fact_marketing → dim_date | date_key → date_key | Many to One |
| fact_marketing → dim_customer | customer_sk → customer_sk | Many to One |
| fact_marketing → dim_campaign | campaign_sk → campaign_sk | Many to One |

---

## DAX Measures (Basic)

Create these measures in a dedicated `_Measures` table:

```dax
Total Revenue =
    SUM(fact_sales[net_revenue])

Total Profit =
    SUM(fact_sales[gross_profit])

Total Orders =
    COUNT(fact_sales[sale_sk])

Total Units Sold =
    SUM(fact_sales[quantity])

Profit Margin % =
    DIVIDE([Total Profit], [Total Revenue], 0) * 100

Average Order Value =
    DIVIDE([Total Revenue], [Total Orders], 0)

Total Customers =
    DISTINCTCOUNT(fact_sales[customer_sk])

Revenue per Customer =
    DIVIDE([Total Revenue], [Total Customers], 0)

Total Campaign Spend =
    SUM(fact_marketing[spend])

Total Responses =
    CALCULATE(COUNT(fact_marketing[marketing_sk]),
              fact_marketing[responded] = TRUE())

Response Rate % =
    DIVIDE([Total Responses],
           COUNT(fact_marketing[marketing_sk]), 0) * 100

Stockout Rate % =
    DIVIDE(
        CALCULATE(COUNT(fact_inventory[inventory_sk]),
                  fact_inventory[stockout_flag] = TRUE()),
        COUNT(fact_inventory[inventory_sk]),
        0
    ) * 100
```

---

## Dashboard Pages

### Page 1 — Executive Overview
| Visual | Data |
|---|---|
| Card: Total Revenue | [Total Revenue] |
| Card: Total Profit | [Total Profit] |
| Card: Profit Margin % | [Profit Margin %] |
| Card: Total Orders | [Total Orders] |
| Card: AOV | [Average Order Value] |
| Line chart: Revenue by Month | dim_date[year_month] × [Total Revenue] |
| Bar chart: Revenue by Category | dim_product[category] × [Total Revenue] |
| Bar chart: Top 10 Stores | dim_store[store_name] × [Total Revenue] |
| Map: Revenue by State | dim_store[state] × [Total Revenue] |

### Page 2 — Customer Analytics
| Visual | Data |
|---|---|
| Card: Total Customers | [Total Customers] |
| Card: Revenue per Customer | [Revenue per Customer] |
| Bar chart: Revenue by Age Group | dim_customer[age_group] × [Total Revenue] |
| Pie chart: Revenue by Gender | dim_customer[gender] × [Total Revenue] |
| Bar chart: Revenue by Income Segment | dim_customer[income_segment] × [Total Revenue] |
| Bar chart: Revenue by Region | dim_store[region] × [Total Revenue] |
| Slicer: Year | dim_date[year] |

### Page 3 — Product Analytics
| Visual | Data |
|---|---|
| Bar chart: Top 10 Products by Revenue | dim_product[product_name] × [Total Revenue] |
| Bar chart: Revenue by Sub-Category | dim_product[sub_category] × [Total Revenue] |
| Bar chart: Revenue by Brand | dim_product[brand] × [Total Revenue] |
| Scatter: Revenue vs Profit (by Category) | [Total Revenue] × [Total Profit] colored by category |
| Table: Product Performance | product_name, category, [Total Revenue], [Total Profit], [Profit Margin %] |
| Slicer: Category | dim_product[category] |

### Page 4 — Store & Geography
| Visual | Data |
|---|---|
| Map: Revenue by City | dim_store[city] × [Total Revenue] |
| Bar chart: Revenue by Store Type | dim_store[store_type] × [Total Revenue] |
| Table: Store Rankings | store_name, city, region, [Total Revenue], [Total Orders], [Profit Margin %] |
| Slicer: Region | dim_store[region] |

### Page 5 — Inventory
| Visual | Data |
|---|---|
| Card: Stockout Rate % | [Stockout Rate %] |
| Bar chart: Stockout Rate by Category | dim_product[category] × [Stockout Rate %] |
| Table: Slow-Moving Products | product_name, avg_closing_stock, avg_daily_sales |
| Slicer: Store | dim_store[store_name] |

### Page 6 — Marketing
| Visual | Data |
|---|---|
| Card: Total Campaign Spend | [Total Campaign Spend] |
| Card: Response Rate % | [Response Rate %] |
| Bar chart: Response Rate by Channel | dim_campaign[channel] × [Response Rate %] |
| Bar chart: Contacts by Campaign | dim_campaign[campaign_name] × COUNT |
| Bar chart: Spend by Channel | dim_campaign[channel] × [Total Campaign Spend] |
