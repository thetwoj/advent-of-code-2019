import math


def part_one():
    masses = []
    with open('input.txt') as f:
        for line in f:
            masses.append(int(line))

    return [math.floor(m/3)-2 for m in masses]


def part_two(fuels):
    recursive_fuel_req = [recursive_mass(fuel_mass) for fuel_mass in fuels]
    return sum(recursive_fuel_req)


def recursive_mass(fuel):
    fuel_req_by_fuel = math.floor(fuel / 3) - 2
    if fuel_req_by_fuel <= 0:
        return fuel
    return fuel + recursive_mass(fuel_req_by_fuel)


if __name__ == "__main__":
    fuel_req = part_one()
    print(f'part one:\n{sum(fuel_req)}')
    print()
    total_fuel = part_two(fuel_req)
    print(f'part two:\n{total_fuel}')
