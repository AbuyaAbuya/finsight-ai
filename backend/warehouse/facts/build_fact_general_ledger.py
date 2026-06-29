import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build FactGeneralLedger
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building FactGeneralLedger")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

# ----------------------------------------------------------
# Drop Existing Table
# ----------------------------------------------------------

conn.execute("""
DROP TABLE IF EXISTS FactGeneralLedger;
""")

# ----------------------------------------------------------
# Build Fact Table
# ----------------------------------------------------------

conn.execute("""

CREATE TABLE FactGeneralLedger AS

SELECT

    -- =====================================================
    -- Dimension Keys
    -- =====================================================

    d.date_id,
    a.account_id,
    t.territory_id,

    -- =====================================================
    -- Business Keys
    -- =====================================================

    gl.entryno,
    CAST(gl.date AS DATE)            AS transaction_date,
    gl.account_key,
    gl.territory_key,

    -- =====================================================
    -- Date Attributes
    -- =====================================================

    d.year,
    d.quarter,
    d.month,
    d.month_number,
    d.week_number,

    -- =====================================================
    -- Account Attributes
    -- =====================================================

    a.report,
    a.class,
    a.subclass,
    a.subclass2,
    a.account,
    a.subaccount,

    -- =====================================================
    -- Territory Attributes
    -- =====================================================

    t.country,
    t.region,

    -- =====================================================
    -- Transaction
    -- =====================================================

    gl.details,

    CAST(gl.amount AS DOUBLE)        AS amount,

    CASE

        WHEN gl.amount > 0

            THEN gl.amount

        ELSE 0

    END                              AS debit,

    CASE

        WHEN gl.amount < 0

            THEN ABS(gl.amount)

        ELSE 0

    END                              AS credit,

    gl.amount                        AS net_amount

FROM gl_raw gl

INNER JOIN DimAccount a

ON gl.account_key = a.account_key

INNER JOIN DimDate d

ON CAST(gl.date AS DATE)=CAST(d.date AS DATE)

INNER JOIN DimTerritory t

ON gl.territory_key=t.territory_key

ORDER BY

transaction_date,
entryno

""")

# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------

print("\nRows")
print("-"*80)

print(

conn.execute("""

SELECT COUNT(*)

FROM FactGeneralLedger

""").fetchone()[0]

)

print("\nColumns")
print("-"*80)

print(

conn.execute("""

DESCRIBE FactGeneralLedger

""").fetchdf()

)

print("\nFinancial Summary")
print("-"*80)

print(

conn.execute("""

SELECT

report,

COUNT(*) transactions,

SUM(debit) debit,

SUM(credit) credit,

SUM(net_amount) balance

FROM FactGeneralLedger

GROUP BY report

ORDER BY report

""").fetchdf()

)

print("\nSample")
print("-"*80)

print(

conn.execute("""

SELECT *

FROM FactGeneralLedger

LIMIT 20

""").fetchdf()

)

conn.close()

print("\nFactGeneralLedger created successfully.")