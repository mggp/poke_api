from fastapi import APIRouter, Depends
from app.models import BerryStatsResponse
from app.services.pokebase_client import BerryClient
from app.utils.stats import calculate_stats

router = APIRouter()


@router.get("/allBerryStats")
def all_berry_stats() -> BerryStatsResponse:
    
    client = BerryClient(base_url="https://pokeapi.co/api/v2") # TODO: Use environment variable for base_url
    berries = client.get_all_details()
    names = [berry.name for berry in berries]
    growth_times = [berry.growth_time for berry in berries]
    growth_time_stats = calculate_stats(growth_times)
       
    return BerryStatsResponse(
        berries_names=names,
        min_growth_time=growth_time_stats["min"],
        median_growth_time=growth_time_stats["median"],
        max_growth_time=growth_time_stats["max"],
        variance_growth_time=growth_time_stats["variance"],
        mean_growth_time=growth_time_stats["mean"],
        frequency_growth_time=growth_time_stats["frequency"]
    )
