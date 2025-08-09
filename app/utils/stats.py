from typing import List
import numpy as np
from collections import Counter

def calculate_stats(data_list: List[int]):
    """
    Gets basic statistics from a list of numerical data.
    """
    if not data_list:
        return {}

    # TODO: Convert data_list to a numpy array for efficient calculations?
    # TODO: Handle cases where data_list has only one element?
    # TODO: Consider using pandas for more complex statistics?
    # TODO: Add error handling for non-numeric data?
    # TODO: Add type hints for better code clarity? Or schema validation?
    
    stats = {
        "min": np.min(data_list),
        "max": np.max(data_list),
        "mean": np.mean(data_list),
        "median": np.median(data_list),
        "variance": np.var(data_list),
        "frequency": Counter(data_list)
    }

    return stats