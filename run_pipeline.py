"""
============================================================
run_pipeline.py
============================================================
Master script — runs the full analytics pipeline in order.
Run from the project root:
    py run_pipeline.py

Steps:
  1. Data cleaning (transactions, customers, products)
  2. EDA (sales, customers, products, stores)
  3. Customer analytics (RFM, CLV)
  4. Statistical correlations
============================================================
"""

import subprocess
import sys
import time
from pathlib import Path

PY = sys.executable

STEPS = [
    ("Data Cleaning — Transactions",
     "python/02_data_cleaning/clean_transactions.py"),
    ("Data Cleaning — Customers",
     "python/02_data_cleaning/clean_customers.py"),
    ("Data Cleaning — Products",
     "python/02_data_cleaning/clean_products.py"),
    ("EDA — Sales",
     "python/03_eda/01_sales_eda.py"),
    ("EDA — Customers",
     "python/03_eda/02_customer_eda.py"),
    ("EDA — Products",
     "python/03_eda/03_product_eda.py"),
    ("EDA — Stores",
     "python/03_eda/04_store_eda.py"),
    ("Customer Analytics — RFM",
     "python/04_customer_analytics/rfm_analysis.py"),
    ("Customer Analytics — CLV",
     "python/04_customer_analytics/clv_analysis.py"),
    ("Statistical Analysis — Correlations",
     "python/07_statistical_analysis/basic_correlations.py"),
]

print("=" * 60)
print("  Retail Consumer Intelligence — Full Pipeline")
print("=" * 60)

failed = []
for i, (label, script) in enumerate(STEPS, 1):
    print(f"\n[{i}/{len(STEPS)}] {label}")
    print(f"  Running: {script}")
    t0 = time.time()
    result = subprocess.run(
        [PY, script],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    elapsed = time.time() - t0
    if result.returncode == 0:
        print(f"  OK  ({elapsed:.1f}s)")
        # Print last 3 lines of output
        lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
        for line in lines[-3:]:
            print(f"    {line}")
    else:
        print(f"  FAILED ({elapsed:.1f}s)")
        print(result.stderr[-500:] if result.stderr else "No error output.")
        failed.append(label)

print("\n" + "=" * 60)
if failed:
    print(f"  Pipeline finished with {len(failed)} failure(s):")
    for f in failed:
        print(f"    - {f}")
else:
    print("  Pipeline completed successfully!")
    print(f"  Charts saved to: python/03_eda/charts/")
    print(f"  Analytics saved to: data/processed/")
print("=" * 60)
