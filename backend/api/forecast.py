from fastapi import APIRouter

from backend.services.forecast_service import ForecastService

router = APIRouter(
    prefix="/api/forecast",
    tags=["Forecast"],
)


@router.get("")
def get_forecast(
    year: int,
    country: str | None = None,
    growth_rate_override: float | None = None,
):

    service = ForecastService()

    try:

        return service.get_forecast(
            year,
            country,
            growth_rate_override,
        )

    finally:

        service.close()
