from dataclasses import dataclass
from functools import cached_property
import heapq
import numpy as np
from tqdm import tqdm

from main import load_data


@dataclass
class Node:
    buttons: list
    counters: np.ndarray
    target: np.ndarray
    presses: int

    def __post_init__(self):
        self.dist = (self.target - self.counters).sum()

    def __lt__(self, other):
        return self.presses < other.presses

    @cached_property
    def key(self) -> tuple:
        return tuple(self.counters)

    @property
    def children(self):

        for button in self.buttons:

            next_counters = self.counters.copy()
            next_counters[button] += 1

            # no counters overshoot
            if not any(next_counters > self.target):

                next_buttons = [
                    b
                    for b in self.buttons
                    if np.all(next_counters[b] + 1 <= self.target[b])
                ]

                yield Node(
                    next_buttons, next_counters, self.target, self.presses + 1
                )


def count_presses(buttons, target):
    counters = np.zeros_like(target)

    tree = [Node(buttons, counters, target, presses=0)]
    heapq.heapify(tree)

    node = heapq.heappop(tree)
    visited = {node.key}

    while not all(node.counters == target):

        for child in node.children:
            if child.key not in visited:
                visited.add(child.key)
                heapq.heappush(tree, child)

        if not tree:
            raise ValueError("probably shouldn't happen")

        node = heapq.heappop(tree)

    return node.presses


def solve(path):
    return sum(
        count_presses(buttons, target)
        for _, buttons, target in tqdm(list(load_data(path)))
    )


if __name__ == "__main__":
    assert solve("example") == 33
    print(solve("input"))
