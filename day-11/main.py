from functools import cache
from itertools import pairwise

import matplotlib.pyplot as plt
import networkx as nx

from lib import plot_graph


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
    g = load_nx_graph("input")

    assert nx.has_path(g, "svr", "dac")
    assert nx.has_path(g, "svr", "fft")

    assert nx.has_path(g, "fft", "dac")
    assert not nx.has_path(g, "dac", "fft")  # no path from dac -> fft

    assert nx.has_path(g, "fft", "out")
    assert nx.has_path(g, "dac", "out")

    assert nx.is_directed_acyclic_graph(g)  # this is a DAG

    return count_paths_iter(
        path, start_ends=pairwise(("svr", "fft", "dac", "out")), plot=True
    )


def count_paths(g, start, end):
    """Heart of part 2"""

    @cache
    def count(u):
        if u == end:
            return 1
        return sum(count(v) for v in g.successors(u))

    return count(start)


def count_paths_iter(path, start_ends, plot=False):
    """
    Donkey work of part 2
    
    Multiply the number of paths in each subgraph.
    """
    g = load_nx_graph(path)

    if plot:
        fig, _ = plt.subplots(
            nrows=2, ncols=2, figsize=(20, 10), sharex=True, sharey=True
        )
        axes = iter(fig.axes)
        # pos = nx.bfs_layout(g, "svr")
        pos = nx.kamada_kawai_layout(g)
        ax = next(axes)
        plot_graph(g, pos=pos, ax=ax)
        ax.set_title("Full graph")

    n = 1
    for start, end in start_ends:
        assert nx.has_path(g, start, end)
        subgraph = load_subgraph(path, start, end)

        if plot:
            ax = ax = next(axes)
            plot_graph(
                g,
                edge_color="lightgrey",
                node_color="lightgrey",
                pos=pos,
                ax=ax,
            )
            plot_graph(subgraph, pos=pos, ax=ax)
            ax.set_title(f"{start} → {end}")

        n *= count_paths(subgraph, start, end)

    if plot:
        plt.savefig("part2-subgraphs.png", dpi=300, bbox_inches="tight")
        plt.close()

    return n


def load_nx_graph(path):
    with open(path) as fobj:
        d = {}
        for line in fobj:
            parent, *children = line.strip().split()
            d[parent.strip(":")] = children
    return nx.DiGraph(d)


def load_subgraph(path, start, end):
    g = load_nx_graph(path)

    # Anything that isn't a descendant of start (keep start)
    g.remove_nodes_from(set(g.nodes()) - (nx.descendants(g, start) | {start}))

    # Anything that doesn't have end in its descendants
    g.remove_nodes_from(
        {node for node in g.nodes() if end not in nx.descendants(g, node)}
        - {end}
    )

    return g


if __name__ == "__main__":
    print(part1("input"))  # 753
    print(part2("input"))  # 450854305019580
