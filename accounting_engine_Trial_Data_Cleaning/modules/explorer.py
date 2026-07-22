import pandas as pd


def explore_general_ledger(gl):
    """
    Explore the structure of the General Ledger.
    """

    print("\n" + "=" * 60)
    print("GENERAL LEDGER EXPLORER")
    print("=" * 60)

    # ---------------------------------------------------
    # Journal Size Distribution
    # ---------------------------------------------------
    print("\nJournal Size Distribution")
    print("-" * 60)

    journal_sizes = gl.groupby("EntryNo").size()

    print(journal_sizes.value_counts().sort_index())

    # ---------------------------------------------------
    # Largest Journals
    # ---------------------------------------------------
    print("\nLargest Journals")
    print("-" * 60)

    largest = (
        journal_sizes
        .sort_values(ascending=False)
        .head(10)
    )

    print(largest)

    # ---------------------------------------------------
    # Most Frequently Used Accounts
    # ---------------------------------------------------
    print("\nMost Frequently Used Accounts")
    print("-" * 60)

    print(gl["Account_key"].value_counts().head(20))

    # ---------------------------------------------------
    # Largest Positive Accounts
    # ---------------------------------------------------
    print("\nLargest Account Balances")
    print("-" * 60)

    balances = (
        gl.groupby("Account_key")["Amount"]
          .sum()
          .sort_values(ascending=False)
    )

    print(balances.head(15))

    # ---------------------------------------------------
    # Largest Negative Accounts
    # ---------------------------------------------------
    print("\nMost Negative Account Balances")
    print("-" * 60)

    print(balances.tail(15))

    # ---------------------------------------------------
    # Sample Journals
    # ---------------------------------------------------
    print("\nSample Journal 1")
    print("-" * 60)

    sample = gl[gl["EntryNo"] == gl["EntryNo"].iloc[0]]
    print(sample)

    print("\nSample Journal 2")
    print("-" * 60)

    second = gl[gl["EntryNo"] == gl["EntryNo"].iloc[50]]
    print(second)