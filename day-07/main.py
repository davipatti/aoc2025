import numpy as np
from collections import Counter


def load_data(path):
    arr = np.array([list(line) for line in np.loadtxt(path, str)])
    start = np.argwhere(arr[0] == "S")[0][0]
    lines = [set(np.argwhere(line == "^")[:, 0]) for line in arr[2::2]]
    return start, lines


def part1(path):
    start, lines = load_data(path)
    beams = set([start])
    total_splits = 0
    for splitters in lines:
        split = set()
        for hit in beams & splitters:
            total_splits += 1
            split.add(hit - 1)
            split.add(hit + 1)
            beams.remove(hit)
        beams = beams | split
    return total_splits


def part2(path):
    start, lines = load_data(path)
    beams = Counter({start: 1})
    for line in lines:
        for hit in set(beams) & line:
            value = beams.pop(hit)
            beams[hit - 1] += value
            beams[hit + 1] += value
    return sum(beams.values())


if __name__ == "__main__":
    print(part1("input"))  # 1698
    print(part2("input"))  # 95408386769474
