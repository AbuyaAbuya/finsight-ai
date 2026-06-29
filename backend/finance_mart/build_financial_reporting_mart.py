import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build FinancialReportingMart
# Enterprise Semantic Layer
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building FinancialReportingMart")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

# ----------------------------------------------------------
# Drop Existing Table
# ----------------------------------------------------------

conn.execute("""
DROP TABLE IF EXISTS FinancialReportingMart;
""")

# ----------------------------------------------------------
# Build Financial Reporting Mart
# ----------------------------------------------------------

conn.execute("""

CREATE TABLE FinancialReportingMart AS

SELECT

    -- ======================================================
    -- Time
    -- ======================================================

    year,
    quarter,
    month,
    month_number,

    -- ======================================================
    -- Geography
    -- ======================================================

    territory_id,
    country,
    region,

    -- ======================================================
    -- Account
    -- ======================================================

    account_id,
    account_key,

    report,
    class,
    subclass,
    subclass2,

    account,
    subaccount,

    -- ======================================================
    -- Financial Measures
    -- ======================================================

    SUM(debit)           AS debit,
    SUM(credit)          AS credit,
    SUM(net_amount)      AS balance,
    COUNT(*)             AS transactions

FROM FactGeneralLedger

GROUP BY

    year,
    quarter,
    month,
    month_number,

    territory_id,
    country,
    region,

    account_id,
    account_key,

    report,
    class,
    subclass,
    subclass2,

    account,
    subaccount

ORDER BY

    year,
    month_number,
    account_key,
    territory_id

""")

# ----------------------------------------------------------
# Row Count
# ----------------------------------------------------------

rows = conn.execute("""

SELECT COUNT(*)

FROM FinancialReportingMart

""").fetchone()[0]

print(f"\nRows : {rows:,}")

# ----------------------------------------------------------
# Structure
# ----------------------------------------------------------

print("\nColumns")
print("-" * 80)

print(

    conn.execute("""

    DESCRIBE FinancialReportingMart

    """).fetchdf()

)

# ----------------------------------------------------------
# Financial Statement Summary
# ----------------------------------------------------------

print("\nFinancial Statement Summary")
print("-" * 80)

print(

    conn.execute("""

    SELECT

        report,

        SUM(balance)      AS balance,
        SUM(debit)        AS debit,
        SUM(credit)       AS credit,
        SUM(transactions) AS transactions

    FROM FinancialReportingMart

    GROUP BY report

    ORDER BY report

    """).fetchdf()

)

# ----------------------------------------------------------
# Class Summary
# ----------------------------------------------------------

print("\nClass Summary")
print("-" * 80)

print(

    conn.execute("""

    SELECT

        class,

        SUM(balance) AS balance,

        COUNT(*) AS row_count

    FROM FinancialReportingMart

    GROUP BY class

    ORDER BY class

    """).fetchdf()

)

# ----------------------------------------------------------
# Top 20 Accounts
# ----------------------------------------------------------

print("\nTop 20 Accounts")
print("-" * 80)

print(

    conn.execute("""

    SELECT

        account_key,

        subaccount,

        SUM(balance) AS balance

    FROM FinancialReportingMart

    GROUP BY

        account_key,
        subaccount

    ORDER BY ABS(SUM(balance)) DESC

    LIMIT 20

    """).fetchdf()

)

# ----------------------------------------------------------
# Sample
# ----------------------------------------------------------

print("\nSample")
print("-" * 80)

print(

    conn.execute("""

    SELECT *

    FROM FinancialReportingMart

    LIMIT 20

    """).fetchdf()

)

conn.close()

print("\nFinancialReportingMart created successfully.")