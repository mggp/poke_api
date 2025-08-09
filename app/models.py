from typing import Dict, List

from pydantic import BaseModel


class BerryStatsResponse(BaseModel):
    berries_names: List[str] = []
    min_growth_time: int = None
    median_growth_time: float = None
    max_growth_time: int = None
    variance_growth_time: float = None
    mean_growth_time: float = None
    frequency_growth_time: Dict[int, int] = {}
