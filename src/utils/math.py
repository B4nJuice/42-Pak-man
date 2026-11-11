def lerp(a: float, b: float, t: float) -> float:
    """
    Interpolate linearly between two numeric values.

    Args:
        a: First value used in the calculation.
        b: Second value used in the calculation.
        t: Interpolation factor between the two values.

    Returns:
        The value produced by the lerp operation.
    """
    return a + (b - a) * t
