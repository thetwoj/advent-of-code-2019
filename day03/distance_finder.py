wires = []


def read_map():
    with open("input.txt") as f:
        wires_directions = [line.strip().split(",") for line in f]
    for wire_directions in wires_directions:
        current_x = 0
        current_y = 0
        current_wire = [(current_x, current_y)]
        for instruction in wire_directions:
            direction = instruction[0]
            count = int(instruction[1:])
            if direction == "L":
                current_x -= count
            elif direction == "U":
                current_y += count
            elif direction == "R":
                current_x += count
            elif direction == "D":
                current_y -= count
            current_wire.append((current_x, current_y))
        wires.append(current_wire)
    return shortest_distance_to_intersection()


def wires_cross(v1, v2, h1, h2):
    # horizontal wire crosses x of vertical wire
    if h1[0] <= v1[0] <= h2[0] or h1[0] >= v1[0] >= h2[0]:
        # horizontal wire exists within y bounds of vertical wire
        if v1[1] <= h1[1] <= v2[1] or v1[1] >= h1[1] >= v2[1]:
            return True
    return False


def is_horizontal(c1, c2):
    return c1[0] == c2[0]


def is_vertical(c1, c2):
    return c1[1] == c2[1]


def shortest_distance_to_intersection():
    intersections = []
    steps_to_intersection = []

    def record_steps_to_intersection(c1, c2):
        tmp1wst = wire_steps + abs(c1[1] - c2[1])
        tmp2wst = second_wire_steps + abs(c2[0] - c1[0])
        steps_to_intersection.append(tmp1wst + tmp2wst)

    # not a huge fan of this, there's gotta be some simple algorithm for
    # this sort of problem that i'm not familiar with
    for index, wire in enumerate(wires):
        wire_steps = 0
        if index == len(wires) - 1:
            continue
        for coord_index, coord in enumerate(wire):
            if coord_index == len(wire) - 1:
                continue
            coord2 = wire[coord_index + 1]

            second_wire = wires[index + 1]
            second_wire_steps = 0
            for second_coord_index, second_coord in enumerate(second_wire):
                if second_coord_index == len(second_wire) - 1:
                    continue
                second_coord2 = second_wire[second_coord_index + 1]

                # this is also gross
                if (
                    is_horizontal(coord, coord2)
                    and is_horizontal(second_coord, second_coord2)
                    or is_vertical(coord, coord2)
                    and is_vertical(second_coord, second_coord2)
                ):
                    second_wire_steps += abs(second_coord[0] - second_coord2[0]) + abs(
                        second_coord[1] - second_coord2[1]
                    )
                    continue

                # wire vertical, second_wire horizontal
                if coord[0] == coord2[0]:
                    if wires_cross(coord, coord2, second_coord, second_coord2):
                        intersections.append((coord[0], second_coord[1]))
                        record_steps_to_intersection(coord, second_coord)
                # second_wire vertical, wire horizontal
                else:
                    if wires_cross(second_coord, second_coord2, coord, coord2):
                        intersections.append((second_coord[0], coord[1]))
                        record_steps_to_intersection(coord, second_coord)

                second_wire_steps += abs(second_coord[0] - second_coord2[0]) + abs(
                    second_coord[1] - second_coord2[1]
                )
            wire_steps += abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])

    distances = [abs(c[0]) + abs(c[1]) for c in intersections]
    return min(distances), min(steps_to_intersection)


if __name__ == "__main__":
    min_distance, min_steps = read_map()
    print(f"part one:\n{min_distance}")
    print()
    print(f"part two:\n{min_steps}")
