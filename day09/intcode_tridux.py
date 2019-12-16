from collections import defaultdict

SYSTEM_ID = 1
RELATIVE_BASE = 0


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
        opcode[param1] = SYSTEM_ID
        return position + 2, False
    elif op == "04":
        param1 = get_params(opcode, modes, position, op)
        print(param1)
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


print(f"part one:")
opcode = run_intcode()
position = 0
finished = False
while not finished:
    position, finished = process_op(opcode, position)
print()
print(f"part two:")
SYSTEM_ID = 2
RELATIVE_BASE = 0
opcode = run_intcode()
position = 0
finished = False
while not finished:
    position, finished = process_op(opcode, position)
