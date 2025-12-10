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
        self.distance = (self.target - self.counters).sum()

    def __lt__(self, other):
        return self.distance < other.distance

    @property
    def children(self):

        for i, button in enumerate(self.buttons):

            next_counters = self.counters.copy()
            next_counters[button] += 1

            # no counters overshoot
            if not any(next_counters > self.target):
                yield State(
                    self.buttons, next_counters, self.target, self.presses + 1
                )

            # counter has overshot having pressed this button
            # remove this button, and children without it
            else:
                next_buttons = self.buttons.copy()
                next_buttons.pop(i)
                if next_buttons:
                    yield from State(
                        next_buttons, self.counters, target, self.presses
                    ).children


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


n_presses = 0
for _, buttons, target in tqdm(list(load_data("input"))):
    target = np.array(target)
    n_presses += count_presses(buttons, target)
print()

print(n_presses)


# %%
