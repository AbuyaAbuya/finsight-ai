import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build DimTerritory
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building DimTerritory")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

conn.execute("""
DROP TABLE IF EXISTS DimTerritory;
""")

conn.execute("""

CREATE TABLE DimTerritory AS

SELECT

    ROW_NUMBER() OVER(
        ORDER BY territory_key
    )                   AS territory_id,

    territory_key,

    country,

    region

FROM territory_raw

ORDER BY territory_key

""")

rows = conn.execute("""
SELECT COUNT(*)
FROM DimTerritory
""").fetchone()[0]

print(f"\nRows : {rows:,}")

print("\nColumns")
print("-" * 80)

print(conn.execute("""
DESCRIBE DimTerritory
""").fetchdf())

print("\nDuplicate Check")
print("-" * 80)

duplicates = conn.execute("""

SELECT

territory_key,

COUNT(*) records

FROM DimTerritory

GROUP BY territory_key

HAVING COUNT(*) > 1

""").fetchdf()

if duplicates.empty:

    print("✅ No duplicate territories found.")

else:

    print(duplicates)

print("\nSample")
print("-" * 80)

print(conn.execute("""

SELECT *

FROM DimTerritory

ORDER BY territory_key

""").fetchdf())

conn.close()

print("\nDimTerritory created successfully.")