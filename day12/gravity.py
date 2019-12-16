import math


class Planet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.x_vel = 0
        self.y_vel = 0
        self.z_vel = 0

    def apply_velocity(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.z += self.z_vel

    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return abs(self.x_vel) + abs(self.y_vel) + abs(self.z_vel)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()


def process_input():
    planets = []
    with open("input.txt") as f:
        for line in f:
            x, y, z = line.strip().replace("<", "").replace(">", "").split(", ")
            planets.append(
                Planet(
                    int(x.split("=")[-1]), int(y.split("=")[-1]), int(z.split("=")[-1])
                )
            )

    return planets


def apply_gravity(p1, p2):
    if p1.x > p2.x:
        p1.x_vel -= 1
        p2.x_vel += 1
    elif p1.x < p2.x:
        p1.x_vel += 1
        p2.x_vel -= 1

    if p1.y > p2.y:
        p1.y_vel -= 1
        p2.y_vel += 1
    elif p1.y < p2.y:
        p1.y_vel += 1
        p2.y_vel -= 1

    if p1.z > p2.z:
        p1.z_vel -= 1
        p2.z_vel += 1
    elif p1.z < p2.z:
        p1.z_vel += 1
        p2.z_vel -= 1


def current_state(planets, find):
    state_string = ""
    for planet in planets:
        if find == "x":
            state_string += str(planet.x) + str(planet.x_vel)
        elif find == "y":
            state_string += str(planet.y) + str(planet.y_vel)
        elif find == "z":
            state_string += str(planet.z) + str(planet.z_vel)
    return state_string


def step(planets):
    for index, planet in enumerate(planets):
        for second_planet in planets[index:]:
            apply_gravity(planet, second_planet)
    for planet in planets:
        planet.apply_velocity()


def total_energy(planets):
    return sum([planet.total_energy() for planet in planets])


def find_repeats(planets):
    initial_x_state = current_state(planets, "x")
    initial_y_state = current_state(planets, "y")
    initial_z_state = current_state(planets, "z")
    x_period, y_period, z_period = 0, 0, 0
    step(planets)
    steps = 1
    while 0 in [x_period, y_period, z_period]:
        step(planets)
        steps += 1
        if x_period == 0 and current_state(planets, "x") == initial_x_state:
            x_period = steps
        if y_period == 0 and current_state(planets, "y") == initial_y_state:
            y_period = steps
        if z_period == 0 and current_state(planets, "z") == initial_z_state:
            z_period = steps
    return x_period, y_period, z_period


def lcm(a, b):
    return a * b // math.gcd(a, b)


def run():
    planets = process_input()
    for x in range(1000):
        step(planets)
    print(f"part one: {total_energy(planets)} total energy\n")
    x, y, z = find_repeats(planets)
    print(f"part two: {lcm(lcm(x, y), z)} steps")


if __name__ == "__main__":
    run()
