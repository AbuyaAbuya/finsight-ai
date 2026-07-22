import pandas as pd


def load_files(config):
    """
    Load all required sheets from the source workbook.
    """

    workbook = config.SOURCE_FILE

    print(f"Loading workbook: {workbook.name}")

    gl = pd.read_excel(workbook, sheet_name="GL")
    coa = pd.read_excel(workbook, sheet_name="Chart of Accounts")
    calendar = pd.read_excel(workbook, sheet_name="Calendar")
    territory = pd.read_excel(workbook, sheet_name="Territory")
    cashflow = pd.read_excel(workbook, sheet_name="CashFlow_St")
    soce = pd.read_excel(workbook, sheet_name="SoCE_St")

    print(f"✓ GL: {len(gl):,} rows")
    print(f"✓ Chart of Accounts: {len(coa):,} rows")
    print(f"✓ Calendar: {len(calendar):,} rows")
    print(f"✓ Territory: {len(territory):,} rows")
    print(f"✓ Cash Flow Template: {len(cashflow):,} rows")
    print(f"✓ Statement of Changes in Equity Template: {len(soce):,} rows")

    return gl, coa, calendar, territory, cashflow, soce