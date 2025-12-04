from main import read_input, KERNEL

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt


def plot(n):
    plt.imshow(grid, "binary")
    plt.gca().axis("off")
    plt.savefig(f"img/img{n}.png", bbox_inches="tight", dpi=150)


def animate_remove_rolls(grid: np.ndarray, fig_num: int) -> np.ndarray:
    num_rolls_orig = grid.sum()

    plot(fig_num)
    fig_num += 1

    n_neighbours = signal.convolve2d(grid, KERNEL, mode="same")

    grid[n_neighbours < 4] = 0

    return (
        animate_remove_rolls(grid, fig_num)
        if grid.sum() != num_rolls_orig
        else grid
    )


if __name__ == "__main__":
    grid = read_input("input")
    animate_remove_rolls(grid, fig_num=0)
