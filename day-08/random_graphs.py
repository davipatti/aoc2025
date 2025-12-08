# %%

from itertools import count
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")


def count_random_pairs_for_single_cc(n):
    nodes = np.arange(n)
    g = nx.Graph()
    for c in count():
        u, v = np.random.choice(nodes, 2)
        g.add_edge(u, v)
        if g.number_of_nodes() == n and nx.number_connected_components(g) == 1:
            return c


np.random.seed(42)

N_REPS = 100
Ns = np.logspace(1, 3, num=10).astype(int)

counts = [
    [count_random_pairs_for_single_cc(n) for _ in range(N_REPS)] for n in Ns
]

# %%


def f(n):
    return (n / 2) * np.log(n) + (n / 2) * np.log(np.log(n))


plt.plot(Ns, f(Ns), label="(n/2) * ln(n) + (n/2) * ln((ln(n)))")
plt.errorbar(Ns, np.mean(counts, axis=1), yerr=np.std(counts, axis=1), fmt="o")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("Draws")
plt.title(
    "Number of draws of random edges required to fully\n"
    f"connect graph with n nodes ({N_REPS} repeats for each n)"
)
plt.legend()

plt.savefig("random-draws.png", dpi=300, bbox_inches="tight")

# %%
