import duckdb

# ==============================================================
# FinSight AI
# Build Budget table
#
# Unlike the other finance_mart tables, Budget is NOT derived
# purely from FactGeneralLedger -- it holds user-entered planning
# figures that persist across sessions and get edited over time.
# This script only ensures the table exists; it does not populate
# it. Baseline figures are generated on demand by BudgetService
# (from prior-year actuals), and users can then edit individual
# line items via the Budget page.
# ==============================================================

DB_PATH = "database/finsight.duckdb"

print("=" * 80)
print("Ensuring Budget table exists")
print("=" * 80)

conn = duckdb.connect(DB_PATH)

conn.execute("""
CREATE TABLE IF NOT EXISTS Budget (
    year INTEGER,
    quarter VARCHAR,
    month VARCHAR,
    month_number INTEGER,
    country VARCHAR,
    account VARCHAR,
    budget_amount DOUBLE
)
""")

rows = conn.execute("SELECT COUNT(*) FROM Budget").fetchone()[0]
print(f"\nBudget table ready. Current rows: {rows:,}")

conn.close()
