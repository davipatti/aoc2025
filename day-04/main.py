import numpy as np
from scipy import signal


def read_input(path):
    with open(path) as fobj:
        return np.array(
            [
                [0 if char == "." else 1 for char in line.strip()]
                for line in fobj
            ]
        )


KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def remove_accessible_rolls(grid: np.ndarray, recursive: bool) -> np.ndarray:
    n_rolls_orig = grid.sum()

    n_neighbours = signal.convolve2d(grid, KERNEL, mode="same").astype(float)

    n_neighbours[grid == 0] = np.nan  # empty slots -> nan

    # remove accessible rolls
    idx = np.argwhere(n_neighbours < 4)
    grid[idx[:, 0], idx[:, 1]] = 0

    # keep trying to remove rolls if rolls were just removed
    return (
        remove_accessible_rolls(grid, recursive)
        if recursive and grid.sum() != n_rolls_orig
        else grid
    )


def solve(input_path, recursive):
    grid = read_input(input_path)

    # number of rolls removed is the number of initial rolls - number of
    # ending rolls
    return grid.sum() - remove_accessible_rolls(grid, recursive).sum()


if __name__ == "__main__":
    print(solve("input", recursive=False))  # 1516
    print(solve("input", recursive=True))  # 9122
