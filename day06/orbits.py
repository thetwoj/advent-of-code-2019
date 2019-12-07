bodies = {}


class Body:
    def __init__(self, name, orbit=None):
        self.name = name
        self.orbit = orbit


def parse_input():
    with open("input.txt") as f:
        for line in f:
            orbit_name, body_name = line.strip().split(")")
            if orbit_name in bodies:
                orbit = bodies[orbit_name]
            else:
                orbit = Body(orbit_name)
                bodies[orbit_name] = orbit

            if body_name in bodies:
                body = bodies[body_name]
                body.orbit = orbit
            else:
                bodies[body_name] = Body(body_name, orbit)


def total_orbits():
    orbit_count = 0
    for _, body in bodies.items():
        orbit_count += recursive_orbit_depth(body, 0)
    return orbit_count


def recursive_orbit_depth(body, depth):
    if body.orbit:
        depth += 1
        return recursive_orbit_depth(body.orbit, depth)
    return depth


def recursive_orbit_names(body, names):
    names.append(body.name)
    if body.orbit:
        return recursive_orbit_names(body.orbit, names)
    return names


def path_intersections():
    santa = recursive_orbit_names(bodies["SAN"].orbit, [])
    you = recursive_orbit_names(bodies["YOU"].orbit, [])
    intersection = [x for x in santa if x in you][0]
    return santa.index(intersection) + you.index(intersection)


if __name__ == "__main__":
    parse_input()
    print(f"part one: {total_orbits()} total direct + indirect orbits")
    print()
    print(f"part two: {path_intersections()} moves for YOU to share same orbit as SAN")
