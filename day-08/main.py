from itertools import product

from scipy.spatial.distance import pdist
import networkx as nx
import numpy as np


class JunctionBoxes:
    def __init__(self, path):
        self.coords = np.loadtxt(path, int, delimiter=",")
        self.m = len(self.coords)
        self.dists = pdist(self.coords)        
        self.pairs = np.array(  # pairs of coords in dists
            [
                (i, j)
                for i, j in product(range(self.m), repeat=2)
                if i < j and j < self.m
            ]
        )

    def part1(self, n_closest: int = 1000):
        edges = self.pairs[np.argsort(self.dists)][:n_closest]
        g = nx.Graph(list(edges))
        cc_lens = [len(cc) for cc in nx.connected_components(g)]
        return np.prod(sorted(cc_lens)[-3:])

    def part2(self):
        g = nx.Graph()
        for u, v in self.pairs[np.argsort(self.dists)]:
            g.add_edge(u, v)
            if (
                len(g.nodes()) == self.m  # all nodes added
                and len(list(nx.connected_components(g))) == 1  # single cc
            ):
                return self.coords[u, 0] * self.coords[v, 0]


if __name__ == "__main__":
    jb = JunctionBoxes("input")

    print(jb.part1(n_closest=1000))  # 79056
    print(jb.part2())  #  4639477
