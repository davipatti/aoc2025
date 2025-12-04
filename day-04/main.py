import numpy as np
from scipy import signal


def read_input(path):
    with open(path) as fobj:
        for line in fobj:
            yield [0 if char == "." else 1 for char in line.strip()]


KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def part1(input_path):
    grid = np.array(list(read_input(input_path)))
    result = signal.convolve2d(grid, KERNEL, mode="same")
    return (result[grid == 1] < 4).sum()


def remove_accessible_rolls(grid: np.ndarray) -> np.ndarray:
    num_rolls_orig = grid.sum()

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
        remove_accessible_rolls(grid)
        if num_rolls_now != num_rolls_orig
        else grid
    )


def part2(input_path):
    grid = np.array(list(read_input(input_path)))

    # number of rolls removed is the number of initial rolls - number of
    # ending rolls
    return grid.sum() - remove_accessible_rolls(grid).sum()


if __name__ == "__main__":
    print(part1("input"))
    print(part2("input"))
