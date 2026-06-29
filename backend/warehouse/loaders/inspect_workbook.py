import duckdb
import pandas as pd
from pathlib import Path

# ==============================================================
# FinSight AI
# Inspect Excel Workbook
# ==============================================================

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 100)

WORKBOOK = Path("data/general_ledger.xlsx")

print("=" * 80)
print("FinSight AI - Workbook Inspection")
print("=" * 80)

if not WORKBOOK.exists():
    raise FileNotFoundError(
        f"\nWorkbook not found:\n{WORKBOOK.resolve()}"
    )

print(f"\nWorkbook : {WORKBOOK.name}")

excel = pd.ExcelFile(WORKBOOK)

print(f"Worksheets : {len(excel.sheet_names)}")

print("\nSheet Names")
print("-" * 80)

for i, sheet in enumerate(excel.sheet_names, start=1):
    print(f"{i}. {sheet}")

print("\n" + "=" * 80)
print("WORKSHEET DETAILS")
print("=" * 80)

for sheet in excel.sheet_names:

    print(f"\n{sheet.upper()}")
    print("-" * 80)

    df = pd.read_excel(
        WORKBOOK,
        sheet_name=sheet
    )

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    print("\nColumn Information")
    print(
        pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str)
        })
    )

    print("\nMissing Values")
    print(df.isna().sum())

    print("\nSample Data")
    print(df.head(10))

print("\n" + "=" * 80)
print("Inspection Complete")
print("=" * 80)