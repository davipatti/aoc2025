# %%

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

    # Save a figure
    plot(fig_num)
    fig_num += 1

    result = signal.convolve2d(grid, KERNEL, mode="same").astype(float)

    # replace empty slots with nan
    result[grid == 0] = np.nan

    # indexes of rolls to remove
    idx = np.argwhere(result < 4)

    # remove accessible rolls
    grid[idx[:, 0], idx[:, 1]] = 0

    num_rolls_now = grid.sum()

    # keep trying to remove rolls if rolls were just removed
    return (
        animate_remove_rolls(grid, fig_num)
        if num_rolls_now != num_rolls_orig
        else grid
    )


if __name__ == "__main__":
    grid = np.array(list(read_input("input")))
    animate_remove_rolls(grid, fig_num=0)
