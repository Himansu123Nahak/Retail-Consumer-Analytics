# Excel Workbook Guide

## File: `excel/Retail_Analysis.xlsx`

## Sheets

### Sheet 1 — Executive KPIs
Manually enter these values after running SQL queries.
Apply conditional formatting: green for good, red for below target.

| KPI | SQL Value | Excel Formula | Power BI Value |
|---|---|---|---|
| Total Revenue | — | =SUMIF(transactions!E:E,"*",transactions!J:J) | — |
| Total Orders | — | =COUNTA(transactions!A:A)-1 | — |
| Avg Order Value | — | =B2/B3 | — |
| Total Profit | — | From SQL query | — |
| Profit Margin % | — | =B4/B2*100 | — |

### Sheet 2 — Sales by Category
1. Select the transactions and products tables (copied from SQL output)
2. Insert → PivotTable
3. Rows: Category
4. Values: SUM of total_amount, COUNT of transaction_id
5. Sort by SUM descending

**Key formulas for a separate summary table:**
```excel
=SUMIF(ProductCategory_col, "Electronics", Revenue_col)
=COUNTIF(ProductCategory_col, "Fashion")
```

### Sheet 3 — Customer Analysis
1. PivotTable from transactions + customers joined data
2. Rows: age_group, gender
3. Values: COUNT DISTINCT customer_id (use helper column), SUM total_amount
4. Slicers: Region, Year

**Key formulas:**
```excel
=SUMIF(gender_col, "Male", revenue_col)
=COUNTIFS(age_col, "25-34", region_col, "South")
```

### Sheet 4 — Store Performance
1. PivotTable from transactions + stores
2. Rows: Region, Store Name
3. Values: SUM revenue, COUNT orders
4. Conditional formatting: colour scale on revenue column

### Sheet 5 — Product Top/Bottom 10
1. SUMIF revenue per product
2. Sort descending → Top 10
3. Sort ascending → Bottom 10
4. Add a bar chart for each

### Sheet 6 — KPI Validation
Compare values across SQL, Excel, and Power BI to confirm they match.

| Metric | SQL Result | Excel Result | Power BI Result | Match? |
|---|---|---|---|---|
| Total Revenue | — | — | — | ✓/✗ |
| Total Orders | — | — | — | ✓/✗ |
| Total Customers | — | — | — | ✓/✗ |

All values should match within ±1%.
