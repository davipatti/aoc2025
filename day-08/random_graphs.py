from itertools import count
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

# Graph sizes
Ns = np.logspace(1, 3, num=10).astype(int)


def count_random_pairs_for_single_cc(n, with_replacement: bool = False):
    nodes = np.arange(n)
    g = nx.Graph()
    for c in count():
        u, v = np.random.choice(nodes, 2, replace=with_replacement)
        g.add_edge(u, v)
        if g.number_of_nodes() == n and nx.number_connected_components(g) == 1:
            return c


def run_experiments(n_reps: int = 100, with_replacement: bool = False):
    return np.array(
        [
            [
                count_random_pairs_for_single_cc(n, with_replacement)
                for _ in range(n_reps)
            ]
            for n in Ns
        ]
    )


def f(n):
    return (n / 2) * np.log(n) + (n / 2) * np.log(np.log(n))


def plot_experiments(counts):
    plt.plot(Ns, f(Ns), label="(n/2) * ln(n) + (n/2) * ln((ln(n)))")
    plt.errorbar(
        Ns, np.mean(counts, axis=1), yerr=np.std(counts, axis=1), fmt="o"
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("Draws")
    plt.legend()


if __name__ == "__main__":
    np.random.seed(42)

    n_reps = 100

    # Without replacement
    counts = run_experiments(n_reps=n_reps, with_replacement=False)
    plot_experiments(counts)
    plt.title(
        "Number of draws of random edges required to fully\n"
        f"connect graph with n nodes ({counts.shape[1]} repeats for each n,\n"
        "nodes randomly selected without replacement)"
    )
    plt.savefig("random-draws.png", dpi=300, bbox_inches="tight")
    plt.close()


    # With replacement
    counts_with_replacement = run_experiments(
        n_reps=n_reps, with_replacement=True
    )
    plot_experiments(counts_with_replacement)
    plt.title(
        "Number of draws of random edges required to fully\n"
        f"connect graph with n nodes ({counts.shape[1]} repeats for each n,\n"
        "nodes randomly selected with replacement)"
    )
    plt.savefig(
        "random-draws-with-replacement.png", dpi=300, bbox_inches="tight"
    )
    plt.close()
