import base64
from typing import List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from httpx import HTTPError

from app.config import settings
from app.constants import ALL_BERRIES_CACHE_KEY, JINJA_TEMPLATES_DIR
from app.models import BerryStatsResponse
from app.services.pokebase_client import BerryClient
from app.services.schemas import Berry
from app.utils import cache, plots
from app.utils.stats import calculate_stats, get_frequencies

router = APIRouter()

templates = Jinja2Templates(directory=JINJA_TEMPLATES_DIR)


@cache.cache(ALL_BERRIES_CACHE_KEY)
async def get_berries() -> List[Berry]:
    client = BerryClient(base_url=settings.poke_api_path)

    try:
        berries = await client.get_all_details()
    except HTTPError as e:
        # Log the error here if needed
        raise HTTPException(
            status_code=500, detail="Failed to fetch berry details from the PokéAPI"
        ) from e

    return berries


@router.get("/allBerryStats")
async def all_berry_stats() -> BerryStatsResponse:
    """Retrieve berry info and compute statistics on their growth times."""

    berries = await get_berries()

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


@router.get("/growthTimeGraphs", response_class=HTMLResponse)
async def growth_time_graphs(request: Request) -> HTMLResponse:
    """Render a simple HTML page for growth time graphs."""

    berries = await get_berries()

    if not berries:
        return templates.TemplateResponse(
            name="growth_time_graphs.html",
            request=request,
        )

    growth_times = [berry.growth_time for berry in berries]
    frequency = get_frequencies(growth_times)

    plot_bytes = plots.get_histogram(
        frequency,
        xlabel="Growth Time [hours]",
        ylabel="Frequency",
    )
    histogram_data = base64.b64encode(plot_bytes).decode("utf-8")

    return templates.TemplateResponse(
        name="growth_time_graphs.html",
        request=request,
        context={"histogram_data": histogram_data},
    )
