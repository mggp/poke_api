

from typing import Dict, List
from pydantic import BaseModel


class BerryStatsResponse(BaseModel):
    berries_names: List[str]
    min_growth_time: int
    median_growth_time: float
    max_growth_time: int
    variance_growth_time: float
    mean_growth_time: float
    frequency_growth_time: Dict[str, int]