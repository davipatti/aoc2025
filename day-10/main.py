from itertools import combinations

from scipy.optimize import milp, LinearConstraint
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


def count_presses(buttons, target):
    """
    scipy milp (mixed integer linear programming) minimizes:

        c @ x

    such that:

        b_l <= A @ x <= b_u     # -> can constrain the result
        l <= x <= u             # -> can constrain the decision variables

    and elements of x must be integers.

    - `x` is a vector of button presses; the number of times each button is
      pressed.  `x` is what is being optimized. Also called the 'decision
      variables'.
    - `c` can be thought of as a vector of 'weights' for each button. Passing
      all ones for c sums the total number of button presses (c @ x).
    - `A` can also constrain the decision variables via A @ x. A encodes the
      counters that get incremented for each button press.
    - We set b_l and b_u as the target, so that A @ x must == target (target is
      the required counts on each counter).
    """
    m = len(buttons)
    n = len(target)

    # A[i, j] is 1 if the ith button turns on the jth light
    A = np.zeros((n, m))
    for j, i in enumerate(buttons):
        A[i, j] = 1

    res = milp(
        c=np.ones(m),
        constraints=LinearConstraint(A, lb=target, ub=target),
        integrality=1,  # forces decision variables to be ints
    )

    return round(res.x.sum())


def part1(path):
    return sum(
        find_comb(buttons, goal) for goal, buttons, _ in load_data(path)
    )


def part2(path):
    return sum(
        count_presses(buttons, target)
        for _, buttons, target in load_data(path)
    )


if __name__ == "__main__":
    print(part1("input"))
    print(part2("input"))
