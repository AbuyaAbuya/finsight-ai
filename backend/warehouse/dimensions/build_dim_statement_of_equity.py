import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build DimStatementOfEquity
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building DimStatementOfEquity")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

conn.execute("""
DROP TABLE IF EXISTS DimStatementOfEquity;
""")

conn.execute("""

CREATE TABLE DimStatementOfEquity AS

SELECT

    ROW_NUMBER() OVER(
        ORDER BY account_key
    ) AS equity_id,

    account_key,
    type,
    account,
    balancetype

FROM soce_st_raw

ORDER BY account_key

""")

rows = conn.execute("""
SELECT COUNT(*)
FROM DimStatementOfEquity
""").fetchone()[0]

print(f"\nRows : {rows:,}")

print("\nColumns")
print("-"*80)

print(conn.execute("""
DESCRIBE DimStatementOfEquity
""").fetchdf())

print("\nDuplicate Check")
print("-"*80)

duplicates = conn.execute("""

SELECT

account_key,

COUNT(*) records

FROM DimStatementOfEquity

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

FROM DimStatementOfEquity

LIMIT 20

""").fetchdf())

conn.close()

print("\nDimStatementOfEquity created successfully.")