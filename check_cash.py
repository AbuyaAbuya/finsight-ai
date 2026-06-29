from pathlib import Path

import duckdb
import pandas as pd

DB_PATH = Path("database") / "finsight.duckdb"

conn = duckdb.connect(DB_PATH)

print("\n==============================")
print("CASH & CASH EQUIVALENTS")
print("==============================\n")

query = """
SELECT
    account,
    subaccount,
    SUM(balance) AS balance
FROM FinancialReportingMart
WHERE account = 'Cash & Cash Equivalents'
GROUP BY
    account,
    subaccount
ORDER BY
    balance DESC;
"""

df = conn.execute(query).fetchdf()

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df)

conn.close()