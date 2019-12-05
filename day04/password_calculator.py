def get_input():
    with open("input.txt") as f:
        line = f.readline().strip()
    return int(line.split("-")[0]), int(line.split("-")[1])


def digits_decrease(x):
    prev_digit = "0"
    for digit in str(x):
        if digit < prev_digit:
            return True
        prev_digit = digit
    return False


def no_double(x):
    prev_digit = None
    for digit in str(x):
        if digit == prev_digit:
            return False
        prev_digit = digit
    return True


def has_isolated_double(x):
    prev_prev_digit = None
    prev_digit = None
    isolated_double = False
    for index, digit in enumerate(str(x)):
        if index < len(str(x)) - 1:
            next_digit = str(x)[index + 1]
        else:
            next_digit = None
        # first two digits are an isolated double
        if not prev_prev_digit and prev_digit == digit != next_digit:
            isolated_double = True
        # any two digits that aren't in the first or last index are an isolated double
        if prev_prev_digit != prev_digit == digit != next_digit:
            isolated_double = True
        # last two digits are an isolated double
        if prev_prev_digit != prev_digit == digit and not next_digit:
            isolated_double = True
        prev_prev_digit = prev_digit
        prev_digit = digit
    if isolated_double:
        return True


def calculate_passwords(low, up, part=1):
    candidates = set()
    for x in range(low, up):
        if digits_decrease(x):
            continue
        if part == 1 and no_double(x):
            continue
        elif part == 2 and not has_isolated_double(x):
            continue
        candidates.add(x)

    return candidates


if __name__ == "__main__":
    lower, upper = get_input()
    password_candidates = calculate_passwords(lower, upper, 1)
    print(f"part one:\n{len(password_candidates)}")
    print()
    password_candidates = calculate_passwords(lower, upper, 2)
    print(f"part two:\n{len(password_candidates)}")
