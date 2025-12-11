from functools import cache
from itertools import pairwise

import networkx as nx


def part1(path):
    g = load_nx_graph(path)
    return len(list(nx.all_simple_paths(g, source="you", target="out")))


def part2(path):
    """
    Paths can either go:

        svr -> dac -> fft -> out
        svr -> fft -> dac -> out

    However, there are no paths from dac -> fft.

    Therefore the only path allowed must go:

        svr -> fft -> dac -> out
    """
    g = load_nx_graph(path)

    assert nx.has_path(g, "svr", "dac")
    assert nx.has_path(g, "svr", "fft")

    assert nx.has_path(g, "fft", "dac")
    assert not nx.has_path(g, "dac", "fft")  # no path from dac -> fft
    assert nx.has_path(g, "fft", "out")
    assert nx.has_path(g, "dac", "out")

    assert nx.is_directed_acyclic_graph(g)  # this is a DAG

    return count_paths_iter(
        g, start_ends=pairwise(("svr", "fft", "dac", "out"))
    )


def count_paths(g, start, end):
    """Heart of part 2"""

    @cache  # memoisation only improves runtime from ~4 -> ~0.8 s
    def count(u):
        if u == end:
            return 1
        return sum(count(v) for v in g.successors(u))

    return count(start)


def count_paths_iter(g, start_ends):
    """Multiply the number of paths in each subgraph."""
    n = 1
    for start, end in start_ends:
        n *= count_paths(g, start, end)
    return n


def load_nx_graph(path):
    with open(path) as fobj:
        d = {}
        for line in fobj:
            parent, *children = line.strip().split()
            d[parent.strip(":")] = children
    return nx.DiGraph(d)


if __name__ == "__main__":
    print(part1("input"))  # 753
    print(part2("input"))  # 450854305019580
