from pathlib import Path

import duckdb

DB_PATH = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "finsight.duckdb"
)

# Accounts credit-normal in the corrected ledger (Revenue/Income/Gains),
# stored as negative balances -- same convention used throughout the
# Income Statement. Flipped to positive here so budget figures are
# intuitive to enter and read (a revenue target and an expense budget
# should both look like ordinary positive numbers).
CREDIT_NORMAL_ACCOUNTS = {
    "Sales",
    "Interest Income",
    "Dividend Income",
    "Gain/Loss on Sales of Asset",
    "Exchange Loss/Gain",
}

# The set of P&L line items a budget is planned against, matching the
# Income Statement's line-item granularity.
BUDGETABLE_ACCOUNTS = [
    "Sales",
    "Sales Return",
    "Cost of Sales",
    "Staff Costs",
    "Commissions",
    "Advertisements",
    "Travel",
    "Entertainment",
    "Office Supplies",
    "Professional Services",
    "Telephone",
    "Utilities",
    "Other Expenses",
    "Equipment",
    "Amortization of Intangible Assets",
    "Interest Income",
    "Dividend Income",
    "Gain/Loss on Sales of Asset",
    "Exchange Loss/Gain",
    "Interest Expense",
    "Taxation",
]


class BudgetService:

    def __init__(self):
        self.conn = duckdb.connect(DB_PATH)
        self._ensure_table()

    def _ensure_table(self):
        self.conn.execute("""
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

    # ==========================================================
    # ACTUALS (period-exact, matching Income Statement)
    # ==========================================================

    def _actuals_by_month_account(self, year, country=None):

        clauses = ["year = ?", "report = 'Profit and Loss'"]
        params = [year]

        if country:
            clauses.append("country = ?")
            params.append(country)

        where = " WHERE " + " AND ".join(clauses)

        rows = self.conn.execute(
            f"""
            SELECT
                month,
                month_number,
                quarter,
                account,
                SUM(balance) AS balance
            FROM FinancialReportingMart
            {where}
            GROUP BY month, month_number, quarter, account
            """,
            params,
        ).fetchall()

        result = {}

        for month, month_number, quarter, account, balance in rows:
            display = -balance if account in CREDIT_NORMAL_ACCOUNTS else balance
            result[(month_number, account)] = {
                "month": month,
                "month_number": month_number,
                "quarter": quarter,
                "amount": float(display),
            }

        return result

    # ==========================================================
    # BASELINE GENERATION
    # ==========================================================

    def generate_baseline(self, year, country=None, growth_rate=0.0):

        prior_actuals = self._actuals_by_month_account(year - 1, country)

        month_lookup = self.conn.execute(
            """
            SELECT DISTINCT month, month_number, quarter
            FROM FinancialReportingMart
            ORDER BY month_number
            """
        ).fetchall()

        # Clear any existing budget for this year/country combination
        # before regenerating, so this can be safely re-run.
        if country:
            self.conn.execute(
                "DELETE FROM Budget WHERE year = ? AND country = ?",
                [year, country],
            )
        else:
            self.conn.execute(
                "DELETE FROM Budget WHERE year = ? AND country IS NULL",
                [year],
            )

        rows_to_insert = []

        for month, month_number, quarter in month_lookup:
            for account in BUDGETABLE_ACCOUNTS:
                prior = prior_actuals.get((month_number, account))
                baseline_amount = (
                    prior["amount"] * (1 + growth_rate) if prior else 0.0
                )

                rows_to_insert.append((
                    year,
                    quarter,
                    month,
                    month_number,
                    country,
                    account,
                    baseline_amount,
                ))

        self.conn.executemany(
            """
            INSERT INTO Budget
                (year, quarter, month, month_number, country, account, budget_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows_to_insert,
        )

        return len(rows_to_insert)

    # ==========================================================
    # BUDGET VS ACTUAL
    # ==========================================================

    def get_budget_vs_actual(self, year, country=None):

        if country:
            existing = self.conn.execute(
                "SELECT COUNT(*) FROM Budget WHERE year = ? AND country = ?",
                [year, country],
            ).fetchone()[0]
        else:
            existing = self.conn.execute(
                "SELECT COUNT(*) FROM Budget WHERE year = ? AND country IS NULL",
                [year],
            ).fetchone()[0]

        if existing == 0:
            self.generate_baseline(year, country, growth_rate=0.0)

        if country:
            budget_rows = self.conn.execute(
                """
                SELECT month, month_number, quarter, account, budget_amount
                FROM Budget
                WHERE year = ? AND country = ?
                """,
                [year, country],
            ).fetchall()
        else:
            budget_rows = self.conn.execute(
                """
                SELECT month, month_number, quarter, account, budget_amount
                FROM Budget
                WHERE year = ? AND country IS NULL
                """,
                [year],
            ).fetchall()

        actuals = self._actuals_by_month_account(year, country)

        results = []

        for month, month_number, quarter, account, budget_amount in budget_rows:
            actual_entry = actuals.get((month_number, account))
            actual_amount = actual_entry["amount"] if actual_entry else 0.0

            variance = actual_amount - budget_amount

            # For credit-normal (revenue/income) accounts, actual >
            # budget is favorable. For everything else (expenses),
            # actual < budget (spending less than planned) is
            # favorable.
            favorable = (
                variance >= 0
                if account in CREDIT_NORMAL_ACCOUNTS
                else variance <= 0
            )

            variance_pct = (
                (variance / abs(budget_amount) * 100) if budget_amount else None
            )

            results.append({
                "month": month,
                "month_number": month_number,
                "quarter": quarter,
                "account": account,
                "budget": round(budget_amount, 2),
                "actual": round(actual_amount, 2),
                "variance": round(variance, 2),
                "variance_pct": round(variance_pct, 1) if variance_pct is not None else None,
                "favorable": favorable,
            })

        results.sort(key=lambda r: (r["month_number"], BUDGETABLE_ACCOUNTS.index(r["account"])))

        return results

    # ==========================================================
    # UPDATE A SINGLE BUDGET LINE
    # ==========================================================

    def update_budget_line(
        self,
        year,
        month,
        country,
        account,
        budget_amount,
    ):

        month_info = self.conn.execute(
            """
            SELECT DISTINCT month_number, quarter
            FROM FinancialReportingMart
            WHERE month = ?
            LIMIT 1
            """,
            [month],
        ).fetchone()

        if not month_info:
            raise ValueError(f"Unknown month: {month}")

        month_number, quarter = month_info

        if country:
            self.conn.execute(
                "DELETE FROM Budget WHERE year = ? AND month = ? AND country = ? AND account = ?",
                [year, month, country, account],
            )
        else:
            self.conn.execute(
                "DELETE FROM Budget WHERE year = ? AND month = ? AND country IS NULL AND account = ?",
                [year, month, account],
            )

        self.conn.execute(
            """
            INSERT INTO Budget
                (year, quarter, month, month_number, country, account, budget_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [year, quarter, month, month_number, country, account, budget_amount],
        )

        return True

    def close(self):
        self.conn.close()
