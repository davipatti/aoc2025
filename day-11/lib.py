import matplotlib.pyplot as plt
import networkx as nx


def plot_graph(g, **kwds):
    nodes_of_interest = {"svr", "dac", "fft", "out"}
    nx.draw(
        g,
        node_size=kwds.pop(
            "node_size",
            [100 if node in nodes_of_interest else 5 for node in g.nodes()],
        ),
        font_size=kwds.pop("font_size", 3),
        node_color=kwds.pop(
            "node_color",
            [
                "red" if node in nodes_of_interest else "black"
                for node in g.nodes()
            ],
        ),
        width=0.5,
        arrows=False,
        linewidths=0.5,
        **kwds,
    )


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


def plot_subgraphs(path, start_ends):
    """
    plot the subgraphs implied by start_end
    """
    fig, _ = plt.subplots(
        nrows=2, ncols=2, figsize=(20, 10), sharex=True, sharey=True
    )
    axes = iter(fig.axes)
    g = load_nx_graph(path)
    pos = nx.bfs_layout(g, "svr")
    ax = next(axes)
    plot_graph(g, pos=pos, ax=ax)
    ax.set_title("Full graph")

    for start, end in start_ends:
        assert nx.has_path(g, start, end)
        subgraph = load_subgraph(path, start, end)
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

    plt.savefig("part2-subgraphs.png", dpi=300, bbox_inches="tight")
    plt.close()
