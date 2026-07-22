import pandas as pd


def validate_journals(gl):
    """
    Validate whether each journal balances.
    """

    print("\n" + "=" * 60)
    print("JOURNAL VALIDATION")
    print("=" * 60)

    journal_totals = (
        gl.groupby("EntryNo")["Amount"]
        .sum()
        .round(2)
    )

    balanced = journal_totals[journal_totals == 0]
    unbalanced = journal_totals[journal_totals != 0]

    print(f"Total Journals      : {len(journal_totals):,}")
    print(f"Balanced Journals   : {len(balanced):,}")
    print(f"Unbalanced Journals : {len(unbalanced):,}")

    if len(unbalanced) > 0:
        print("\nFirst 20 Unbalanced Journals")
        print("-" * 60)
        print(unbalanced.head(20))

    return balanced, unbalanced