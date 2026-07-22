import pandas as pd


def audit_general_ledger(gl):
    """
    Perform a basic audit of the General Ledger.
    """

    print("\n" + "=" * 60)
    print("GENERAL LEDGER AUDIT")
    print("=" * 60)

    print(f"Duplicate rows           : {gl.duplicated().sum():,}")
    print(f"Duplicate Entry Numbers  : {gl['EntryNo'].duplicated().sum():,}")
    print(f"Missing Amounts          : {gl['Amount'].isna().sum():,}")
    print(f"Zero Amounts             : {(gl['Amount'] == 0).sum():,}")

    print("\nTop 10 Journals by Number of Lines")
    print("-" * 60)

    journal_sizes = (
        gl.groupby("EntryNo")
          .size()
          .sort_values(ascending=False)
          .head(10)
    )

    print(journal_sizes)