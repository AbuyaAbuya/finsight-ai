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
    # CUMULATIVE FILTER BUILDER (for point-in-time balances, e.g.
    # Cash -- unlike Revenue/Expenses/Profit, which are legitimate
    # period-flow metrics, Cash is a balance that should always be
    # cumulative-to-date, not summed only over the selected period.
    # Same validated pattern used in financial_service.py.
    # ============================================================

    def build_cumulative_where(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
        upper_bound_exclusive=False,
    ):

        clauses = []
        params = []

        if year:
            if month:
                cmp_op = "<" if upper_bound_exclusive else "<="
                clauses.append(
                    f"""
                    (year < ? OR (year = ? AND month_number {cmp_op} (
                        SELECT MIN(month_number) FROM FinancialReportingMart
                        WHERE month = ?
                    )))
                    """
                )
                params.extend([year, year, month])
            elif quarter:
                cmp_op = "<" if upper_bound_exclusive else "<="
                clauses.append(
                    f"""
                    (year < ? OR (year = ? AND
                        CAST(TRIM(REPLACE(quarter, 'Qtr', '')) AS INTEGER)
                        {cmp_op} CAST(TRIM(REPLACE(?, 'Qtr', '')) AS INTEGER)
                    ))
                    """
                )
                params.extend([year, year, quarter])
            else:
                cmp_op = "<" if upper_bound_exclusive else "<="
                clauses.append(f"year {cmp_op} ?")
                params.append(year)
        elif quarter:
            clauses.append("quarter = ?")
            params.append(quarter)
        elif month:
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
            SELECT COALESCE(-SUM(balance),0)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} subaccount='Sales'
            """,
            params,
        ).fetchone()[0]

        expenses = self.conn.execute(
            f"""
            SELECT COALESCE(SUM(balance),0)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} report='Profit and Loss'
            AND balance > 0
            """,
            params,
        ).fetchone()[0]

        profit = self.conn.execute(
            f"""
            SELECT COALESCE(-SUM(balance),0)
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} subaccount='Retained Earnings'
            """,
            params,
        ).fetchone()[0]

        cumulative_where, cumulative_params = self.build_cumulative_where(
            year,
            quarter,
            month,
            country,
        )

        cash = self.conn.execute(
            f"""
            SELECT COALESCE(SUM(balance),0)
            FROM FinancialReportingMart
            {cumulative_where}
            {"AND" if cumulative_where else "WHERE"} account='Cash & Cash Equivalents'
            """,
            cumulative_params,
        ).fetchone()[0]

        # -------------------------------------------------------
        # Previous Year Filter
        #
        # A previous-year comparison is only meaningful when a
        # specific year is selected. When "All Years" is selected,
        # the current period is already a multi-year aggregate, so
        # there is no single coherent "previous year" to compare it
        # against -- fabricating one (e.g. against the latest year
        # in the data) produces misleading percentages, comparing a
        # multi-year total against a single year's figure.
        # -------------------------------------------------------

        previous_year = year - 1 if year else None
        comparison_available = previous_year is not None

        previous_revenue = 0
        previous_expenses = 0
        previous_profit = 0
        previous_cash = 0

        # -------------------------------------------------------
        # Recent trend hint (only when no year is selected): find
        # the two most recent years that match the current
        # quarter/month/country filter, and compute a small,
        # clearly-labeled auxiliary comparison -- distinct from the
        # main (aggregate) value shown on the card, and NOT used as
        # if it were "vs previous year" for that aggregate.
        # -------------------------------------------------------

        recent_trend_by_metric = {}

        if not comparison_available:

            qm_where, qm_params = self.build_where(None, quarter, month, country)

            max_year_row = self.conn.execute(
                f"SELECT MAX(year) FROM FinancialReportingMart {qm_where}",
                qm_params,
            ).fetchone()

            auto_year = max_year_row[0] if max_year_row and max_year_row[0] else None

            if auto_year:

                auto_prev_year = auto_year - 1

                def metrics_for_year(y):
                    y_where, y_params = self.build_where(y, quarter, month, country)
                    y_cum_where, y_cum_params = self.build_cumulative_where(
                        y, quarter, month, country
                    )

                    rev = self.conn.execute(
                        f"""SELECT COALESCE(-SUM(balance),0) FROM FinancialReportingMart
                        {y_where} {"AND" if y_where else "WHERE"} subaccount='Sales'""",
                        y_params,
                    ).fetchone()[0]

                    exp = self.conn.execute(
                        f"""SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart
                        {y_where} {"AND" if y_where else "WHERE"} report='Profit and Loss'
                        AND balance > 0""",
                        y_params,
                    ).fetchone()[0]

                    prof = self.conn.execute(
                        f"""SELECT COALESCE(-SUM(balance),0) FROM FinancialReportingMart
                        {y_where} {"AND" if y_where else "WHERE"} subaccount='Retained Earnings'""",
                        y_params,
                    ).fetchone()[0]

                    csh = self.conn.execute(
                        f"""SELECT COALESCE(SUM(balance),0) FROM FinancialReportingMart
                        {y_cum_where} {"AND" if y_cum_where else "WHERE"} account='Cash & Cash Equivalents'""",
                        y_cum_params,
                    ).fetchone()[0]

                    return {"revenue": rev, "expenses": exp, "profit": prof, "cash": csh}

                current_metrics = metrics_for_year(auto_year)
                prior_metrics = metrics_for_year(auto_prev_year)

                insight_templates = {
                    "revenue": {
                        "up": "Revenue grew {pct:.1f}% in {y} vs {py} — sustain the momentum with continued investment in top-performing channels.",
                        "down": "Revenue fell {pct:.1f}% in {y} vs {py} — investigate demand drivers before committing to new spend.",
                        "flat": "Revenue was flat in {y} vs {py} — look for new growth levers.",
                    },
                    "expenses": {
                        "up": "Expenses rose {pct:.1f}% in {y} vs {py} — review cost efficiency before the next period.",
                        "down": "Expenses fell {pct:.1f}% in {y} vs {py} — cost discipline is improving.",
                        "flat": "Expenses held steady in {y} vs {py}.",
                    },
                    "profit": {
                        "up": "Profit improved {pct:.1f}% in {y} vs {py} — a good window to reinvest surplus strategically.",
                        "down": "Profit declined {pct:.1f}% in {y} vs {py} — reassess cost structure or pricing.",
                        "flat": "Profit was flat in {y} vs {py}.",
                    },
                    "cash": {
                        "up": "Cash position strengthened {pct:.1f}% in {y} vs {py}.",
                        "down": "Cash position weakened {pct:.1f}% in {y} vs {py} — monitor liquidity closely.",
                        "flat": "Cash position was stable in {y} vs {py}.",
                    },
                }

                for metric_key in ["revenue", "expenses", "profit", "cash"]:
                    cur_val = current_metrics[metric_key]
                    prior_val = prior_metrics[metric_key]

                    if prior_val == 0:
                        continue

                    pct = ((cur_val - prior_val) / abs(prior_val)) * 100

                    if abs(pct) < 0.01:
                        trend_dir = "flat"
                    elif pct > 0:
                        trend_dir = "up"
                    else:
                        trend_dir = "down"

                    insight = insight_templates[metric_key][trend_dir].format(
                        pct=abs(pct), y=auto_year, py=auto_prev_year
                    )

                    recent_trend_by_metric[metric_key] = {
                        "latest_year": auto_year,
                        "latest_value": float(cur_val),
                        "prior_year": auto_prev_year,
                        "prior_value": float(prior_val),
                        "change_pct": round(abs(pct), 1),
                        "direction": trend_dir,
                        "insight": insight,
                    }

        if previous_year:

            previous_where, previous_params = self.build_where(
                previous_year,
                quarter,
                month,
                country,
            )

            previous_revenue = self.conn.execute(
                f"""
                SELECT COALESCE(-SUM(balance),0)
                FROM FinancialReportingMart
                {previous_where}
                {"AND" if previous_where else "WHERE"} subaccount='Sales'
                """,
                previous_params,
            ).fetchone()[0]

            previous_expenses = self.conn.execute(
                f"""
                SELECT COALESCE(SUM(balance),0)
                FROM FinancialReportingMart
                {previous_where}
                {"AND" if previous_where else "WHERE"} report='Profit and Loss'
                AND balance > 0
                """,
                previous_params,
            ).fetchone()[0]

            previous_profit = self.conn.execute(
                f"""
                SELECT COALESCE(-SUM(balance),0)
                FROM FinancialReportingMart
                {previous_where}
                {"AND" if previous_where else "WHERE"} subaccount='Retained Earnings'
                """,
                previous_params,
            ).fetchone()[0]

            # Cash is a point-in-time balance, not a period flow, so
            # its year-over-year comparison uses the cumulative
            # balance as of the same point one year earlier -- not
            # "previous year's period-exact movement" like the flow
            # metrics above.
            previous_cash_where, previous_cash_params = self.build_cumulative_where(
                previous_year,
                quarter,
                month,
                country,
            )

            previous_cash = self.conn.execute(
                f"""
                SELECT COALESCE(SUM(balance),0)
                FROM FinancialReportingMart
                {previous_cash_where}
                {"AND" if previous_cash_where else "WHERE"} account='Cash & Cash Equivalents'
                """,
                previous_cash_params,
            ).fetchone()[0]

        # -------------------------------------------------------
        # Helper
        # -------------------------------------------------------

        def build_metric(current, previous, positive_when_up=True, metric_key=None):

            if not comparison_available:

                result = {
                    "value": float(current),
                    "change": 0,
                    "direction": "neutral",
                    "comparison": "Previous Year",
                    "message": "Select a specific year to see a year-over-year comparison.",
                }

                if metric_key and metric_key in recent_trend_by_metric:
                    result["recentTrend"] = recent_trend_by_metric[metric_key]

                return result

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
                "revenue",
            ),

            "expenses": build_metric(
                expenses,
                previous_expenses,
                False,
                "expenses",
            ),

            "profit": build_metric(
                profit,
                previous_profit,
                True,
                "profit",
            ),

            "cash": build_metric(
                cash,
                previous_cash,
                True,
                "cash",
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
                -SUM(balance) AS revenue
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
                SUM(balance) AS expenses
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} report='Profit and Loss'
            AND balance > 0
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
    # PROFIT TREND
    #
    # Uses the exact same account (subaccount='Retained Earnings')
    # as the Net Profit KPI, so the chart and the KPI card can never
    # disagree. Deliberately NOT computed as revenue-minus-expenses
    # client-side, since Revenue trend only covers Sales and Expense
    # trend only covers debit-positive P&L accounts -- non-operating
    # income (Interest Income, Dividend Income, Gains) falls through
    # both and would be silently dropped from a derived figure.
    # ============================================================

    def get_profit_trend(
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
                -SUM(balance) AS profit
            FROM FinancialReportingMart
            {where}
            {"AND" if where else "WHERE"} subaccount='Retained Earnings'
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
                "profit": float(row[2]),
            }

            for row in rows

        ]

    # ============================================================
    # PERFORMANCE BY COUNTRY
    #
    # Always breaks out ALL countries regardless of the country
    # filter, since narrowing to one country would make a
    # geographic comparison trivial. Year/quarter/month filters
    # still apply normally.
    # ============================================================

    def get_country_performance(
        self,
        year=None,
        quarter=None,
        month=None,
    ):

        where, params = self.build_where(
            year,
            quarter,
            month,
            None,
        )

        rows = self.conn.execute(
            f"""
            SELECT
                country,
                -SUM(CASE WHEN subaccount='Sales' THEN balance ELSE 0 END) AS revenue,
                SUM(CASE WHEN report='Profit and Loss' AND balance > 0
                    THEN balance ELSE 0 END) AS expenses,
                -SUM(CASE WHEN subaccount='Retained Earnings'
                    THEN balance ELSE 0 END) AS profit
            FROM FinancialReportingMart
            {where}
            GROUP BY country
            ORDER BY revenue DESC
            """,
            params,
        ).fetchall()

        return [

            {
                "country": row[0],
                "revenue": float(row[1]),
                "expenses": float(row[2]),
                "profit": float(row[3]),
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

        profit_trend = self.get_profit_trend(
            year,
            quarter,
            month,
            country,
        )

        country_performance = self.get_country_performance(
            year,
            quarter,
            month,
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
            true_total=kpis["revenue"]["value"],
        )

        expense_drivers = analyzer.top_expense_drivers(
            self.conn,
            where,
            params,
            true_total=kpis["expenses"]["value"],
        )

        cumulative_where, cumulative_params = self.build_cumulative_where(
            year,
            quarter,
            month,
            country,
        )

        cash_breakdown = analyzer.cash_breakdown(
            self.conn,
            cumulative_where,
            cumulative_params,
        )

        # ----------------------------------------------------------
        # Executive Insights
        # ----------------------------------------------------------

        insights = InsightsEngine().generate(
            revenue_trend=revenue_trend,
            expense_trend=expense_trend,
            profit_trend=profit_trend,
            expense_drivers=expense_drivers,
            country_performance=country_performance,
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

            "profitTrend": profit_trend,

            "countryPerformance": country_performance,

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