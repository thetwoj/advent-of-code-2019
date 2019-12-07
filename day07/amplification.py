import itertools
import queue
from threading import Thread


class Amplifier:
    def __init__(self, name, input_queue, output_queue):
        self.name = name
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.stop_thread = False

    def process_op(self, opcode, position):
        instruction = str(opcode[position]).zfill(5)
        op = instruction[-2:]

        modes = instruction[:3]
        if op == "01":
            param1, param2, param3 = get_params(opcode, modes, position, op)
            opcode[param3] = param1 + param2
            return self.process_op(opcode, position + 4)
        elif op == "02":
            param1, param2, param3 = get_params(opcode, modes, position, op)
            opcode[param3] = param1 * param2
            return self.process_op(opcode, position + 4)
        elif op == "03":
            next_input = self.input_queue.get()
            opcode[opcode[position + 1]] = next_input
            return self.process_op(opcode, position + 2)
        elif op == "04":
            param1 = get_params(opcode, modes, position, op)
            self.output_queue.put(param1)
            return self.process_op(opcode, position + 2)
        elif op == "05":
            param1, param2 = get_params(opcode, modes, position, op)
            if param1 != 0:
                return self.process_op(opcode, param2)
            return self.process_op(opcode, position + 3)
        elif op == "06":
            param1, param2 = get_params(opcode, modes, position, op)
            if param1 == 0:
                return self.process_op(opcode, param2)
            return self.process_op(opcode, position + 3)
        elif op == "07":
            param1, param2, param3 = get_params(opcode, modes, position, op)
            opcode[param3] = 1 if param1 < param2 else 0
            return self.process_op(opcode, position + 4)
        elif op == "08":
            param1, param2, param3 = get_params(opcode, modes, position, op)
            opcode[param3] = 1 if param1 == param2 else 0
            return self.process_op(opcode, position + 4)
        elif op == "99":
            return opcode
        else:
            print(f"Invalid op found at position {position}: {instruction}")

    def run_intcode(self):
        with open("input.txt") as f:
            opcode = [int(op) for op in f.readline().split(",")]

        return self.process_op(opcode, 0)


def set_up_amplifiers(count, phase_settings, feedback=False):
    input_queue = queue.Queue()
    amps = []
    for x in range(count):
        input_queue.put(phase_settings[x])
        if x == 0:
            input_queue.put(0)
        output_queue = queue.Queue()
        amps.append(Amplifier(x, input_queue, output_queue))
        input_queue = output_queue
        if feedback and x == count - 1:
            amps[-1].output_queue = amps[0].input_queue
    return amps


def get_params(opcode, modes, position, op):
    param1 = opcode[opcode[position + 1]] if modes[2] == "0" else opcode[position + 1]
    if op in ["04"]:
        return param1
    param2 = opcode[opcode[position + 2]] if modes[1] == "0" else opcode[position + 2]
    if op in ["05", "06"]:
        return param1, param2
    param3 = opcode[position + 3]
    return param1, param2, param3


def controller(amp_count, phase_min, feedback=False):
    output = []
    phase_settings = itertools.permutations(
        [x for x in range(phase_min, phase_min + amp_count)]
    )
    for phase_setting in phase_settings:
        amps = set_up_amplifiers(amp_count, phase_setting, feedback)
        threads = []
        for amp in amps:
            t = Thread(target=amp.run_intcode)
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        final_output = amps[-1].output_queue.get()
        output.append(final_output)

    return max(output)


if __name__ == "__main__":
    print(f"part one: {controller(5, 0, False)} is highest thruster signal")
    print()
    print(
        f"part two: {controller(5, 5, True)} is highest thruster signal with feedback"
    )
