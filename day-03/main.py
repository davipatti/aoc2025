# %%


def read_input(path):
    with open(path) as fobj:
        for line in fobj:
            yield line.strip()


def max_joltage(line: str, n_digits: int) -> int:
    digits = []

    for n in reversed(range(n_digits)):

        # have to leave enough digits for subsequent rounds
        candidate_digits = line[: len(line) - n]

        digit = max(candidate_digits)
        digits.append(digit)

        if n > 0:
            # set up for the next iteration
            line = line[line.index(digit) + 1 :]

    return int("".join(digits))


def solve(path: str, n: int) -> int:
    return sum(max_joltage(line, n) for line in read_input(path))


# part 1
assert solve("example", 2) == 357
assert solve("input", 2) == 16927

# part 2
assert solve("example", 12) == 3121910778619
assert solve("input", 12) == 167384358365132
