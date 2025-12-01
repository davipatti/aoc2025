# %%

def read_input(path):
    with open(path) as fobj:
        for line in fobj:
            line = line.strip()
            direction = line[0]
            n = int(line[1:])
            yield direction, n

# %% part 1

position = 50

password = 0

for direction, n in read_input("input"):

    if position == 0:
        password += 1

    if direction == "L":
        position = (position - n) % 100
    else:
        position = (position + n) % 100

print(password)

# %% part 2

position = 50

password = 0

for direction, n in read_input("input"):

    for _ in range(n):

        if direction == "R":
            position = (position + 1) % 100
        else:
            position = (position - 1) % 100
        
        if position == 0:
            password += 1

print(password)
