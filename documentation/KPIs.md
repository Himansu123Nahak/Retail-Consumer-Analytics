# KPI Definitions

All monetary values are in Indian Rupees (₹).

## Sales KPIs

| KPI | Definition | Formula |
|---|---|---|
| Total Revenue | Sum of all net transaction amounts | `SUM(total_amount)` |
| Total Profit | Revenue minus cost of goods sold | `SUM(net_revenue - cost)` |
| Profit Margin % | Profit as a % of revenue | `(Total Profit / Total Revenue) × 100` |
| Total Orders | Count of all transactions | `COUNT(transaction_id)` |
| Average Order Value (AOV) | Average revenue per transaction | `Total Revenue / Total Orders` |
| Total Units Sold | Sum of all quantities | `SUM(quantity)` |
| Discount Amount | Total value discounted | `SUM(unit_price × quantity × discount)` |

## Customer KPIs

| KPI | Definition | Formula |
|---|---|---|
| Total Customers | Count of unique customers with a purchase | `COUNT DISTINCT (customer_id)` |
| Repeat Customer Rate | % of customers with more than 1 order | `(Customers with 2+ orders / Total Customers) × 100` |
| Revenue per Customer | Average revenue generated per customer | `Total Revenue / Total Customers` |
| Customer Lifetime Value | Total spend per customer over the full period | `SUM(total_amount) per customer_id` |
| New Customers | Customers making their first purchase in a period | Count of first-purchase customer IDs |

## Product KPIs

| KPI | Definition | Formula |
|---|---|---|
| Top Products by Revenue | Products ranked by total net revenue | `SUM(net_revenue)` grouped by product |
| Category Revenue Share | % of total revenue per category | `Category Revenue / Total Revenue × 100` |
| Product Profit Margin | Margin for a specific product | `(Revenue - Cost) / Revenue × 100` |

## Inventory KPIs

| KPI | Definition | Formula |
|---|---|---|
| Stockout Rate | % of snapshots where closing stock = 0 | `(Stockout days / Total snapshots) × 100` |
| Average Closing Stock | Average end-of-day units in stock | `AVG(closing_stock)` |
| Inventory Value | Value of stock on hand | `SUM(closing_stock × cost_price)` |

## Marketing KPIs

| KPI | Definition | Formula |
|---|---|---|
| Response Rate | % of contacted customers who responded | `(Responses / Contacts) × 100` |
| Total Campaign Spend | Total money spent on campaigns | `SUM(spend)` |
| Cost per Response | Spend divided by number of responses | `Total Spend / Total Responses` |
