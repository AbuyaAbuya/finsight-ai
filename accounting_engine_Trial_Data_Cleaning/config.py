from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

# ==========================================================
# SOURCE WORKBOOK
# ==========================================================

SOURCE_FILE = INPUT_DIR / "general_ledger.xlsx"