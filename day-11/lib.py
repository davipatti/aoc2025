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
