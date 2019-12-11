from copy import deepcopy


def read_map():
    with open("input.txt") as f:
        data = ""
        for x in f:
            width = len(x)
            data += x.strip()

    star_map = [[] for _ in range(width)]
    for index, value in enumerate(data):
        x = index % width
        star_map[x].append(value)

    return star_map


def print_star_map(sm):
    for y in range(len(sm[0])):
        for x in range(len(sm)):
            if x == len(sm) - 1:
                print(sm[x][y])
            else:
                print(sm[x][y], end="")


def find_asteroids(sm):
    asteroids = {}
    for x in range(len(sm)):
        for y in range(len(sm[0])):
            if sm[x][y] == "#":
                asteroids[(x, y)] = 0
    # print(asteroids)
    return asteroids


def next_move(last_move, x, y, max_x, max_y, explored):
    if last_move == 0:  # L
        if (x, y - 1) not in explored and y - 1 >= 0:
            return x, y - 1, 1
        if (x - 1, y) not in explored and x - 1 >= 0:
            return x - 1, y, 0
        if (x, y + 1) not in explored and y + 1 < max_y:
            return x, y + 1, 3
        if (x + 1, y) not in explored and x + 1 < max_x:
            return x + 1, y, 2
    if last_move == 1:  # U
        if (x + 1, y) not in explored and x + 1 < max_x:
            return x + 1, y, 2
        if (x, y - 1) not in explored and y - 1 >= 0:
            return x, y - 1, 1
        if (x - 1, y) not in explored and x - 1 >= 0:
            return x - 1, y, 0
        if (x, y + 1) not in explored and y + 1 < max_y:
            return x, y + 1, 3
    if last_move == 2:  # R
        if (x, y + 1) not in explored and y + 1 < max_y:
            return x, y + 1, 3
        if (x + 1, y) not in explored and x + 1 < max_x:
            return x + 1, y, 2
        if (x, y - 1) not in explored and y - 1 >= 0:
            return x, y - 1, 1
        if (x - 1, y) not in explored and x - 1 >= 0:
            return x - 1, y, 0
    if last_move == 3:  # D
        if (x - 1, y) not in explored and x - 1 >= 0:
            return x - 1, y, 0
        if (x, y + 1) not in explored and y + 1 < max_y:
            return x, y + 1, 3
        if (x + 1, y) not in explored and x + 1 < max_x:
            return x + 1, y, 2
        if (x, y - 1) not in explored and y - 1 >= 0:
            return x, y - 1, 1


def count_viewable_asteroids(sm, asteroid):
    # print(asteroid)
    blocked_coords = set()
    blocked_coords.add(asteroid)
    sights = set()
    visible_count = 0
    og_x, og_y = asteroid
    x, y = og_x, og_y
    max_x = len(sm)
    max_y = len(sm[0])

    last_move = 0
    explored = []
    explored.append((x, y))
    while len(explored) < max_x * max_y:
        x, y, last_move = next_move(
            last_move, x, y, max_x, max_y, explored
        )  # 0:L, 1:U, 2:R, 3:D
        explored.append((x, y))
        print(explored)

        if (x, y) in blocked_coords or sm[x][y] != "#":
            continue
        visible_count += 1
        sights.add((x, y))
        blocked_coords.add((x, y))

        if og_x == x:
            if y < og_y:
                for new_y in range(0, og_y + 1):
                    blocked_coords.add((x, new_y))
                continue
            else:
                for new_y in range(og_y, max_y + 1):
                    blocked_coords.add((x, new_y))
                continue

        if og_y == y:
            if x < og_x:
                for new_x in range(0, og_x + 1):
                    blocked_coords.add((new_x, y))
                continue
            else:
                for new_x in range(og_x, max_x + 1):
                    blocked_coords.add((new_x, y))
                continue

        if x > og_x and y > og_y:
            new_x = x + (x - og_x)
            new_y = y + (y - og_x)
            while max_x - 1 > new_x > og_x and max_y - 1 > new_y > og_y:
                new_x = new_x + (x - og_x)
                new_y = new_y + (y - og_x)

    print(asteroid)
    new_map = deepcopy(sm)
    for x, y in blocked_coords:
        new_map[x][y] = "x"
    for x, y in sights:
        new_map[x][y] = "O"
    new_map[og_x][og_y] = "#"
    print()
    print_star_map(new_map)
    print()
    print(visible_count)
    return visible_count


if __name__ == "__main__":
    star_map = read_map()
    print_star_map(star_map)
    asteroids = find_asteroids(star_map)
    results = {}
    for asteroid in asteroids:
        results[asteroid] = count_viewable_asteroids(star_map, asteroid)
    print()
    max_asteroid = max(results, key=results.get)
    print(max_asteroid)
    print(results[max_asteroid])
