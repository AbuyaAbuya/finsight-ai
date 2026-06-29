import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build DimCashFlow
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building DimCashFlow")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

conn.execute("""
DROP TABLE IF EXISTS DimCashFlow;
""")

conn.execute("""

CREATE TABLE DimCashFlow AS

SELECT

    ROW_NUMBER() OVER(
        ORDER BY account_key
    ) AS cashflow_id,

    account_key,
    type,
    subtype,
    account,
    subaccount,
    valuetype

FROM cashflow_st_raw

ORDER BY account_key

""")

rows = conn.execute("""
SELECT COUNT(*)
FROM DimCashFlow
""").fetchone()[0]

print(f"\nRows : {rows:,}")

print("\nColumns")
print("-"*80)

print(conn.execute("""
DESCRIBE DimCashFlow
""").fetchdf())

print("\nDuplicate Check")
print("-"*80)

duplicates = conn.execute("""

SELECT

account_key,

COUNT(*) records

FROM DimCashFlow

GROUP BY account_key

HAVING COUNT(*) > 1

""").fetchdf()

if duplicates.empty:
    print("✅ No duplicate mappings found.")
else:
    print(duplicates)

print("\nSample")
print("-"*80)

print(conn.execute("""

SELECT *

FROM DimCashFlow

LIMIT 20

""").fetchdf())

conn.close()

print("\nDimCashFlow created successfully.")