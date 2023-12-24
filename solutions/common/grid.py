from collections.abc import Iterator, Sequence
from typing import Any, overload


def distance(a: complex, b: complex) -> float:
    """Calculates the distance between two complex numbers, or the distance between two
    coordinates
    """
    return ((c := (a - b)).imag ** 2 + c.real**2) ** 0.5


class Grid[T]:
    """Acts as a grid with certain possibilities."""

    def __init__(self, grid: Sequence[Sequence[T]], /) -> None:
        self._grid = grid

    @property
    def rows(self) -> Sequence[Sequence[T]]:
        return self._grid

    @property
    def cells(self) -> Iterator[T]:
        """Yield all cell values, grouped by row."""
        for row in self.rows:
            yield from row

    @classmethod
    def _coordinate(cls, *args: Any) -> complex:
        """Convert the provided argument(s) into a complex number representing a coordinate."""
        if len(args) == 1 and isinstance(args[0], complex):
            return args[0]
        elif len(args) == 1 and isinstance(args[0], tuple):
            return complex(*args[0])
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            return complex(*args)
        raise ValueError(f"Could not parse the provided coordinates: {args!r}")

    @property
    def height(self) -> int:
        """Return the height of the grid."""
        return len(self._grid)

    @property
    def width(self) -> int:
        """Return the width of the grid."""
        return len(self._grid[0]) if self._grid else 0

    def __len__(self) -> int:
        """Returns the size of the grid, if it is square, otherwise return error."""
        if self.height == 0:
            return 0
        if self.height == self.width:
            return self.height
        raise ValueError("grid is not square")

    @overload
    def in_bounds(self, coordinate: complex | tuple[int, int]) -> bool: ...

    @overload
    def in_bounds(self, x: int, y: int) -> bool: ...

    def in_bounds(self, *args: Any) -> bool:
        """Returns whether the provided coordinate is in bounds."""
        coordinate = self._coordinate(*args)
        return (0 <= int(coordinate.imag) < self.height) and (
            0 <= int(coordinate.real) < self.width
        )

    def __getitem__(self, item: Any) -> T:
        """Same as .get()"""
        return self.get(item)

    @overload
    def get(self, coordinate: complex | tuple[int, int]) -> T: ...

    @overload
    def get(self, x: int, y: int) -> T: ...

    def get(self, *args: Any) -> T:
        """Gets the data at the provided coordinate."""
        coordinate = self._coordinate(*args)
        return self._grid[int(coordinate.imag)][int(coordinate.real)]

    def find(self, value: T) -> Iterator[complex]:
        """Yields all coordinates for which the value is at that location."""
        yield from (
            complex(x, y)
            for y, row in enumerate(self._grid)
            for x, v in enumerate(row)
            if v == value
        )

    @overload
    def orthogonal(self, coordinate: complex | tuple[int, int]) -> Iterator[complex]: ...

    @overload
    def orthogonal(self, x: int, y: int) -> Iterator[complex]: ...

    def orthogonal(self, *args: Any) -> Iterator[complex]:
        """Yields all orthogonal directions in of the provided coordinate"""

        coordinate = self._coordinate(*args)
        for direction in (+1, -1, -1j, +1j):
            if self.in_bounds(coordinate + direction):
                yield coordinate + direction

    @overload
    def diagonal(self, coordinate: complex | tuple[int, int]) -> Iterator[complex]: ...

    @overload
    def diagonal(self, x: int, y: int) -> Iterator[complex]: ...

    def diagonal(self, *args: Any) -> Iterator[complex]:
        """Yields all diagonal directions in of the provided coordinate"""

        coordinate = self._coordinate(*args)
        for direction in (+1 + 1j, -1 + 1j, +1 - 1j, -1 + 1j):
            if self.in_bounds(coordinate + direction):
                yield coordinate + direction

    @overload
    def adjacent(self, coordinate: complex | tuple[int, int]) -> Iterator[complex]: ...

    @overload
    def adjacent(self, x: int, y: int) -> Iterator[complex]: ...

    def adjacent(self, *args: Any) -> Iterator[complex]:
        """Yields all adjacent directions in of the provided coordinate"""

        yield from self.orthogonal(*args)
        yield from self.diagonal(*args)


class RepeatingGrid[T](Grid):
    """The same as Grid, but repeats itself infinitely."""

    def in_bounds(self, *args: Any) -> bool:
        return True

    def _mod_coordinate(self, *args: Any) -> complex:
        coordinate = self._coordinate(*args)
        return complex(coordinate.real % self.width, coordinate.imag % self.height)

    def get(self, *args: Any) -> T:
        return super().get(self._mod_coordinate(*args))


class FrozenGrid[T](Grid):
    """Same as Grid, but cannot be adjusted so it can be cached."""

    def __init__(self, grid: Sequence[Sequence[T]], /) -> None:
        super().__init__(grid)
        self._grid = tuple(map(tuple, self._grid))

    def __hash__(self):
        return hash(self._grid)
