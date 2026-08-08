# Data Dictionary

## customers / dim_customer

| Column | Type | Description |
|---|---|---|
| customer_id | VARCHAR | Unique customer identifier (e.g. CUS0000001) |
| age_group | VARCHAR | Age bracket: 18-24, 25-34, 35-44, 45-54, 55+ |
| gender | VARCHAR | Male / Female / Other |
| city | VARCHAR | Customer's city |
| state | VARCHAR | Customer's state |
| region | VARCHAR | North / South / West / East / Central |
| income_segment | VARCHAR | Low / Lower-Middle / Middle / Upper-Middle / High |
| signup_date | DATE | Date customer registered |
| customer_segment | VARCHAR | RFM segment assigned by Python pipeline |

## products / dim_product

| Column | Type | Description |
|---|---|---|
| product_id | VARCHAR | Unique product identifier (e.g. PRD00001) |
| product_name | VARCHAR | Full product name |
| category | VARCHAR | Top-level category (Electronics, Fashion, etc.) |
| sub_category | VARCHAR | Sub-category within the category |
| brand | VARCHAR | Brand name |
| cost_price | NUMERIC | Purchase cost per unit (₹) |
| selling_price | NUMERIC | Listed selling price per unit (₹) |
| margin_pct | NUMERIC | (selling_price - cost_price) / selling_price |
| supplier | VARCHAR | Supplier name |

## stores / dim_store

| Column | Type | Description |
|---|---|---|
| store_id | VARCHAR | Unique store identifier (e.g. STR0001) |
| store_name | VARCHAR | Store display name |
| store_type | VARCHAR | Superstore / Mall Outlet / Standalone / Express / Flagship |
| city | VARCHAR | Store city |
| state | VARCHAR | Store state |
| region | VARCHAR | Geographic region |
| store_size_sqft | INTEGER | Floor area in square feet |
| opening_date | DATE | Date the store opened |
| is_active | BOOLEAN | Whether the store is currently operating |

## transactions / fact_sales

| Column | Type | Description |
|---|---|---|
| transaction_id | VARCHAR | Unique transaction ID (e.g. TXN000000001) |
| customer_id | VARCHAR | FK → customers |
| store_id | VARCHAR | FK → stores |
| product_id | VARCHAR | FK → products |
| transaction_date | DATE | Date of transaction |
| quantity | INTEGER | Number of units purchased |
| unit_price | NUMERIC | Price per unit at time of sale (₹) |
| discount | NUMERIC | Discount applied as decimal (e.g. 0.15 = 15%) |
| payment_method | VARCHAR | UPI / Credit Card / Debit Card / Cash / Net Banking / EMI |
| total_amount | NUMERIC | Final amount paid: qty × unit_price × (1 − discount) (₹) |

## inventory / fact_inventory

| Column | Type | Description |
|---|---|---|
| snapshot_date | DATE | Date of the stock snapshot |
| store_id | VARCHAR | FK → stores |
| product_id | VARCHAR | FK → products |
| opening_stock | INTEGER | Units at start of day |
| purchase_qty | INTEGER | Units received from supplier |
| sales_qty | INTEGER | Units sold during the day |
| closing_stock | INTEGER | Units at end of day |
| stockout_flag | INTEGER | 1 if closing_stock = 0 and sales_qty > 0, else 0 |

## marketing_campaigns / fact_marketing

| Column | Type | Description |
|---|---|---|
| campaign_interaction_id | VARCHAR | Unique marketing interaction ID |
| customer_id | VARCHAR | FK → customers |
| campaign_name | VARCHAR | Name of the campaign (e.g. Diwali Sale) |
| channel | VARCHAR | Email / SMS / Social Media / In-App / Push Notification |
| campaign_date | DATE | Date the contact was made |
| responded | INTEGER | 1 = customer responded, 0 = no response |
| spend | NUMERIC | Cost of this contact (₹) |
