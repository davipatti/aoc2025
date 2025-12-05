from typing import Self


def read_input(path):

    spans = []
    available_ingredients = []

    with open(path) as fobj:
        for line in fobj:
            match line.strip().split("-"):
                case [a, b]:
                    spans.append((int(a), int(b)))
                case [""]:
                    ...
                case [a]:
                    available_ingredients.append(int(a))

    return spans, available_ingredients


def part1(path):
    spans, available_ingredients = read_input(path)
    return sum(
        any(a <= ingredient <= b for a, b in spans)
        for ingredient in available_ingredients
    )


class Span:
    def __init__(self, a, b) -> None:
        if b < a:
            a, b = b, a
        self.a = a
        self.b = b

    def __repr__(self) -> str:
        return f"Span({self.a}, {self.b})"

    def __len__(self) -> int:
        return self.b - self.a + 1

    def __eq__(self, other) -> bool:
        return self.a == other.a and self.b == other.b

    def __add__(self, other) -> Self | list[Self, Self]:
        if self.overlaps(other):
            return Span(min(self.a, other.a), max(self.b, other.b))
        else:
            return [self, other]

    def overlaps(self, other) -> bool:
        return max(self.a, other.a) <= min(self.b, other.b)


def merge(span: Span, spans: list[Span]) -> list[Span]:

    overlapping = [s for s in spans if span.overlaps(s)]
    non_overlapping = [s for s in spans if not span.overlaps(s)]

    if overlapping:
        overlapping += [span]

        merged = Span(
            min(o.a for o in overlapping), max(o.b for o in overlapping)
        )

        return non_overlapping + [merged]

    else:
        return non_overlapping + [span]


def part2(path):
    input, _ = read_input(path)

    merged_spans = []
    for a, b in input:
        merged_spans = merge(Span(a, b), merged_spans)

    return sum(len(s) for s in merged_spans)


if __name__ == "__main__":
    assert part1("input") == 679
    assert part2("input") == 358155203664116
