import duckdb
import pandas as pd

# ==============================================================
# FinSight AI
# Build DimDate
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Building DimDate")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

conn.execute("""
DROP TABLE IF EXISTS DimDate;
""")

conn.execute("""

CREATE TABLE DimDate AS

SELECT

    ROW_NUMBER() OVER(
        ORDER BY date
    )                                   AS date_id,

    date,

    year,

    quarter,

    month,

    day,

    EXTRACT(MONTH FROM date)            AS month_number,

    EXTRACT(DAY FROM date)              AS day_number,

    EXTRACT(WEEK FROM date)             AS week_number,

    EXTRACT(DAYOFYEAR FROM date)        AS day_of_year,

    CASE

        WHEN EXTRACT(MONTH FROM date) IN (1,2,3)
            THEN 1

        WHEN EXTRACT(MONTH FROM date) IN (4,5,6)
            THEN 2

        WHEN EXTRACT(MONTH FROM date) IN (7,8,9)
            THEN 3

        ELSE 4

    END                                 AS quarter_number

FROM calendar_raw

ORDER BY date

""")

rows = conn.execute("""
SELECT COUNT(*)
FROM DimDate
""").fetchone()[0]

print(f"\nRows : {rows:,}")

print("\nColumns")
print("-" * 80)

print(conn.execute("""
DESCRIBE DimDate
""").fetchdf())

print("\nDuplicate Check")
print("-" * 80)

duplicates = conn.execute("""

SELECT

date,

COUNT(*) records

FROM DimDate

GROUP BY date

HAVING COUNT(*) > 1

""").fetchdf()

if duplicates.empty:

    print("✅ No duplicate dates found.")

else:

    print(duplicates)

print("\nSample")
print("-" * 80)

print(conn.execute("""

SELECT *

FROM DimDate

LIMIT 20

""").fetchdf())

conn.close()

print("\nDimDate created successfully.")