from pathlib import Path

import duckdb

DB_PATH = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "finsight.duckdb"
)

CREDIT_NORMAL_ACCOUNTS = {
    "Sales",
    "Interest Income",
    "Dividend Income",
    "Gain/Loss on Sales of Asset",
    "Exchange Loss/Gain",
}

FORECASTABLE_ACCOUNTS = [
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

EXPENSE_ACCOUNTS = [
    a for a in FORECASTABLE_ACCOUNTS
    if a not in CREDIT_NORMAL_ACCOUNTS and a != "Sales Return"
]


class ForecastService:
    """
    Projects future performance using a trend + seasonality method:

      1. Growth rate: average year-over-year growth in each account's
         ANNUAL total, across every consecutive pair of years available
         (e.g. 2018->2019 and 2019->2020 averaged), applied to the most
         recent full year to get a forecasted annual total.
      2. Seasonal index: each month's historical average share of the
         annual total (relative to an even 1/12 split), applied to
         spread the forecasted annual total back across 12 months.

    This is a standard, transparent FP&A forecasting approach -- not a
    black box -- and every assumption (growth rate, seasonal index) is
    returned alongside the forecast so it can be inspected or overridden.
    """

    def __init__(self):
        self.conn = duckdb.connect(DB_PATH)

    def _actuals_by_year_month_account(self, country=None):

        clauses = ["report = 'Profit and Loss'"]
        params = []

        if country:
            clauses.append("country = ?")
            params.append(country)

        where = " WHERE " + " AND ".join(clauses)

        rows = self.conn.execute(
            f"""
            SELECT year, month_number, month, account, SUM(balance) AS balance
            FROM FinancialReportingMart
            {where}
            GROUP BY year, month_number, month, account
            """,
            params,
        ).fetchall()

        result = {}

        for year, month_number, month, account, balance in rows:
            display = -balance if account in CREDIT_NORMAL_ACCOUNTS else balance
            result[(year, month_number, account)] = {
                "month": month,
                "amount": float(display),
            }

        return result

    def get_forecast(self, target_year, country=None, growth_rate_override=None):

        actuals = self._actuals_by_year_month_account(country)

        available_years = sorted({y for (y, m, a) in actuals.keys()})
        base_year = target_year - 1

        month_lookup = self.conn.execute(
            """
            SELECT DISTINCT month, month_number
            FROM FinancialReportingMart
            ORDER BY month_number
            """
        ).fetchall()

        if base_year not in available_years:
            return {
                "has_history": False,
                "forecast": [],
                "assumptions": [],
                "historical": [],
            }

        assumptions = []
        forecast_rows = []

        for account in FORECASTABLE_ACCOUNTS:

            # Annual totals for every available year, for this account.
            annual_totals = {}
            for year in available_years:
                total = sum(
                    actuals.get((year, m, account), {}).get("amount", 0.0)
                    for m, _mn in [(mn, mn) for mn in range(1, 13)]
                )
                annual_totals[year] = total

            # Growth rate: average YoY growth across every consecutive
            # pair of years with non-zero prior-year totals.
            growth_rates = []
            sorted_years = sorted(available_years)
            for prev_y, cur_y in zip(sorted_years, sorted_years[1:]):
                prev_total = annual_totals.get(prev_y, 0)
                cur_total = annual_totals.get(cur_y, 0)
                if prev_total:
                    growth_rates.append((cur_total - prev_total) / prev_total)

            computed_growth_rate = (
                sum(growth_rates) / len(growth_rates) if growth_rates else 0.0
            )

            growth_rate = (
                growth_rate_override
                if growth_rate_override is not None
                else computed_growth_rate
            )

            base_annual = annual_totals.get(base_year, 0.0)
            forecast_annual = base_annual * (1 + growth_rate)

            # Seasonal index: each month's historical average share of
            # the annual total, relative to an even 1/12 split.
            monthly_avgs = {}
            for month_number in range(1, 13):
                vals = [
                    actuals.get((y, month_number, account), {}).get("amount", 0.0)
                    for y in available_years
                ]
                monthly_avgs[month_number] = sum(vals) / len(vals) if vals else 0.0

            avg_month = sum(monthly_avgs.values()) / 12 if monthly_avgs else 0.0

            seasonal_index = {
                m: (v / avg_month if avg_month else 1 / 12)
                for m, v in monthly_avgs.items()
            }

            assumptions.append({
                "account": account,
                "growth_rate": round(growth_rate * 100, 1),
                "base_year": base_year,
                "base_annual": round(base_annual, 2),
                "forecast_annual": round(forecast_annual, 2),
            })

            for month, month_number in month_lookup:
                monthly_forecast = (forecast_annual / 12) * seasonal_index.get(month_number, 1 / 12)

                forecast_rows.append({
                    "account": account,
                    "month": month,
                    "month_number": month_number,
                    "year": target_year,
                    "forecast": round(monthly_forecast, 2),
                })

        # Trailing historical actuals (most recent available year) for
        # chart continuity into the forecast period.
        historical_rows = []
        for month, month_number in month_lookup:
            for account in FORECASTABLE_ACCOUNTS:
                amount = actuals.get((base_year, month_number, account), {}).get("amount", 0.0)
                historical_rows.append({
                    "account": account,
                    "month": month,
                    "month_number": month_number,
                    "year": base_year,
                    "actual": round(amount, 2),
                })

        return {
            "has_history": True,
            "base_year": base_year,
            "forecast": forecast_rows,
            "historical": historical_rows,
            "assumptions": assumptions,
        }

    def close(self):
        self.conn.close()
