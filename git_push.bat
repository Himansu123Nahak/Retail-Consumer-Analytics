@echo off
:: ============================================================
:: git_push.bat - One-click Git init and push to GitHub
:: Run this AFTER Git is installed
:: ============================================================

echo.
echo ================================================
echo   Retail Analytics - Git Push to GitHub
echo ================================================
echo.

:: Add Git to PATH for this session
SET PATH=C:\Program Files\Git\cmd;C:\Program Files\Git\bin;%PATH%

echo [1/6] Configuring git identity...
git config --global user.name "Himanshu Nahak"
git config --global user.email "himansunahak@gmail.com"
git config --global init.defaultBranch main

echo [2/6] Initialising repository...
git init

echo [3/6] Staging all project files...
git add .
git status --short

echo [4/6] Creating initial commit...
git commit -m "Initial commit: Retail Consumer Intelligence Platform

- 200K transactions, 50K customers, 5K products, 200 stores (2021-2024)
- PostgreSQL star schema: 4 dims, 3 facts, 5 analytical views
- 27 SQL analytics queries (sales, customer, product, inventory, marketing)
- 21 Python scripts: ETL, EDA, RFM, CLV, statistical analysis
- 28 EDA charts across sales, customers, products, stores, marketing
- Excel workbook: 6 sheets with KPI cards and charts
- Power BI guide: 6-page dashboard with DAX measures
- Full documentation: business requirements, data dictionary, KPIs, insights
- Key findings: 84.3%% repeat rate, Rs 873 Cr total revenue"

echo [5/6] Setting remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/Himansu123Nahak/Retail-Consumer-Analytics.git

echo [6/6] Pushing to GitHub...
echo.
echo When prompted:
echo   Username: Himansu123Nahak
echo   Password: ^<paste your GitHub Personal Access Token^>
echo.
git push -u origin main

echo.
echo ================================================
echo   Done! Visit:
echo   https://github.com/Himansu123Nahak/Retail-Consumer-Analytics
echo ================================================
pause
