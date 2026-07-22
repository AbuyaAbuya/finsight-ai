import pandas as pd

SUSPENSE_ACCOUNT = {
    "Account_key": 9999,
    "Report": "Balance Sheet",
    "Class": "Assets",
    "SubClass": "Current Assets",
    "SubClass2": "Suspense",
    "Account": "Suspense / Clearing",
    "SubAccount": "Suspense / Clearing"
}


def map_chart_of_accounts(coa):
    """
    Standardize the Chart of Accounts using the actual
    workbook structure.
    """

    coa = coa.copy()

    coa.columns = coa.columns.str.strip()

    # Rename to canonical names
    coa = coa.rename(
        columns={
            "Report": "Statement",
            "Class": "Account_Type",
            "SubClass": "Category",
            "SubClass2": "SubCategory",
            "Account": "Account_Name",
            "SubAccount": "Sub_Account"
        }
    )

    # Add Normal Balance
    if "Normal_Balance" not in coa.columns:

        def normal_balance(account_type):

            account_type = str(account_type).lower()

            if account_type in ["assets", "expense", "expenses"]:
                return "Debit"

            if account_type in ["liabilities",
                                "equity",
                                "income",
                                "revenue"]:
                return "Credit"

            return "Unknown"

        coa["Normal_Balance"] = coa["Account_Type"].apply(normal_balance)

    # Add Suspense account if missing
    if 9999 not in coa["Account_key"].values:

        suspense = pd.DataFrame([{
            "Account_key":9999,
            "Statement":"Balance Sheet",
            "Account_Type":"Assets",
            "Category":"Current Assets",
            "SubCategory":"Suspense",
            "Account_Name":"Suspense / Clearing",
            "Sub_Account":"Suspense / Clearing",
            "Normal_Balance":"Debit"
        }])

        coa = pd.concat(
            [coa, suspense],
            ignore_index=True
        )

    coa = coa.sort_values("Account_key")

    print("\n")
    print("="*70)
    print("STANDARDIZED CHART OF ACCOUNTS")
    print("="*70)

    print(coa.head(15))

    return coa