SYSTEM_ID = None


def run_intcode():
    with open("input.txt") as f:
        opcode = [int(op) for op in f.readline().split(",")]

    return process_op(opcode, 0)


def get_params(opcode, modes, position, op):
    param1 = opcode[opcode[position + 1]] if modes[2] == "0" else opcode[position + 1]
    if op in ["04"]:
        return param1
    param2 = opcode[opcode[position + 2]] if modes[1] == "0" else opcode[position + 2]
    if op in ["05", "06"]:
        return param1, param2
    param3 = opcode[position + 3]
    return param1, param2, param3


def process_op(opcode, position):
    instruction = str(opcode[position]).zfill(5)
    op = instruction[-2:]

    modes = instruction[:3]
    if op == "01":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = param1 + param2
        return process_op(opcode, position + 4)
    elif op == "02":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = param1 * param2
        return process_op(opcode, position + 4)
    elif op == "03":
        opcode[opcode[position + 1]] = SYSTEM_ID
        return process_op(opcode, position + 2)
    elif op == "04":
        param1 = get_params(opcode, modes, position, op)
        print(param1)
        return process_op(opcode, position + 2)
    elif op == "05":
        param1, param2 = get_params(opcode, modes, position, op)
        if param1 != 0:
            return process_op(opcode, param2)
        return process_op(opcode, position + 3)
    elif op == "06":
        param1, param2 = get_params(opcode, modes, position, op)
        if param1 == 0:
            return process_op(opcode, param2)
        return process_op(opcode, position + 3)
    elif op == "07":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = 1 if param1 < param2 else 0
        return process_op(opcode, position + 4)
    elif op == "08":
        param1, param2, param3 = get_params(opcode, modes, position, op)
        opcode[param3] = 1 if param1 == param2 else 0
        return process_op(opcode, position + 4)
    elif op == "99":
        return opcode
    else:
        print(f"Invalid op found at position {position}: {instruction}")


if __name__ == "__main__":
    SYSTEM_ID = 1
    print(f"part one:")
    run_intcode()
    print()
    SYSTEM_ID = 5
    print(f"part two:")
    results = run_intcode()
