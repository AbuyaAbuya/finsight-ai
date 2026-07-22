import sys
from pathlib import Path

# ==========================================================
# Add project root to Python path
# ==========================================================

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

import config

from modules.loader import load_files
from modules.cleaner import clean_general_ledger
from modules.coa_mapper import map_chart_of_accounts
from modules.normalizer import LedgerNormalizer
from modules.trial_balance import generate_trial_balance


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 70)
    print("AI ACCOUNTING NORMALIZATION ENGINE")
    print("=" * 70)

    # ------------------------------------------------------
    # Create Output Folder
    # ------------------------------------------------------

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------
    # Load Source Files
    # ------------------------------------------------------

    print("\nLoading source workbook...")

    gl, coa, calendar, territory, cashflow, soce = load_files(config)

    print("✓ Source workbook loaded successfully")

    # ------------------------------------------------------
    # Clean General Ledger
    # ------------------------------------------------------

    print("\nCleaning General Ledger...")

    gl = clean_general_ledger(gl)

    print(f"✓ Ledger Rows: {len(gl):,}")

    # ------------------------------------------------------
    # Standardize Chart of Accounts
    # ------------------------------------------------------

    print("\nStandardizing Chart of Accounts...")

    coa = map_chart_of_accounts(coa)

    print(f"✓ COA Accounts: {len(coa):,}")

    # ------------------------------------------------------
    # Normalize Ledger
    # ------------------------------------------------------

    print("\nNormalizing journals...")

    normalizer = LedgerNormalizer(
        gl_df=gl,
        coa_df=coa
    )

    normalized_gl = normalizer.normalize()

    print("✓ Journal normalization completed")

    # ------------------------------------------------------
    # Save Normalized Ledger
    # ------------------------------------------------------

    normalized_file = config.OUTPUT_DIR / "GL_Normalized.xlsx"

    normalized_gl.to_excel(
        normalized_file,
        index=False
    )

    print(f"✓ Saved: {normalized_file.name}")

    # ------------------------------------------------------
    # Generate Trial Balance
    # ------------------------------------------------------

    print("\nGenerating Trial Balance...")

    tb, exceptions = generate_trial_balance(
        normalized_gl,
        coa
    )

    tb_file = config.OUTPUT_DIR / "Trial_Balance.xlsx"

    tb.to_excel(
        tb_file,
        index=False
    )

    print(f"✓ Saved: {tb_file.name}")

    # ------------------------------------------------------
    # Save Accounting Exceptions
    # ------------------------------------------------------

    exception_file = config.OUTPUT_DIR / "Accounting_Exceptions.xlsx"

    exceptions.to_excel(
        exception_file,
        index=False
    )

    print(f"✓ Saved: {exception_file.name}")

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    print("\n" + "=" * 70)
    print("PROCESS SUMMARY")
    print("=" * 70)

    print(f"Original Ledger Rows      : {len(gl):,}")
    print(f"Normalized Ledger Rows    : {len(normalized_gl):,}")
    print(f"Unique Journals           : {normalized_gl['EntryNo'].nunique():,}")
    print(f"Chart of Accounts         : {len(coa):,}")
    print(f"Trial Balance Accounts    : {len(tb)-1:,}")
    print(f"Accounting Exceptions     : {len(exceptions):,}")

    print("\n" + "=" * 70)
    print("FIRST 20 NORMALIZED ROWS")
    print("=" * 70)
    print(normalized_gl.head(20))

    print("\n" + "=" * 70)
    print("FIRST 20 TRIAL BALANCE ROWS")
    print("=" * 70)
    print(tb.head(20))

    if not exceptions.empty:

        print("\n" + "=" * 70)
        print("FIRST 20 ACCOUNTING EXCEPTIONS")
        print("=" * 70)
        print(exceptions.head(20))

    print("\n" + "=" * 70)
    print("FILES CREATED")
    print("=" * 70)

    print(f"• {normalized_file}")
    print(f"• {tb_file}")
    print(f"• {exception_file}")

    print("\n" + "=" * 70)
    print("ACCOUNTING NORMALIZATION COMPLETE")
    print("=" * 70)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()