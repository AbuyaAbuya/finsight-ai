import duckdb
import pandas as pd
from pathlib import Path

# ==============================================================
# FinSight AI
# Load Excel Workbook into DuckDB
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

DB_PATH = "database/finsight.duckdb"
WORKBOOK = Path("data/general_ledger.xlsx")

print("=" * 80)
print("Loading Excel Workbook")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

excel = pd.ExcelFile(WORKBOOK)

for sheet in excel.sheet_names:

    print(f"\nLoading: {sheet}")

    df = pd.read_excel(
        WORKBOOK,
        sheet_name=sheet
    )

    # ----------------------------------------------------------
    # Remove completely empty columns
    # ----------------------------------------------------------

    df = df.dropna(axis=1, how="all")

    # ----------------------------------------------------------
    # Standardize column names
    # ----------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    table = (
        sheet.lower()
        .replace(" ", "_")
        .replace("/", "_")
        + "_raw"
    )

    conn.execute(f"DROP TABLE IF EXISTS {table}")

    conn.register("temp_df", df)

    conn.execute(f"""
        CREATE TABLE {table} AS
        SELECT *
        FROM temp_df
    """)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")
    print(f"Table   : {table}")

print("\n" + "=" * 80)
print("Raw tables created successfully.")
print("=" * 80)

conn.close()