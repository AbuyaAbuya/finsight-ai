import duckdb
import pandas as pd

DB_PATH = "database/finsight.duckdb"


class FinancialService:

    def __init__(self):
        self.conn = duckdb.connect(DB_PATH)

    # ---------------------------------------------------------
    # Trial Balance
    # ---------------------------------------------------------

    def trial_balance(self):

        return self.conn.execute("""

            SELECT *

            FROM TrialBalance

            ORDER BY

                year,
                month_number,
                account_key

        """).fetchdf()

    # ---------------------------------------------------------
    # Income Statement
    # ---------------------------------------------------------

    def income_statement(self):

        return self.conn.execute("""

            SELECT

                year,
                quarter,
                month,
                country,

                subclass,
                subclass2,
                account,
                subaccount,

                SUM(balance) balance

            FROM FinancialReportingMart

            WHERE report='Profit and Loss'

            GROUP BY

                year,
                quarter,
                month,
                country,

                subclass,
                subclass2,
                account,
                subaccount

            ORDER BY

                year,
                month,
                subclass

        """).fetchdf()

    # ---------------------------------------------------------
    # Balance Sheet
    # ---------------------------------------------------------

    def balance_sheet(self):

        return self.conn.execute("""

            SELECT

                year,
                quarter,
                month,
                country,

                subclass,
                subclass2,
                account,
                subaccount,

                SUM(balance) balance

            FROM FinancialReportingMart

            WHERE report='Balance Sheet'

            GROUP BY

                year,
                quarter,
                month,
                country,

                subclass,
                subclass2,
                account,
                subaccount

            ORDER BY

                year,
                month,
                subclass

        """).fetchdf()

    # ---------------------------------------------------------
    # KPI Summary
    # ---------------------------------------------------------

    def kpis(self):

        return self.conn.execute("""

            SELECT

                COUNT(*)                    AS rows,

                SUM(balance)                AS balance,

                SUM(debit)                  AS debit,

                SUM(credit)                 AS credit,

                SUM(transactions)           AS transactions

            FROM FinancialReportingMart

        """).fetchdf()

    # ---------------------------------------------------------
    # Countries
    # ---------------------------------------------------------

    def countries(self):

        return self.conn.execute("""

            SELECT DISTINCT

                country

            FROM FinancialReportingMart

            ORDER BY country

        """).fetchdf()

    # ---------------------------------------------------------
    # Years
    # ---------------------------------------------------------

    def years(self):

        return self.conn.execute("""

            SELECT DISTINCT

                year

            FROM FinancialReportingMart

            ORDER BY year

        """).fetchdf()

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(self):
        self.conn.close()