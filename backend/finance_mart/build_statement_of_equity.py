import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build StatementOfEquity
# Roll-forward: Opening Balance + Net Income - Dividends +
# Share Issuance = Closing Balance, computed at monthly
# granularity per territory so it can be filtered the same way
# as every other report.
#
# NOTE: like CashFlowStatement, this is built from
# FactGeneralLedger (transaction-level), not FinancialReportingMart.
# Opening/Closing balances are cumulative-to-date (point-in-time,
# same as the Balance Sheet) and are computed in the service layer
# from FinancialReportingMart directly; this mart only stores the
# PERIOD movement line items (Net Income, Dividends, Share Issued).
# Validated against ground truth (Opening + Net Income - Dividends
# + Share Issued = Closing) for every year and every country before
# being encoded here.
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building StatementOfEquity")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

conn.execute("""
DROP TABLE IF EXISTS StatementOfEquity;
""")

conn.execute("""

CREATE TABLE StatementOfEquity AS

SELECT

    year,
    quarter,
    month,
    month_number,
    country,
    region,

    -- Total income for the period: full P&L (including Taxation,
    -- unlike the Cash Flow Statement's "Profit before tax"), negated
    -- since revenue/gains are stored negative (credit) and expenses
    -- positive (debit).
    -SUM(CASE WHEN account_key IN
        (210,220,230,240,250,260,270,280,290,300,310,320,330,
         340,350,360,370,380,390,400,410,420,430,431,440,450)
        THEN net_amount ELSE 0 END)                        AS net_income,

    -- Dividends paid in the period: account 201 is a contra-equity,
    -- debit-normal account, already positive when dividends increase.
    SUM(CASE WHEN account_key = 201
        THEN net_amount ELSE 0 END)                        AS dividends_for_period,

    -- Issue of share capital: accounts 180 (Share Capital) and 190
    -- (Share Premium) are credit-normal, stored negative; negate for
    -- a positive "amount raised" display.
    -SUM(CASE WHEN account_key IN (180, 190)
        THEN net_amount ELSE 0 END)                        AS share_issued

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

rows = conn.execute("SELECT COUNT(*) FROM StatementOfEquity").fetchone()[0]
print(f"\nRows : {rows:,}")

print("\nColumns")
print("-" * 80)
print(conn.execute("DESCRIBE StatementOfEquity").fetchdf())

print("\nSample (2018, USA)")
print("-" * 80)
print(
    conn.execute("""
        SELECT * FROM StatementOfEquity
        WHERE year = 2018 AND country = 'USA'
        ORDER BY month_number
    """).fetchdf()
)

conn.close()

print("\nStatementOfEquity created successfully.")
