# Copyright (C) 2024 Jakub Więckowski

import numpy as np
from ...validator import Validator
from ...utils import memory_guard

@memory_guard
def laplace_distribution(size: int, loc: float = 0.0, scale: float = 1.0) -> np.ndarray:
    """
    Generate a set of normalized weights sampled from a laplace distribution.

    Parameters:
    ------------
    size : int
        Number of weights to generate.

    loc : float, optional, default=0.0
        The position of distribution peak
    
    scale : float, optional, default=1.0
        The exponential decay. Must be non-negative

    Returns:
    ---------
        ndarray
            Array of normalized weights sampled from a laplace distribution.

    Examples
    ----------
    Example 1: Generate normalized weights from a laplace distribution with default parameters
    
    >>> weights = laplace_distribution(3)
    >>> print(weights)

    Example 2: Generate normalized weights from a laplace distribution with explicit parameters
    
    >>> weights = laplace_distribution(3, 5, 2)
    >>> print(weights)
    """

    Validator.is_type_valid(size, (int, np.integer), 'size')
    Validator.is_positive_value(size, var_name='size')
    Validator.is_type_valid(loc, (int, np.integer, float, np.floating), 'loc')
    Validator.is_type_valid(scale, (int, np.integer, float, np.floating), 'scale')
    Validator.is_positive_value(scale, var_name='scale')

    weights = np.abs(np.random.laplace(loc, scale, size=size))
    return np.array(weights) / np.sum(weights)
