from pathlib import Path

import duckdb

from backend.analytics.gl_analyzer import GLAnalyzer
from backend.analytics.insights_engine import InsightsEngine

DB_PATH = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "finsight.duckdb"
)


class DashboardService:

    def __init__(self):

        self.conn = duckdb.connect(DB_PATH)

    # ============================================================
    # FILTER BUILDER
    # ============================================================

    def build_where(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        clauses = []
        params = []

        if year:
            clauses.append("year = ?")
            params.append(year)

        if quarter:
            clauses.append("quarter = ?")
            params.append(quarter)

        if month:
            clauses.append("month = ?")
            params.append(month)

        if country:
            clauses.append("country = ?")
            params.append(country)

        where = ""

        if clauses:
            where = " WHERE " + " AND ".join(clauses)

        return where, params

    # ============================================================
    # KPI ENGINE
    # ============================================================

    def get_kpis(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        # -------------------------------------------------------
        # Current Period KPIs
        # -------------------------------------------------------

        revenue = self.conn.execute(
            f"""
            SELECT COALESCE(SUM(balance),0)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} subaccount='Sales'
            """,
            params,
        ).fetchone()[0]

        expenses = self.conn.execute(
            f"""
            SELECT COALESCE(SUM(ABS(balance)),0)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} report='Profit and Loss'
            AND balance < 0
            """,
            params,
        ).fetchone()[0]

        profit = self.conn.execute(
            f"""
            SELECT COALESCE(SUM(balance),0)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} subaccount='Retained Earnings'
            """,
            params,
        ).fetchone()[0]

        cash = self.conn.execute(
            f"""
            SELECT COALESCE(SUM(balance),0)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} account='Cash & Cash Equivalents'
            """,
            params,
        ).fetchone()[0]

        # -------------------------------------------------------
        # Previous Year Filter
        # -------------------------------------------------------

        previous_year = None

        if year:
            previous_year = year - 1
        else:
            row = self.conn.execute(
                """
                SELECT MAX(year)
                FROM FinancialReportingMart
                """
            ).fetchone()

            if row and row[0]:
                previous_year = row[0] - 1

        previous_revenue = 0
        previous_expenses = 0
        previous_profit = 0
        previous_cash = 0

        if previous_year:

            previous_where, previous_params = self.build_where(
                previous_year,
                quarter,
                month,
                country,
            )

            previous_revenue = self.conn.execute(
                f"""
                SELECT COALESCE(SUM(balance),0)
                FROM FinancialReportingMart
                {previous_where}
                {"AND" if previous_where else "WHERE"} subaccount='Sales'
                """,
                previous_params,
            ).fetchone()[0]

            previous_expenses = self.conn.execute(
                f"""
                SELECT COALESCE(SUM(ABS(balance)),0)
                FROM FinancialReportingMart
                {previous_where}
                {"AND" if previous_where else "WHERE"} report='Profit and Loss'
                AND balance < 0
                """,
                previous_params,
            ).fetchone()[0]

            previous_profit = self.conn.execute(
                f"""
                SELECT COALESCE(SUM(balance),0)
                FROM FinancialReportingMart
                {previous_where}
                {"AND" if previous_where else "WHERE"} subaccount='Retained Earnings'
                """,
                previous_params,
            ).fetchone()[0]

            previous_cash = self.conn.execute(
                f"""
                SELECT COALESCE(SUM(balance),0)
                FROM FinancialReportingMart
                {previous_where}
                {"AND" if previous_where else "WHERE"} account='Cash & Cash Equivalents'
                """,
                previous_params,
            ).fetchone()[0]
            # -------------------------------------------------------
        # Helper
        # -------------------------------------------------------

        def build_metric(current, previous, positive_when_up=True):

            if previous == 0:

                return {
                    "value": float(current),
                    "change": 0,
                    "direction": "neutral",
                    "comparison": "Previous Year",
                    "message": "No previous-year data available.",
                }

            change = ((current - previous) / abs(previous)) * 100

            if abs(change) < 0.01:
                direction = "neutral"

            elif change > 0:
                direction = "up"

            else:
                direction = "down"

            if positive_when_up:

                if direction == "up":
                    message = f"Increased by {abs(change):.1f}% vs previous year."
                elif direction == "down":
                    message = f"Decreased by {abs(change):.1f}% vs previous year."
                else:
                    message = "No change from previous year."

            else:

                if direction == "down":
                    message = f"Reduced by {abs(change):.1f}% vs previous year."
                elif direction == "up":
                    message = f"Increased by {abs(change):.1f}% vs previous year."
                else:
                    message = "No change from previous year."

            return {
                "value": float(current),
                "change": round(abs(change), 1),
                "direction": direction,
                "comparison": "Previous Year",
                "message": message,
            }

        # -------------------------------------------------------
        # Return
        # -------------------------------------------------------

        return {

            "revenue": build_metric(
                revenue,
                previous_revenue,
                True,
            ),

            "expenses": build_metric(
                expenses,
                previous_expenses,
                False,
            ),

            "profit": build_metric(
                profit,
                previous_profit,
                True,
            ),

            "cash": build_metric(
                cash,
                previous_cash,
                True,
            ),

        }

    # ============================================================
    # FILTERS
    # ============================================================

    def get_filters(self):

        return {

            "years": [
                r[0]
                for r in self.conn.execute(
                    """
                    SELECT DISTINCT year
                    FROM FinancialReportingMart
                    ORDER BY year
                    """
                ).fetchall()
            ],

            "quarters": [
                r[0]
                for r in self.conn.execute(
                    """
                    SELECT DISTINCT quarter
                    FROM FinancialReportingMart
                    ORDER BY quarter
                    """
                ).fetchall()
            ],

            "months": [
                r[0]
                for r in self.conn.execute(
                    """
                    SELECT DISTINCT month
                    FROM FinancialReportingMart
                    ORDER BY month_number
                    """
                ).fetchall()
            ],

            "countries": [
                r[0]
                for r in self.conn.execute(
                    """
                    SELECT DISTINCT country
                    FROM FinancialReportingMart
                    ORDER BY country
                    """
                ).fetchall()
            ],

        }

    # ============================================================
    # REVENUE TREND
    # ============================================================

    def get_revenue_trend(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        rows = self.conn.execute(
            f"""
            SELECT
                month,
                month_number,
                SUM(balance) AS revenue
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} subaccount='Sales'
            GROUP BY
                month,
                month_number
            ORDER BY
                month_number
            """,
            params,
        ).fetchall()

        return [

            {
                "month": row[0],
                "month_number": row[1],
                "revenue": float(row[2]),
            }

            for row in rows

        ]

    # ============================================================
    # EXPENSE TREND
    # ============================================================

    def get_expense_trend(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        rows = self.conn.execute(
            f"""
            SELECT
                month,
                month_number,
                SUM(ABS(balance)) AS expenses
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} report='Profit and Loss'
            AND balance < 0
            GROUP BY
                month,
                month_number
            ORDER BY
                month_number
            """,
            params,
        ).fetchall()

        return [

            {
                "month": row[0],
                "month_number": row[1],
                "expenses": float(row[2]),
            }

            for row in rows

        ]

    # ============================================================
    # DASHBOARD
    # ============================================================

    def get_dashboard(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        # ----------------------------------------------------------
        # KPI Metrics
        # ----------------------------------------------------------

        kpis = self.get_kpis(
            year,
            quarter,
            month,
            country,
        )

        # ----------------------------------------------------------
        # Charts
        # ----------------------------------------------------------

        revenue_trend = self.get_revenue_trend(
            year,
            quarter,
            month,
            country,
        )

        expense_trend = self.get_expense_trend(
            year,
            quarter,
            month,
            country,
        )

        # ----------------------------------------------------------
        # GL Analysis
        # ----------------------------------------------------------

        where, params = self.build_where(
            year,
            quarter,
            month,
            country,
        )

        analyzer = GLAnalyzer()

        revenue_drivers = analyzer.top_revenue_drivers(
            self.conn,
            where,
            params,
        )

        expense_drivers = analyzer.top_expense_drivers(
            self.conn,
            where,
            params,
        )

        cash_breakdown = analyzer.cash_breakdown(
            self.conn,
            where,
            params,
        )

        # ----------------------------------------------------------
        # Executive Insights
        # ----------------------------------------------------------

        insights = InsightsEngine().generate(
            revenue_trend=revenue_trend,
            expense_trend=expense_trend,
            kpis=kpis,
        )

        # ----------------------------------------------------------
        # Dashboard Response
        # ----------------------------------------------------------

        return {

            "filters": self.get_filters(),

            "kpis": kpis,

            "revenueTrend": revenue_trend,

            "expenseTrend": expense_trend,

            "revenueDrivers": revenue_drivers,

            "expenseDrivers": expense_drivers,

            "cashBreakdown": cash_breakdown,

            "insights": insights,

        }

    # ============================================================
    # CLOSE CONNECTION
    # ============================================================

    def close(self):

        self.conn.close()