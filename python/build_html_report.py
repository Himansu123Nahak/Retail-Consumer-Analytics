"""
============================================================
python/build_html_report.py
============================================================
Generates a standalone HTML project summary report:
  - All KPIs displayed as metric cards
  - Embeds all EDA charts
  - RFM segment table
  - Revenue by year table
  - Links to all project files
  
Output: reports/Project_Summary.html
Open in any browser — no internet needed.
============================================================
"""

import pandas as pd
import base64
from pathlib import Path
from datetime import date

PROCESSED_DIR = Path("data/processed")
CHARTS_DIR    = Path("python/03_eda/charts")
OUTPUT_DIR    = Path("reports")
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading data...")
txn  = pd.read_csv(PROCESSED_DIR / "transactions_clean.csv",
                    parse_dates=["transaction_date"])
prod = pd.read_csv(PROCESSED_DIR / "products_clean.csv")
rfm  = pd.read_csv(PROCESSED_DIR / "rfm_segment_summary.csv")

txn_prod = txn.merge(prod[["product_id","category","cost_price"]], on="product_id", how="left")
txn_prod["profit"] = txn_prod["total_amount"] - txn_prod["cost_price"] * txn_prod["quantity"]

total_rev    = txn["total_amount"].sum()
total_profit = txn_prod["profit"].sum()
margin       = total_profit / total_rev * 100
total_orders = len(txn)
aov          = total_rev / total_orders
unique_custs = txn["customer_id"].nunique()
repeat       = (txn.groupby("customer_id").size() > 1).sum()
repeat_rate  = repeat / unique_custs * 100

txn["year"] = txn["transaction_date"].dt.year
yearly = txn.groupby("year")["total_amount"].sum()

top_cat = (txn_prod.groupby("category")["total_amount"]
                   .sum().sort_values(ascending=False).head(5))


def img_to_base64(path):
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def kpi_card(label, value, color):
    return f"""
    <div class="kpi-card" style="border-top: 4px solid {color};">
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>"""


def chart_section(title, charts):
    imgs = ""
    for c in charts:
        p = CHARTS_DIR / c
        if p.exists():
            b64 = img_to_base64(p)
            imgs += f'<img src="data:image/png;base64,{b64}" class="chart-img" alt="{c}"/>'
    return f"""
    <div class="section">
        <h2>{title}</h2>
        <div class="chart-grid">{imgs}</div>
    </div>"""


def rfm_table():
    rows = ""
    colours = {
        "Champions": "#1565C0",
        "Loyal Customers": "#2E7D32",
        "Potential Loyalists": "#00695C",
        "At Risk": "#E65100",
        "Need Attention": "#F57F17",
        "Lost Customers": "#B71C1C",
    }
    for _, r in rfm.iterrows():
        seg   = r["segment"]
        col   = colours.get(seg, "#555")
        rev_cr = r["total_revenue"] / 1e7
        rows += f"""<tr>
            <td><span class="badge" style="background:{col}">{seg}</span></td>
            <td>{int(r["customer_count"]):,}</td>
            <td>₹{r["avg_monetary"]:,.0f}</td>
            <td>₹{rev_cr:.1f} Cr</td>
        </tr>"""
    return rows


def yearly_table():
    rows = ""
    for yr, rev in yearly.items():
        rows += f"<tr><td>{yr}</td><td>₹{rev/1e7:.1f} Cr</td></tr>"
    return rows


def category_table():
    rows = ""
    for cat, rev in top_cat.items():
        rows += f"<tr><td>{cat}</td><td>₹{rev/1e7:.1f} Cr</td></tr>"
    return rows


HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Retail Consumer Intelligence — Project Summary</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', sans-serif; background: #F0F4F8; color: #2D3748; }}

  /* Header */
  .hero {{
    background: linear-gradient(135deg, #1565C0 0%, #0D47A1 50%, #01579B 100%);
    color: white; padding: 60px 40px; text-align: center;
  }}
  .hero h1 {{ font-size: 2.4rem; font-weight: 800; margin-bottom: 12px; }}
  .hero p  {{ font-size: 1.1rem; opacity: 0.85; max-width: 700px; margin: 0 auto 8px; }}
  .hero .meta {{ font-size: 0.9rem; opacity: 0.6; margin-top: 12px; }}

  /* KPI Cards */
  .kpi-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 18px; padding: 36px 40px;
    background: white;
  }}
  .kpi-card {{
    background: #FAFAFA; border-radius: 12px; padding: 22px 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07); text-align: center;
    transition: transform .2s; cursor: default;
  }}
  .kpi-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }}
  .kpi-value {{ font-size: 1.7rem; font-weight: 800; margin-bottom: 6px; }}
  .kpi-label {{ font-size: 0.78rem; font-weight: 600; color: #718096; text-transform: uppercase; letter-spacing: .05em; }}

  /* Sections */
  .section {{ background: white; margin: 20px 40px; border-radius: 16px;
              padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
  .section h2 {{ font-size: 1.3rem; font-weight: 700; color: #1565C0;
                 margin-bottom: 22px; padding-bottom: 10px;
                 border-bottom: 2px solid #E3F2FD; }}

  /* Charts */
  .chart-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 16px; }}
  .chart-img {{ width: 100%; border-radius: 10px; border: 1px solid #E2E8F0;
                 transition: transform .2s; }}
  .chart-img:hover {{ transform: scale(1.02); }}

  /* Tables */
  table {{ width: 100%; border-collapse: collapse; font-size: 0.93rem; }}
  th {{ background: #1565C0; color: white; padding: 10px 14px; text-align: left; font-weight: 600; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #EDF2F7; }}
  tr:nth-child(even) td {{ background: #F7FAFC; }}
  tr:hover td {{ background: #EBF8FF; }}

  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media(max-width: 768px) {{ .two-col {{ grid-template-columns: 1fr; }} .hero h1 {{ font-size: 1.6rem; }} }}

  .badge {{ color: white; padding: 3px 10px; border-radius: 20px;
             font-size: 0.8rem; font-weight: 600; white-space: nowrap; }}

  /* Footer */
  footer {{ text-align: center; padding: 30px; color: #A0AEC0; font-size: 0.85rem;
             margin-top: 20px; }}
  .tag {{ display:inline-block; background:#EBF8FF; color:#2B6CB0;
          border:1px solid #BEE3F8; border-radius:20px;
          padding:4px 12px; margin:4px; font-size:.8rem; font-weight:600; }}
</style>
</head>
<body>

<div class="hero">
  <h1>Retail Consumer Intelligence Platform</h1>
  <p>End-to-end business analytics — from raw data to actionable insights</p>
  <p><strong>200,000</strong> Transactions &nbsp;·&nbsp; <strong>50,000</strong> Customers &nbsp;·&nbsp;
     <strong>5,000</strong> Products &nbsp;·&nbsp; <strong>200</strong> Stores &nbsp;·&nbsp; 2021–2024</p>
  <div class="meta">Generated: {date.today().strftime("%d %B %Y")} &nbsp;|&nbsp;
       Tools: Python &nbsp;·&nbsp; PostgreSQL &nbsp;·&nbsp; SQL &nbsp;·&nbsp; Excel &nbsp;·&nbsp; Power BI</div>
</div>

<!-- KPI Cards -->
<div class="kpi-grid">
  {kpi_card("Total Revenue", f"₹{total_rev/1e7:.0f} Cr", "#1565C0")}
  {kpi_card("Total Profit", f"₹{total_profit/1e7:.0f} Cr", "#2E7D32")}
  {kpi_card("Profit Margin", f"{margin:.1f}%", "#00695C")}
  {kpi_card("Total Orders", f"{total_orders:,}", "#4A148C")}
  {kpi_card("Avg Order Value", f"₹{aov:,.0f}", "#E65100")}
  {kpi_card("Unique Customers", f"{unique_custs:,}", "#01579B")}
  {kpi_card("Repeat Customer Rate", f"{repeat_rate:.1f}%", "#F57F17")}
  {kpi_card("Total Units Sold", f"{txn['quantity'].sum():,}", "#880E4F")}
</div>

<!-- Revenue & Category tables -->
<div class="section">
  <h2>📅 Revenue by Year &amp; Top Categories</h2>
  <div class="two-col">
    <table>
      <tr><th>Year</th><th>Revenue</th></tr>
      {yearly_table()}
    </table>
    <table>
      <tr><th>Category</th><th>Revenue</th></tr>
      {category_table()}
    </table>
  </div>
</div>

<!-- RFM Segments -->
<div class="section">
  <h2>🎯 RFM Customer Segmentation</h2>
  <table>
    <tr><th>Segment</th><th>Customers</th><th>Avg Spend</th><th>Total Revenue</th></tr>
    {rfm_table()}
  </table>
</div>

{chart_section("📈 Sales Analysis", [
    "01_monthly_revenue_trend.png",
    "02_annual_revenue.png",
    "03_revenue_by_day.png",
    "04_payment_method.png",
    "05_discount_distribution.png",
    "06_order_value_dist.png",
])}

{chart_section("👥 Customer Analysis", [
    "07_customer_signups.png",
    "08_age_distribution.png",
    "09_gender_split.png",
    "10_income_segment.png",
    "11_customers_by_state.png",
    "12_orders_per_customer.png",
    "13_revenue_by_age.png",
])}

{chart_section("📦 Product Analysis", [
    "14_revenue_by_category.png",
    "15_units_by_category.png",
    "16_top10_products.png",
    "17_margin_by_category.png",
    "18_top10_brands.png",
])}

{chart_section("🏪 Store & Geography", [
    "19_revenue_by_region.png",
    "20_top10_stores.png",
    "21_revenue_by_store_type.png",
    "22_revenue_by_state.png",
    "23_store_size_vs_revenue.png",
])}

{chart_section("📊 Inventory & Marketing", [
    "24_avg_stock_by_category.png",
    "25_stock_level_distribution.png",
    "26_response_rate_by_channel.png",
    "27_contacts_vs_responses.png",
    "28_responses_by_campaign.png",
])}

<!-- Tech Stack -->
<div class="section">
  <h2>🛠️ Technology Stack</h2>
  <div style="margin-top:8px;">
    <span class="tag">Python 3.13</span>
    <span class="tag">Pandas</span>
    <span class="tag">NumPy</span>
    <span class="tag">Matplotlib</span>
    <span class="tag">Seaborn</span>
    <span class="tag">openpyxl</span>
    <span class="tag">PostgreSQL 17</span>
    <span class="tag">Star Schema</span>
    <span class="tag">Standard SQL</span>
    <span class="tag">Excel</span>
    <span class="tag">Power BI</span>
    <span class="tag">DAX</span>
    <span class="tag">Git</span>
    <span class="tag">psycopg2</span>
    <span class="tag">Rich</span>
    <span class="tag">tqdm</span>
  </div>
</div>

<footer>
  Retail Consumer Intelligence &amp; Business Analytics Platform &nbsp;·&nbsp;
  102 files &nbsp;·&nbsp; 27 SQL scripts &nbsp;·&nbsp; 21 Python scripts &nbsp;·&nbsp; 28 Charts
</footer>

</body>
</html>"""

output = OUTPUT_DIR / "Project_Summary.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"HTML report saved: {output.resolve()}")
print("Open it in your browser to see the full project summary with all charts!")
