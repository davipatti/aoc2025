from scipy.spatial.distance import pdist
import networkx as nx
import numpy as np


class JunctionBoxes:
    def __init__(self, path):
        self.coords = np.loadtxt(path, int, delimiter=",")
        self.m = len(self.coords)
        self.dists = pdist(self.coords)

        # pairs of coords, sorted by distance
        pairs = np.vstack(np.triu_indices(self.m, k=1)).T
        self.pairs = pairs[np.argsort(self.dists)]

    def part1(self, n_closest: int = 1000):
        g = nx.Graph(list(self.pairs[:n_closest]))
        cc_lens = [len(cc) for cc in nx.connected_components(g)]
        return np.prod(sorted(cc_lens)[-3:])

    def part2(self):
        g = nx.Graph()
        for u, v in self.pairs:
            g.add_edge(u, v)
            if (
                g.number_of_nodes() == self.m  # all nodes added
                and nx.number_connected_components(g) == 1
            ):
                return self.coords[u, 0] * self.coords[v, 0]


if __name__ == "__main__":
    jb = JunctionBoxes("input")

    print(jb.part1(n_closest=1000))  # 79056
    print(jb.part2())  #  4639477
