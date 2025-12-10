from itertools import combinations

import numpy as np


def load_data(path):
    with open(path) as fobj:
        for line in fobj:
            lights, *buttons, joltage = line.strip().split()
            yield (
                [char == "#" for char in lights[1:-1]],
                [
                    list(map(int, button[1:-1].split(",")))
                    for button in buttons
                ],
                np.array(list(map(int, joltage[1:-1].split(",")))),
            )


def press(button, status):
    status = status.copy()
    for idx in button:
        status[idx] = not status[idx]
    return status


def press_multiple(buttons, status):
    for button in buttons:
        status = press(button, status)
    return status


def find_comb(buttons, goal):
    status = [False] * len(goal)
    n_buttons = 1
    while True:
        for comb in combinations(buttons, n_buttons):
            if press_multiple(comb, status) == goal:
                return n_buttons
        n_buttons += 1


def part1(path):
    return sum(
        find_comb(buttons, goal) for goal, buttons, _ in load_data(path)
    )


if __name__ == "__main__":

    print(part1("input"))
