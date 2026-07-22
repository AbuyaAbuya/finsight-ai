import pandas as pd


def generate_trial_balance(normalized_gl, coa):
    """
    Generate Trial Balance and Accounting Exception Report.
    """

    # =====================================================
    # Validate Ledger
    # =====================================================

    ledger_debits = normalized_gl["Debit"].sum()
    ledger_credits = normalized_gl["Credit"].sum()

    print("\n" + "=" * 70)
    print("LEDGER VALIDATION")
    print("=" * 70)

    print(f"Ledger Debits : {ledger_debits:,.2f}")
    print(f"Ledger Credits: {ledger_credits:,.2f}")

    if abs(ledger_debits - ledger_credits) > 0.01:
        raise ValueError("Normalized Ledger does not balance.")

    print("✓ Normalized Ledger Balances")

    # =====================================================
    # Trial Balance
    # =====================================================

    tb = (
        normalized_gl
        .groupby("Account_key", as_index=False)
        .agg(
            Debit=("Debit", "sum"),
            Credit=("Credit", "sum")
        )
    )

    # =====================================================
    # Merge Chart of Accounts
    # =====================================================

    coa_cols = [
        c for c in [
            "Account_key",
            "Account_Name",
            "Statement",
            "Account_Type",
            "Category",
            "SubCategory",
            "Normal_Balance"
        ]
        if c in coa.columns
    ]

    tb = tb.merge(
        coa[coa_cols],
        on="Account_key",
        how="left"
    )

    # =====================================================
    # Net Balance
    # =====================================================

    tb["Balance"] = tb["Debit"] - tb["Credit"]

    # =====================================================
    # Actual Balance Side
    # =====================================================

    def actual_side(balance):

        if balance > 0:
            return "Debit"

        elif balance < 0:
            return "Credit"

        return "Zero"

    tb["Actual_Balance"] = tb["Balance"].apply(actual_side)

    # =====================================================
    # Accounting Review
    # =====================================================

    def review(row):

        expected = str(row["Normal_Balance"]).strip()

        if expected == "":
            expected = "Unknown"

        actual = row["Actual_Balance"]

        if actual == "Zero":
            return "OK"

        if expected == "Unknown":
            return "Unknown"

        if expected == actual:
            return "OK"

        return "Review"

    tb["Status"] = tb.apply(review, axis=1)

    # =====================================================
    # Column Order
    # =====================================================

    columns = [
        "Account_key",
        "Account_Name",
        "Statement",
        "Account_Type",
        "Category",
        "SubCategory",
        "Normal_Balance",
        "Actual_Balance",
        "Status",
        "Debit",
        "Credit",
        "Balance"
    ]

    tb = tb[[c for c in columns if c in tb.columns]]

    tb = tb.sort_values(
        "Account_key"
    ).reset_index(drop=True)

    # =====================================================
    # Totals
    # =====================================================

    totals = {}

    for col in tb.columns:

        if col == "Account_Name":
            totals[col] = "TOTAL"

        elif col in ["Debit", "Credit", "Balance"]:
            totals[col] = tb[col].sum()

        else:
            totals[col] = ""

    tb = pd.concat(
        [tb, pd.DataFrame([totals])],
        ignore_index=True
    )

    # =====================================================
    # Validate Trial Balance
    # =====================================================

    debit_total = tb.iloc[:-1]["Debit"].sum()
    credit_total = tb.iloc[:-1]["Credit"].sum()

    print("\n" + "=" * 70)
    print("TRIAL BALANCE")
    print("=" * 70)

    print(f"Accounts   : {len(tb)-1:,}")
    print(f"Debit      : {debit_total:,.2f}")
    print(f"Credit     : {credit_total:,.2f}")
    print(f"Difference : {debit_total-credit_total:,.2f}")

    if abs(debit_total-credit_total) > 0.01:
        raise ValueError("Trial Balance does not balance.")

    print("✓ Trial Balance Balances")

    # =====================================================
    # Accounting Exceptions
    # =====================================================

    exceptions = tb[
        tb["Status"].isin(["Review", "Unknown"])
    ].copy()

    print("\n" + "=" * 70)
    print("ACCOUNTING EXCEPTIONS")
    print("=" * 70)

    if exceptions.empty:

        print("No accounting exceptions detected.")

    else:

        print(exceptions[
            [
                "Account_key",
                "Account_Name",
                "Normal_Balance",
                "Actual_Balance",
                "Status",
                "Balance"
            ]
        ].to_string(index=False))

        print(f"\nTotal Exceptions : {len(exceptions)}")

    return tb, exceptions