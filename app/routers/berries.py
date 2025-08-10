from fastapi import APIRouter, HTTPException
from httpx import HTTPError

from app.config import settings
from app.models import BerryStatsResponse
from app.services.pokebase_client import BerryClient
from app.utils.stats import calculate_stats

router = APIRouter()


@router.get("/allBerryStats")
async def all_berry_stats() -> BerryStatsResponse:
    """Retrieve berry info and compute statistics on their growth times."""

    client = BerryClient(base_url=settings.poke_api_path)

    try:
        # TODO: cache this data
        berries = await client.get_all_details()
    except HTTPError as e:
        # Log the error here if needed
        raise HTTPException(
            status_code=500, detail="Failed to fetch berry details from the PokéAPI"
        ) from e

    if not berries:
        return BerryStatsResponse()

    names = [berry.name for berry in berries]
    growth_times = [berry.growth_time for berry in berries]
    growth_time_stats = calculate_stats(growth_times)

    return BerryStatsResponse(
        berries_names=names,
        min_growth_time=growth_time_stats.min,
        median_growth_time=growth_time_stats.median,
        max_growth_time=growth_time_stats.max,
        variance_growth_time=growth_time_stats.variance,
        mean_growth_time=growth_time_stats.mean,
        frequency_growth_time=growth_time_stats.frequency,
    )
