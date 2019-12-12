from copy import deepcopy
import math


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


def count_viewable_asteroids(sm, station, asteroids, print_map=False):
    blocked_coords = set()
    blocked_coords.add(station)
    sights = set()
    visible_count = 0
    og_x, og_y = station
    max_x = len(sm)
    max_y = len(sm[0])

    distances = {}
    for a_x, a_y in asteroids:
        distances[(a_x, a_y)] = abs(og_x - a_x) + abs(og_y - a_y)
    distances = sorted(distances, key=distances.get)

    for x, y in distances:
        if (x, y) in blocked_coords or sm[x][y] != "#":
            continue
        visible_count += 1
        sights.add((x, y))
        # blocked_coords.add((x, y))

        if og_x == x:
            if y < og_y:
                for new_y in range(0, og_y + 1):
                    if sm[x][new_y] == "#":
                        blocked_coords.add((x, new_y))
                continue
            else:
                for new_y in range(og_y, max_y):
                    if sm[x][new_y] == "#":
                        blocked_coords.add((x, new_y))
                continue

        if og_y == y:
            if x < og_x:
                for new_x in range(0, og_x + 1):
                    if sm[new_x][y] == "#":
                        blocked_coords.add((new_x, y))
                continue
            else:
                for new_x in range(og_x, max_x):
                    if sm[new_x][y] == "#":
                        blocked_coords.add((new_x, y))
                continue

        gcd = math.gcd(abs(x - og_x), abs(y - og_y))
        if x > og_x and y > og_y:
            new_x = x + (x - og_x) // gcd
            new_y = y + (y - og_y) // gcd
            while max_x > new_x > og_x and max_y > new_y > og_y:
                blocked_coords.add((new_x, new_y))
                new_x = new_x + (x - og_x) // gcd
                new_y = new_y + (y - og_y) // gcd
            new_x = x - (x - og_x) // gcd
            new_y = y - (y - og_y) // gcd
            while max_x > new_x > og_x and max_y > new_y > og_y:
                blocked_coords.add((new_x, new_y))
                new_x = new_x - (x - og_x) // gcd
                new_y = new_y - (y - og_y) // gcd

        if x > og_x and y < og_y:
            new_x = x - (og_x - x) // gcd
            new_y = y - (og_y - y) // gcd
            while max_x > new_x > og_x and og_y > new_y >= 0:
                blocked_coords.add((new_x, new_y))
                new_x = new_x - (og_x - x) // gcd
                new_y = new_y - (og_y - y) // gcd
            new_x = x + (og_x - x) // gcd
            new_y = y + (og_y - y) // gcd
            while max_x > new_x > og_x and og_y > new_y >= 0:
                blocked_coords.add((new_x, new_y))
                new_x = new_x + (og_x - x) // gcd
                new_y = new_y + (og_y - y) // gcd

        if x < og_x and y > og_y:
            new_x = x - (og_x - x) // gcd
            new_y = y - (og_y - y) // gcd
            while og_x > new_x >= 0 and max_y > new_y > og_y:
                blocked_coords.add((new_x, new_y))
                new_x = new_x - (og_x - x) // gcd
                new_y = new_y - (og_y - y) // gcd
            new_x = x + (og_x - x) // gcd
            new_y = y + (og_y - y) // gcd
            while og_x > new_x >= 0 and max_y > new_y > og_y:
                blocked_coords.add((new_x, new_y))
                new_x = new_x + (og_x - x) // gcd
                new_y = new_y + (og_y - y) // gcd

        if x < og_x and y < og_y:
            new_x = x + (x - og_x) // gcd
            new_y = y + (y - og_y) // gcd
            while og_x > new_x >= 0 and og_y > new_y >= 0:
                blocked_coords.add((new_x, new_y))
                new_x = new_x + (x - og_x) // gcd
                new_y = new_y + (y - og_y) // gcd
            new_x = x - (x - og_x) // gcd
            new_y = y - (y - og_y) // gcd
            while og_x > new_x >= 0 and og_y > new_y >= 0:
                blocked_coords.add((new_x, new_y))
                new_x = new_x - (x - og_x) // gcd
                new_y = new_y - (y - og_y) // gcd

    if print_map:
        new_map = deepcopy(sm)
        for x, y in blocked_coords:
            new_map[x][y] = "x"
        for x, y in sights:
            new_map[x][y] = "O"
        new_map[og_x][og_y] = "#"
        print_star_map(new_map)
    return visible_count


if __name__ == "__main__":
    star_map = read_map()
    # print_star_map(star_map)
    asteroids = find_asteroids(star_map)
    results = {}
    for asteroid in asteroids:
        results[asteroid] = count_viewable_asteroids(star_map, asteroid, asteroids)
    # print()
    max_asteroid = max(results, key=results.get)
    print("part one:")
    count_viewable_asteroids(star_map, max_asteroid, asteroids, print_map=True)
    print(f"station coords: {max_asteroid}")
    viewable_asteroid_count = results[max_asteroid]
    print(f"visible asteroids: {viewable_asteroid_count}")
