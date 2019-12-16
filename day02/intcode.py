def run_intcode(pos1=12, pos2=2):
    with open("input.txt") as f:
        opcode = [int(op) for op in f.readline().split(",")]
    opcode[1] = pos1
    opcode[2] = pos2

    return process_op(opcode, 0)


def process_op(opcode, position):
    instruction = opcode[position]
    output_loc = opcode[position + 3]
    if instruction == 1:
        opcode[output_loc] = opcode[opcode[position + 1]] + opcode[opcode[position + 2]]
        return process_op(opcode, position + 4)
    elif instruction == 2:
        opcode[output_loc] = opcode[opcode[position + 1]] * opcode[opcode[position + 2]]
        return process_op(opcode, position + 4)
    elif instruction == 99:
        return opcode
    else:
        print(f"Invalid op found at position {position}: {instruction}")


results = run_intcode()
print(f"part one:\n{results[0]}")
print()
for noun in range(99):
    for verb in range(99):
        results = run_intcode(noun, verb)
        if results[0] == 19690720:
            print(f"part two: noun - {noun}, verb - {verb}")
            print(f"{100 * noun + verb}")
