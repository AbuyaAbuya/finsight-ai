from fastapi import APIRouter, Query

from backend.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def get_dashboard(
    year: int | None = Query(None),
    quarter: str | None = Query(None),
    month: str | None = Query(None),
    country: str | None = Query(None),
):

    service = DashboardService()

    try:
        return service.get_dashboard(
            year=year,
            quarter=quarter,
            month=month,
            country=country,
        )
    finally:
        service.close()


@router.get("/kpis")
def get_dashboard_kpis(
    year: int | None = Query(None),
    quarter: str | None = Query(None),
    month: str | None = Query(None),
    country: str | None = Query(None),
):

    service = DashboardService()

    try:
        return service.get_kpis(
            year=year,
            quarter=quarter,
            month=month,
            country=country,
        )
    finally:
        service.close()


@router.get("/revenue-trend")
def get_revenue_trend(
    year: int | None = Query(None),
    quarter: str | None = Query(None),
    month: str | None = Query(None),
    country: str | None = Query(None),
):

    service = DashboardService()

    try:
        return service.get_revenue_trend(
            year=year,
            quarter=quarter,
            month=month,
            country=country,
        )
    finally:
        service.close()