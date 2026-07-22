import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build CashFlowStatement
# Indirect-method Cash Flow Statement, computed at monthly
# granularity per territory so it can be filtered the same way
# as every other report (year / quarter / month / country).
#
# NOTE: this is built from FactGeneralLedger (transaction-level,
# retains `details` and `account_key`), NOT FinancialReportingMart
# (which aggregates those away). Several accounts serve multiple
# purposes -- e.g. account 90 (PPE) is touched by "Purchase of
# equipment", "Depreciation for the month", AND "Sale of asset" --
# so line items are disambiguated by (details, account_key), not
# just account_key alone. This was validated against ground truth
# (Opening Cash + Net Change = Closing Cash) for every year and
# every country before being encoded here.
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building CashFlowStatement")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

conn.execute("""
DROP TABLE IF EXISTS CashFlowStatement;
""")

# ----------------------------------------------------------
# Build Cash Flow Statement (one row per year/month/territory,
# with each indirect-method line item as its own column)
# ----------------------------------------------------------

conn.execute("""

CREATE TABLE CashFlowStatement AS

SELECT

    year,
    quarter,
    month,
    month_number,
    country,
    region,

    -- Profit before tax: sum of the core P&L accounts (revenue
    -- stored negative/credit, expenses positive/debit under our
    -- corrected convention), negated so a profitable period shows
    -- as a positive number.
    -SUM(CASE WHEN account_key IN
        (210,220,230,240,250,260,270,280,290,300,310,320,330,
         340,350,360,370,380,390,400,410,420,430,431,440)
        THEN net_amount ELSE 0 END)                        AS profit_before_tax,

    SUM(CASE WHEN account_key IN (370,380,390,400)
        THEN net_amount ELSE 0 END)                        AS depreciation_amortization,

    SUM(CASE WHEN account_key IN (410,420,430,431)
        THEN net_amount ELSE 0 END)                        AS non_operating_removed,

    SUM(CASE WHEN account_key = 440
        THEN net_amount ELSE 0 END)                        AS interest_expense_addback,

    -SUM(CASE WHEN account_key = 30 THEN net_amount ELSE 0 END)  AS receivables_change,
    -SUM(CASE WHEN account_key = 60 THEN net_amount ELSE 0 END)  AS inventory_change,
    -SUM(CASE WHEN account_key IN (110,120) THEN net_amount ELSE 0 END) AS payables_change,

    SUM(CASE WHEN details = 'Interest expense' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS interest_paid,

    SUM(CASE WHEN details = 'Tax payment for the previous year' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS tax_paid,

    SUM(CASE WHEN details = 'Purchase of equipment' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS purchase_equipment,

    SUM(CASE WHEN details = 'Sale of asset' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS proceeds_from_sale_of_asset,

    SUM(CASE WHEN details = 'Purchase of shares' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS investments_purchase,

    SUM(CASE WHEN details = 'Interest income' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS interest_received,

    SUM(CASE WHEN details = 'Dividend income' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS dividends_received,

    SUM(CASE WHEN details = 'Exchange gain/loss' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS exchange_gain_loss_cash,

    SUM(CASE WHEN details = 'Share Issue' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS share_capital_issued,

    SUM(CASE WHEN details = 'New loan raised @ 6%' AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS new_loan_proceeds,

    SUM(CASE WHEN details IN ('Payment of interim dividends', 'Payment of final dividends')
        AND account_key = 10
        THEN net_amount ELSE 0 END)                        AS dividends_paid_cash

FROM FactGeneralLedger

GROUP BY

    year,
    quarter,
    month,
    month_number,
    country,
    region

ORDER BY year, month_number, country

""")

rows = conn.execute("SELECT COUNT(*) FROM CashFlowStatement").fetchone()[0]
print(f"\nRows : {rows:,}")

print("\nColumns")
print("-" * 80)
print(conn.execute("DESCRIBE CashFlowStatement").fetchdf())

print("\nSample (2018, USA)")
print("-" * 80)
print(
    conn.execute("""
        SELECT * FROM CashFlowStatement
        WHERE year = 2018 AND country = 'USA'
        ORDER BY month_number
    """).fetchdf()
)

conn.close()

print("\nCashFlowStatement created successfully.")
