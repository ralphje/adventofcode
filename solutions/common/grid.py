def distance(a: complex, b: complex) -> float:
    """Calculates the distance between two complex numbers, or the distance between two
    coordinates
    """
    return ((c := (a - b)).imag ** 2 + c.real**2) ** 0.5
