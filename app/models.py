from typing import Dict, List

from pydantic import AfterValidator, BaseModel
from typing_extensions import Annotated

from app.config import settings


def round_float(value: float) -> float:
    """Round a float to the number of decimal places defined in settings.
    If no decimal places are set, return the value unchanged.
    """

    decimal_places = settings.float_decimal_places

    if decimal_places is None:
        return value

    return round(value, decimal_places)


HumanReadableFloat = Annotated[float, AfterValidator(round_float)]


class BerryStatsResponse(BaseModel):
    berries_names: List[str] = []
    min_growth_time: int = None
    median_growth_time: HumanReadableFloat = None
    max_growth_time: int = None
    variance_growth_time: HumanReadableFloat = None
    mean_growth_time: HumanReadableFloat = None
    frequency_growth_time: Dict[int, int] = {}
