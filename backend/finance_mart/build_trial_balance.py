import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build Trial Balance
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building TrialBalance")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

# ----------------------------------------------------------
# Drop Existing
# ----------------------------------------------------------

conn.execute("""
DROP TABLE IF EXISTS TrialBalance;
""")

# ----------------------------------------------------------
# Build Trial Balance
# ----------------------------------------------------------

conn.execute("""

CREATE TABLE TrialBalance AS

SELECT

    account_id,
    account_key,

    report,
    class,
    subclass,
    subclass2,

    account,
    subaccount,

    year,
    quarter,
    month,
    month_number,

    territory_id,
    country,
    region,

    SUM(debit)              AS debit,

    SUM(credit)             AS credit,

    SUM(net_amount)         AS balance,

    COUNT(*)                AS transactions

FROM FactGeneralLedger

GROUP BY

    account_id,
    account_key,

    report,
    class,
    subclass,
    subclass2,

    account,
    subaccount,

    year,
    quarter,
    month,
    month_number,

    territory_id,
    country,
    region

ORDER BY

    year,
    month_number,
    account_key

""")

# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------

rows = conn.execute("""

SELECT COUNT(*)

FROM TrialBalance

""").fetchone()[0]

print(f"\nRows : {rows:,}")

print("\nColumns")
print("-" * 80)

print(conn.execute("""

DESCRIBE TrialBalance

""").fetchdf())

print("\nFinancial Summary")
print("-" * 80)

print(conn.execute("""

SELECT

report,

SUM(debit) debit,

SUM(credit) credit,

SUM(balance) balance,

SUM(transactions) transactions

FROM TrialBalance

GROUP BY report

ORDER BY report

""").fetchdf())

print("\nTop Accounts")
print("-" * 80)

print(conn.execute("""

SELECT

account_key,
subaccount,

SUM(balance) balance

FROM TrialBalance

GROUP BY

account_key,
subaccount

ORDER BY ABS(SUM(balance)) DESC

LIMIT 20

""").fetchdf())

print("\nSample")
print("-" * 80)

print(conn.execute("""

SELECT *

FROM TrialBalance

LIMIT 20

""").fetchdf())

conn.close()

print("\nTrialBalance created successfully.")