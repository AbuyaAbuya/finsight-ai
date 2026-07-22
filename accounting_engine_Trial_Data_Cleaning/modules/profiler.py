import pandas as pd


def profile_general_ledger(gl):
    """
    Profile the General Ledger.
    """

    print("\n" + "=" * 60)
    print("GENERAL LEDGER PROFILE")
    print("=" * 60)

    print(f"Rows                 : {len(gl):,}")
    print(f"Columns              : {len(gl.columns)}")
    print(f"Unique Journals      : {gl['EntryNo'].nunique():,}")
    print(f"Unique Accounts      : {gl['Account_key'].nunique():,}")
    print(f"Date Range           : {gl['Date'].min()}  -->  {gl['Date'].max()}")
    print(f"Total Amount         : {gl['Amount'].sum():,.2f}")

    print("\nMissing Values")
    print("-" * 60)
    print(gl.isna().sum())