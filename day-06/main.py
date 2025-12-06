import numpy as np


def part1(path):
    grid = np.loadtxt(path, dtype=str)
    values, operators = grid[:-1].astype(int).T, grid[-1]
    return sum(
        np.sum(row) if operator == "+" else np.prod(row)
        for row, operator in zip(values, operators)
    )


def transpose_file(path):
    with open(path) as fobj:
        lines = [line for line in fobj]
    line_len = len(lines[0]) - 1
    with open(f"{path}.T", "w") as fobj:
        for i in range(line_len):
            for line in lines:
                fobj.write(line[i])
            fobj.write("\n")


def part2(path):
    transpose_file(path)
    total = 0
    with open(f"{path}.T") as fobj:
        for line in fobj:
            line = line.strip()
            if "*" in line or "+" in line:
                op = np.prod if "*" in line else np.sum
                values = [int(line[:-1])]
            elif line == "":
                total += op(values)
            else:
                values.append(int(line))
        total += op(values)
    return total


if __name__ == "__main__":
    print(part1("input"))  # 5784380717354
    print(part2("input"))  # 7996218225744
