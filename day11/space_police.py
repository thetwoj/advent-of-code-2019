from collections import defaultdict

RELATIVE_BASE = 0
CURRENT_X = 0
CURRENT_Y = 0
MAP = defaultdict(int)
COLOR_STEP = True
DIRECTION = "U"


def reset_globals():
    global CURRENT_X, CURRENT_Y, COLOR_STEP, DIRECTION
    CURRENT_X = 0
    CURRENT_Y = 0
    COLOR_STEP = True
    DIRECTION = "U"


def run_intcode():
    with open("input.txt") as f:
        opcode = defaultdict(int)
        for index, op in enumerate(f.readline().split(",")):
            opcode[index] = int(op)
    return opcode


def get_params(opcode, modes, position, op):
    global RELATIVE_BASE
    if modes[2] == "0":
        param1 = opcode[opcode[position + 1]]
    elif modes[2] == "1":
        param1 = opcode[position + 1]
    elif modes[2] == "2":
        param1 = opcode[opcode[position + 1] + RELATIVE_BASE]

    if op in ["09"]:
        RELATIVE_BASE += param1
        return param1

    if op in ["03", "04"]:
        if op == "03":
            if modes[2] in ["0", "1"]:
                param1 = opcode[position + 1]
            elif modes[2] == "2":
                param1 = opcode[position + 1] + RELATIVE_BASE
        return param1

    if modes[1] == "0":
        param2 = opcode[opcode[position + 2]]
    elif modes[1] == "1":
        param2 = opcode[position + 2]
    elif modes[1] == "2":
        param2 = opcode[opcode[position + 2] + RELATIVE_BASE]

    if op in ["05", "06"]:
        return param1, param2

    if modes[0] in ["0", "1"]:
        param3 = opcode[position + 3]
    elif modes[0] == "2":
        param3 = opcode[position + 3] + RELATIVE_BASE
    return param1, param2, param3


def process_op(opcode, position):
    global DIRECTION, CURRENT_X, CURRENT_Y, COLOR_STEP
    instruction = str(opcode[position]).zfill(5)
    op = instruction[-2:]

    modes = instruction[:3]
    if op == "01":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = param1 + param2
        return position + 4, False
    elif op == "02":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = param1 * param2
        return position + 4, False
    elif op == "03":
        param1 = get_params(opcode, modes, position, op)
        opcode[param1] = MAP[(CURRENT_X, CURRENT_Y)]
        return position + 2, False
    elif op == "04":
        param1 = get_params(opcode, modes, position, op)
        if COLOR_STEP:
            MAP[(CURRENT_X, CURRENT_Y)] = param1
            COLOR_STEP = False
        else:
            if param1 == 0:
                if DIRECTION == "U":
                    DIRECTION = "L"
                elif DIRECTION == "L":
                    DIRECTION = "D"
                elif DIRECTION == "D":
                    DIRECTION = "R"
                else:
                    DIRECTION = "U"
            elif param1 == 1:
                if DIRECTION == "U":
                    DIRECTION = "R"
                elif DIRECTION == "R":
                    DIRECTION = "D"
                elif DIRECTION == "D":
                    DIRECTION = "L"
                else:
                    DIRECTION = "U"
            if DIRECTION == "U":
                CURRENT_Y += 1
            elif DIRECTION == "L":
                CURRENT_X -= 1
            elif DIRECTION == "D":
                CURRENT_Y -= 1
            elif DIRECTION == "R":
                CURRENT_X += 1
            COLOR_STEP = True
        return position + 2, False
    elif op == "05":
        param1, param2 = get_params(opcode, modes, position, op)
        if param1 != 0:
            return param2, False
        return position + 3, False
    elif op == "06":
        param1, param2 = get_params(opcode, modes, position, op)
        if param1 == 0:
            return param2, False
        return position + 3, False
    elif op == "07":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = 1 if param1 < param2 else 0
        return position + 4, False
    elif op == "08":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = 1 if param1 == param2 else 0
        return position + 4, False
    elif op == "09":
        get_params(opcode, modes, position, op)
        return position + 2, False
    elif op == "99":
        return 0, True
    else:
        print(f"Invalid op found at position {position}: {instruction}")


def run():
    global MAP
    print(f"part one:")
    opcode = run_intcode()
    position = 0
    finished = False
    while not finished:
        position, finished = process_op(opcode, position)
    print(len(MAP))

    MAP.clear()
    MAP[(0, 0)] = 1
    reset_globals()
    print()
    print(f"part two:")
    opcode = run_intcode()
    position = 0
    finished = False
    while not finished:
        position, finished = process_op(opcode, position)

    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for x, y in MAP:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y

    transposed_map = {}
    for x, y in MAP:
        color = MAP[(x, y)]
        x -= min_x
        y -= min_y
        transposed_map[(x, y)] = color

    printable_map = [
        [" " for _ in range(max_y - min_y + 1)] for _ in range(max_x - min_x + 1)
    ]
    for x, y in transposed_map:
        printable_map[x][y] = " " if transposed_map[(x, y)] == 0 else "#"

    for y in range(max_y - min_y, -1, -1):
        for x in range(max_x - min_x + 1):
            if x == max_x - min_x:
                print(printable_map[x][y])
            else:
                print(printable_map[x][y], end="")


if __name__ == "__main__":
    run()
