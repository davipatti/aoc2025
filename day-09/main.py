from collections import namedtuple
from dataclasses import dataclass
from itertools import combinations, pairwise


def load_data(path):
    with open(path) as fobj:
        return [Point(*map(int, line.strip().split(","))) for line in fobj]


Point = namedtuple("Point", ("x", "y"))


@dataclass
class Rectangle:
    """A rectangle defined by two opposite corners"""

    corner_a: Point
    corner_b: Point

    def __post_init__(self):
        self.width = abs(self.corner_a.x - self.corner_b.x) + 1
        self.height = abs(self.corner_a.y - self.corner_b.y) + 1
        self.area = self.width * self.height

        # left, right, top, bottom extents
        self.l = min(self.corner_a.x, self.corner_b.x)
        self.r = max(self.corner_a.x, self.corner_b.x)
        self.t = max(self.corner_a.y, self.corner_b.y)
        self.b = min(self.corner_a.y, self.corner_b.y)

    def edges(self):
        yield AxisLine(self.corner_a, Point(self.corner_a.x, self.corner_b.y))
        yield AxisLine(Point(self.corner_a.x, self.corner_b.y), self.corner_b)
        yield AxisLine(self.corner_b, Point(self.corner_b.x, self.corner_a.y))
        yield AxisLine(Point(self.corner_b.x, self.corner_a.y), self.corner_b)

    def contains(self, pt: Point) -> bool:
        return self.l < pt.x < self.r and self.b < pt.y < self.t


@dataclass
class AxisLine:
    """A line aligned to the x or y axis."""

    a: Point
    b: Point

    def __post_init__(self):
        self.left = min(self.a.x, self.b.x)
        self.right = max(self.a.x, self.b.x)
        self.top = max(self.a.y, self.b.y)
        self.bottom = min(self.a.y, self.b.y)
        self.is_vertical = self.a.x == self.b.x

    def intersects(self, other) -> bool:
        """
        Only true if one line is vertical and the other is horizontal
        """
        if self.is_vertical != other.is_vertical:
            (v_line, h_line) = (
                (self, other) if self.is_vertical else (other, self)
            )
            return (
                v_line.bottom < h_line.a.y < v_line.top
                and h_line.left < v_line.a.x < h_line.right
            )
        return False


def part1(path):
    return max(
        Rectangle(*corners).area
        for corners in combinations(load_data(path), 2)
    )


def part2(path):
    points = load_data(path)
    lines = [AxisLine(*corners) for corners in pairwise(points + [points[0]])]
    max_area = 0
    for corners in combinations(points, 2):
        rect = Rectangle(*corners)
        if not any(rect.contains(point) for point in points) and not any(
            edge.intersects(line) for edge in rect.edges() for line in lines
        ):
            max_area = max(max_area, rect.area)
    return max_area


if __name__ == "__main__":
    print(part1("input"))  # 4782151432
    print(part2("input"))  # 1450414119
