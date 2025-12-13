def load_data(path):
    with open(path) as fobj:
        in_shape_def = False
        shape_mass = 0  # A shape's 'mass' is its number of '#' characters

        for line in fobj:

            if in_shape_def:
                shape_mass += line.count("#")
                if line.strip() == "":
                    yield shape_mass
                    shape_mass = 0
                    in_shape_def = False

            elif line[1] == ":":
                in_shape_def = True

            elif "x" in line:
                dims, *counts = line.strip().split()
                grid_w, grid_h = map(int, dims[:-1].split("x"))
                counts = tuple(map(int, counts))
                yield (grid_w, grid_h), counts


def enough_grid_cells(grid_w, grid_h, counts, shape_masses):
    """
    Can rule out some grid and shape count combinations if there aren't
    possibly enough grid cells. If one of the lines asks if two shapes that
    were each composed of 7 '#' chars could fit in a 4x3 grid, then there is
    definitely no solution, because together the shapes would require a grid
    with at least 2x7=14 slots.
    """
    area_required = sum(m * c for m, c in zip(shape_masses, counts))
    grid_area = grid_w * grid_h
    return area_required <= grid_area


def can_trivially_pack(grid_w, grid_h, counts):
    """
    Check if a grid can accommodate the number of shapes in counts by simply
    putting each shape in it's own 3x3 slot.
    """
    num_shapes = sum(counts)
    num_3x3_slots = (grid_w // 3) * (grid_h // 3)
    return num_shapes <= num_3x3_slots


def part1(path):
    data = tuple(load_data(path))
    shape_masses = data[:6]
    grid_dims_counts = data[6:]

    num_can_fit = 0
    num_cant_fit = 0
    num_unknown = 0

    for (grid_w, grid_h), counts in grid_dims_counts:
        if enough_grid_cells(grid_w, grid_h, counts, shape_masses):
            if can_trivially_pack(grid_w, grid_h, counts):
                num_can_fit += 1
            else:
                num_unknown += 1
        else:
            num_cant_fit += 1

    print("can fit:", num_can_fit)
    print("can't fit:", num_cant_fit)
    print("unknown:", num_unknown)


if __name__ == "__main__":
    part1("input")
