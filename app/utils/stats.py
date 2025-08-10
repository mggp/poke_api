from collections import Counter
from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class CommonIntStats:
    min: int
    max: int
    mean: float
    median: float
    variance: float
    frequency: dict[int, int]


def calculate_stats(data_list: Iterable[int]) -> CommonIntStats:
    """
    Gets basic statistics from a list of numerical data.
    """
    if not data_list:
        return {}

    try:
        data_list = np.fromiter(data_list, dtype=int)

        stats = CommonIntStats(
            min=np.min(data_list),
            max=np.max(data_list),
            mean=np.mean(data_list),
            median=np.median(data_list),
            variance=np.var(data_list),
            frequency=dict(Counter(data_list)),
        )

    except ValueError as e:
        raise ValueError("Error calculating statistics") from e

    return stats


def get_frequencies(data_list: Iterable[int]) -> dict[int, int]:
    """
    Returns a frequency dictionary from a list of numerical data.
    """
    if not data_list:
        return {}

    try:
        data_list = np.fromiter(data_list, dtype=int)

        frequency = Counter(data_list)

    except ValueError as e:
        raise ValueError("Error computing frequency") from e

    return dict(frequency)
