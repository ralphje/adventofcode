import math


def quadratic_formula(a: int, b: int, c: int) -> tuple[float, float]:
    """Apply the quadratic formula, and return the solutions for x, if ``0 = ax² + bx + c``

    Solutions are defined as::

        x = (-b ± √(b² - 4ac)) / 2a
    """
    return (
        (-b - (sqrt := math.sqrt(b**2 - 4 * a * c))) / (2 * a),
        (-b + sqrt) / (2 * a),
    )
