from pathlib import Path
import duckdb

conn = duckdb.connect(Path("database/finsight.duckdb"))

df = conn.execute("""
SELECT DISTINCT
    report,
    class,
    subclass,
    subclass2,
    account,
    subaccount
FROM FinancialReportingMart
ORDER BY
    report,
    class,
    subclass,
    subclass2,
    account,
    subaccount;
""").fetchdf()

print(df)

conn.close()