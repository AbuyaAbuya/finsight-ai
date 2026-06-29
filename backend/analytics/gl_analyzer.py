class GLAnalyzer:
    """
    Analyzes General Ledger balances to identify
    the largest contributors to Revenue, Expenses and Cash.
    """

    def top_expense_drivers(self, conn, where="", params=None):

        if params is None:
            params = []

        rows = conn.execute(
            f"""
            SELECT
                subaccount,
                SUM(ABS(balance)) AS amount
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} report='Profit and Loss'
            AND balance < 0
            GROUP BY
                subaccount
            ORDER BY
                amount DESC
            LIMIT 5
            """,
            params,
        ).fetchall()

        total = sum(r[1] for r in rows)

        drivers = []

        for account, amount in rows:

            percent = 0

            if total > 0:

                percent = amount / total * 100

            drivers.append({

                "account": account,

                "amount": float(amount),

                "percent": round(percent, 1),

            })

        return drivers

    # -----------------------------------------------------

    def top_revenue_drivers(self, conn, where="", params=None):

        if params is None:
            params = []

        rows = conn.execute(
            f"""
            SELECT
                subaccount,
                SUM(balance) AS amount
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} subaccount='Sales'
            GROUP BY
                subaccount
            ORDER BY
                amount DESC
            LIMIT 5
            """,
            params,
        ).fetchall()

        total = sum(r[1] for r in rows)

        drivers = []

        for account, amount in rows:

            percent = 0

            if total > 0:

                percent = amount / total * 100

            drivers.append({

                "account": account,

                "amount": float(amount),

                "percent": round(percent, 1),

            })

        return drivers

    # -----------------------------------------------------

    def cash_breakdown(self, conn, where="", params=None):

        if params is None:
            params = []

        rows = conn.execute(
            f"""
            SELECT
                subaccount,
                SUM(balance)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} account='Cash & Cash Equivalents'
            GROUP BY
                subaccount
            ORDER BY
                SUM(balance) DESC
            """
            ,
            params,
        ).fetchall()

        return [

            {

                "account": account,

                "amount": float(amount),

            }

            for account, amount in rows

        ]