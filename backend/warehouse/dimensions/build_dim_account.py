import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build DimAccount
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building DimAccount")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

# ----------------------------------------------------------
# Build Dimension
# ----------------------------------------------------------

conn.execute("""
DROP TABLE IF EXISTS DimAccount;
""")

conn.execute("""

CREATE TABLE DimAccount AS

SELECT

    ROW_NUMBER() OVER(
        ORDER BY account_key
    )                                       AS account_id,

    account_key,

    report,

    class,

    subclass,

    subclass2,

    account,

    subaccount

FROM chart_of_accounts_raw

ORDER BY account_key

""")

# ----------------------------------------------------------
# Summary
# ----------------------------------------------------------

rows = conn.execute("""
SELECT COUNT(*)
FROM DimAccount
""").fetchone()[0]

print(f"\nRows : {rows:,}")

print("\nColumns")
print("-" * 80)

print(
    conn.execute("""
    DESCRIBE DimAccount
    """).fetchdf()
)

print("\nDuplicate Check")
print("-" * 80)

duplicates = conn.execute("""

SELECT

    account_key,

    COUNT(*) records

FROM DimAccount

GROUP BY account_key

HAVING COUNT(*) > 1

""").fetchdf()

if duplicates.empty:

    print("✅ No duplicate accounts found.")

else:

    print(duplicates)

print("\nSample")
print("-" * 80)

print(
    conn.execute("""
    SELECT *
    FROM DimAccount
    LIMIT 20
    """).fetchdf()
)

conn.close()

print("\nDimAccount created successfully.")