from functools import cache
from itertools import pairwise
import math


def load_data(path):
    with open(path) as fobj:
        graph = {}
        for line in fobj:
            parent, *children = line.strip().split()
            graph[parent[:-1]] = children
    return graph


def count_paths(graph, start, end):

    @cache
    def count(node):
        if node == end:
            return 1
        elif node not in graph:
            return 0
        else:
            return sum(count(child) for child in graph[node])

    return count(start)


def count_paths_route(graph, route):
    return math.prod(count_paths(graph, start, end) for start, end in route)


def part1(graph):
    return count_paths(graph, "you", "out")


def part2(graph):
    route1 = pairwise(("svr", "fft", "dac", "out"))
    route2 = pairwise(("svr", "dac", "fft", "out"))
    return count_paths_route(graph, route1) + count_paths_route(graph, route2)


if __name__ == "__main__":
    graph = load_data("input")
    print(part1(graph))  # 753
    print(part2(graph))  # 450854305019580
