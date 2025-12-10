# %%

from dataclasses import dataclass
import heapq
import numpy as np
from tqdm import tqdm

from main import load_data


@dataclass
class State:
    buttons: list
    counters: np.ndarray
    target: np.ndarray
    presses: int

    def __post_init__(self):
        self.dist = (self.target - self.counters).sum()

    def __lt__(self, other):
        return (self.presses + self.dist) < (other.presses + other.dist)

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

                yield State(
                    next_buttons, next_counters, self.target, self.presses + 1
                )


def count_presses(buttons, target):

    counters = np.zeros_like(target)

    states = [State(buttons, counters, target, presses=0)]
    heapq.heapify(states)

    visited = {tuple(counters)}

    state = heapq.heappop(states)

    while not all(state.counters == target):

        for child in state.children:
            key = tuple(child.counters)
            if key not in visited:
                visited.add(key)
                heapq.heappush(states, child)

        if not states:
            return 0

        state = heapq.heappop(states)

    return state.presses


def solve(path):
    n_presses = 0
    for _, buttons, target in tqdm(list(load_data(path))):
        target = np.array(target)
        n_presses += count_presses(buttons, target)
    return n_presses


assert solve("example") == 33

solve("input")

# %%
