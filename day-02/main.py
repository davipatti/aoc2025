# %%


from typing import Callable
from itertools import batched


def read_input(path):
    with open(path) as fobj:
        for line in fobj:
            for pair in line.strip().split(","):
                yield map(int, pair.split("-"))


# %%


def solve(path: str, is_invalid: Callable) -> int:
    return sum(
        id
        for a, b in read_input(path)
        for id in range(a, b + 1)
        if is_invalid(id)
    )


# %%


def is_invalid_part_1(id: str | int) -> bool:
    id = str(id)

    id_len = len(id)

    if id_len % 2 == 0:
        middle = id_len // 2
        return id[:middle] == id[middle:]

    else:
        return False


assert is_invalid_part_1("11")
assert is_invalid_part_1("38593859")
assert not is_invalid_part_1("1698528")

print(solve("input", is_invalid_part_1))  # 21898734247

# %%


def is_invalid_part_2(id: str | int) -> bool:
    id = str(id)
    for n in range(1, (len(id) // 2) + 1):

        unique_chunks = set(batched(id, n))

        if len(unique_chunks) == 1:
            return True
    
    else:
        return False


assert is_invalid_part_2("446446")
assert is_invalid_part_2("2121212121")
assert not is_invalid_part_2("2121212124")

print(solve("input", is_invalid_part_2))  # 28915664389
