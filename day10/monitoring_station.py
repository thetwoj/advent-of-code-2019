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
    return asteroids


def count_viewable_asteroids(sm, station, asteroids, print_map=False):
    blocked_coords = set()
    blocked_coords.add(station)
    sights = set()
    og_x, og_y = station
    max_x = len(sm)
    max_y = len(sm[0])

    # calculate manhattan distance to asteroids so we visit nearest ones first
    distances = {}
    for a_x, a_y in asteroids:
        distances[(a_x, a_y)] = abs(og_x - a_x) + abs(og_y - a_y)
    distances = sorted(distances, key=distances.get)

    for x, y in distances:
        if (x, y) in blocked_coords or sm[x][y] != "#":
            continue
        sights.add((x, y))

        gcd = math.gcd(abs(og_x - x), abs(og_y - y))
        diff_x = (og_x - x) // gcd
        diff_y = (og_y - y) // gcd

        new_x = x - diff_x
        new_y = y - diff_y
        while max_x > new_x >= 0 and max_y > new_y >= 0:
            if sm[new_x][new_y] == "#":
                blocked_coords.add((new_x, new_y))
            new_x -= diff_x
            new_y -= diff_y

    # Print map if requested
    if print_map:
        new_map = deepcopy(sm)
        for x, y in blocked_coords:
            new_map[x][y] = "x"
        for x, y in sights:
            new_map[x][y] = "O"
        new_map[og_x][og_y] = "#"
        print_star_map(new_map)

    return sights


def run():
    star_map = read_map()
    asteroids = find_asteroids(star_map)
    results = {}
    for asteroid in asteroids:
        results[asteroid] = len(count_viewable_asteroids(star_map, asteroid, asteroids))
    max_asteroid = max(results, key=results.get)
    print("part one:")
    count_viewable_asteroids(star_map, max_asteroid, asteroids, print_map=True)
    print(f"station coords: {max_asteroid}")
    viewable_asteroid_count = results[max_asteroid]
    print(f"visible asteroids: {viewable_asteroid_count}")

    print()
    print("part two:")
    destroyed_count = 0
    while destroyed_count < 200:
        visible_asteroids = count_viewable_asteroids(star_map, max_asteroid, asteroids)
        asteroid_angles = {}
        station_x, station_y = max_asteroid
        for x, y in visible_asteroids:
            if station_x - x == 0:
                degrees = 0 if y < station_y else 180
            elif station_y - y == 0:
                degrees = 90 if x > station_x else 270
            else:
                degrees = math.degrees(
                    math.atan(abs(station_y - y) / abs(station_x - x))
                )

            if x > station_x and y > station_y:
                degrees += 90
            elif x < station_x and y > station_y:
                degrees = 90 - degrees
                degrees += 180
            elif x < station_x and y < station_y:
                degrees += 270
            elif 0 < degrees < 90:
                degrees = 90 - degrees

            asteroid_angles[(x, y)] = degrees
        # preserving the value in sorting is helpful for debugging but not necessary for answer
        sorted_angles = {
            k: v for k, v in sorted(asteroid_angles.items(), key=lambda item: item[1])
        }
        for asteroid in sorted_angles:
            del asteroids[asteroid]
            destroyed_count += 1
            if destroyed_count == 200:
                print(f"coords of 200th asteroid destroyed: {asteroid}")


if __name__ == "__main__":
    run()
