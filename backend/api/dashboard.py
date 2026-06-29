from pathlib import Path

import duckdb
from fastapi import APIRouter

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

DB_PATH = Path(__file__).resolve().parents[2] / "database" / "finsight.duckdb"


@router.get("/kpis")
def get_dashboard_kpis():

    conn = duckdb.connect(DB_PATH)

    revenue = conn.execute("""
        SELECT COALESCE(SUM(balance),0)
        FROM FinancialReportingMart
        WHERE subaccount='Sales'
    """).fetchone()[0]

    expenses = conn.execute("""
        SELECT COALESCE(SUM(ABS(balance)),0)
        FROM FinancialReportingMart
        WHERE report='Profit and Loss'
          AND balance < 0
    """).fetchone()[0]

    profit = conn.execute("""
        SELECT COALESCE(SUM(balance),0)
        FROM FinancialReportingMart
        WHERE subaccount='Retained Earnings'
    """).fetchone()[0]

    cash = conn.execute("""
        SELECT COALESCE(SUM(balance),0)
        FROM FinancialReportingMart
        WHERE account='Cash & Cash Equivalents'
    """).fetchone()[0]

    conn.close()

    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "cash": cash,
    }