import pandas as pd


def clean_general_ledger(gl):
    """
    Clean the General Ledger without changing the source workbook.
    """

    # Remove completely empty columns
    gl = gl.dropna(axis=1, how="all")

    # Remove columns that are more than 99% empty
    threshold = len(gl) * 0.01
    gl = gl.dropna(axis=1, thresh=threshold)

    # Clean column names
    gl.columns = gl.columns.str.strip()

    print("\n" + "=" * 60)
    print("GENERAL LEDGER CLEANING")
    print("=" * 60)

    print(f"Columns after cleaning: {len(gl.columns)}")

    print("\nRemaining Columns:")
    for column in gl.columns:
        print(f" - {column}")

    return gl