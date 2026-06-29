from pathlib import Path

import duckdb

DB_PATH = Path(__file__).resolve().parents[3] / "database" / "finsight.duckdb"


class KPIService:

    def __init__(self):
        self.conn = duckdb.connect(DB_PATH)

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
            clauses.append("year=?")
            params.append(year)

        if quarter:
            clauses.append("quarter=?")
            params.append(quarter)

        if month:
            clauses.append("month=?")
            params.append(month)

        if country:
            clauses.append("country=?")
            params.append(country)

        where = ""

        if clauses:
            where = " WHERE " + " AND ".join(clauses)

        return where, params

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

        return {
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "cash": cash,
        }

    def close(self):
        self.conn.close()
