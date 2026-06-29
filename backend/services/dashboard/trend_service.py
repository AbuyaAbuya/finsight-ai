from pathlib import Path

import duckdb

DB_PATH = Path(__file__).resolve().parents[3] / "database" / "finsight.duckdb"


class TrendService:

    def __init__(self):
        self.conn = duckdb.connect(DB_PATH)

    def get_revenue_trend(
        self,
        year=None,
        quarter=None,
        month=None,
        country=None,
    ):

        conditions = ["subaccount = 'Sales'"]
        params = []

        if year:
            conditions.append("year = ?")
            params.append(year)

        if quarter:
            conditions.append("quarter = ?")
            params.append(quarter)

        if month:
            conditions.append("month = ?")
            params.append(month)

        if country:
            conditions.append("country = ?")
            params.append(country)

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT
                month,
                month_number,
                SUM(balance) AS revenue
            FROM FinancialReportingMart
            WHERE {where_clause}
            GROUP BY month, month_number
            ORDER BY month_number
        """

        rows = self.conn.execute(query, params).fetchall()

        return [
            {
                "month": row[0],
                "month_number": row[1],
                "revenue": float(row[2]),
            }
            for row in rows
        ]

    def close(self):
        self.conn.close()
