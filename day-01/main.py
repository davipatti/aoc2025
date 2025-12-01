# %%

from operator import add, sub


def read_input(path):
    with open(path) as fobj:
        for line in fobj:
            line = line.strip()
            op = add if line[0] == "R" else sub
            n = int(line[1:])
            yield op, n


# %% part 1

position = 50

password = 0

for op, n in read_input("input"):

    if position == 0:
        password += 1

    position = op(position, n) % 100

print(password)

# %% part 2

position = 50

password = 0

for op, n in read_input("input"):

    for _ in range(n):

        position = op(position, 1) % 100

        if position == 0:
            password += 1

print(password)
