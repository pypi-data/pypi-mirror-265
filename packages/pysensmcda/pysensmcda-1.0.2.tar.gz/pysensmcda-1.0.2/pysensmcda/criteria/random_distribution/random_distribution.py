# Copyright (C) 2024 Jakub Więckowski

import numpy as np
from ...validator import Validator
from ...utils import memory_guard

@memory_guard
def random_distribution(size: int) -> np.ndarray:
    """
    Generate a set of normalized weights sampled from a random distribution ( from half-open interval [0.0, 1.0) ).

    Parameters:
    ------------
    size : int
        Number of weights to generate.

    Returns:
    ---------
        ndarray
            Array of normalized weights sampled from a random distribution.

    Example
    ---------
    >>> weights = random_distribution(3)
    >>> print(weights)
    """

    Validator.is_type_valid(size, (int, np.integer), 'size')
    Validator.is_positive_value(size, var_name='size')

    weights = np.abs(np.random.random(size=size))
    return np.array(weights) / np.sum(weights)
