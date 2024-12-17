
import src.util as util

class Program:
    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.addr = 0
        self.prog = program
        self.terminated = False
        self.output = []
    def combo_operand(self, val):
        if val >= 0 and val <= 3:
            return val
        elif val == 4:
            return self.A
        elif val == 5:
            return self.B
        elif val == 6:
            return self.B
        # assume val will never be 7
    def execute(self):
        if self.terminated:
            return
        match self.prog[self.addr]:
            case 0: #adv
                numerator = self.A
                denominator = 2**self.combo_operand(self.prog[self.addr + 1])
                self.A = numerator//denominator
                self.addr += 2
            case 1: #bxl
                self.B = self.B ^ self.prog[self.addr + 1]
                self.addr += 2
            case 2: #bst
                self.B = self.combo_operand(self.prog[self.addr + 1]) % 8
                self.addr += 2
            case 3: #jnz
                if self.A != 0:
                    self.addr = self.prog[self.addr + 1]
                else:
                    self.addr += 2
            case 4: #bxc
                self.B = self.B ^ self.C
                self.addr += 2
            case 5: #out
                self.output.append(self.combo_operand(self.prog[self.addr + 1]) % 8)
                self.addr += 2
            case 6: #bdv
                numerator = self.A
                denominator = 2**self.combo_operand(self.prog[self.addr + 1])
                self.B = numerator//denominator
                self.addr += 2
            case 7: #cdv
                numerator = self.A
                denominator = 2**self.combo_operand(self.prog[self.addr + 1])
                self.C = numerator//denominator
                self.addr += 2
        if self.addr >= len(self.prog):
            self.terminated = True

# Find a quine of the input program by trialing new tribit terms until 
# the all digits can be matched.
def quine_find(program):
    candidates = { 0 }
    # Starting with the final digit of the program and working backwards
    # find each prev_candidate << 3 + new tribits that adds the correct next
    # digit as the first output by the program
    for num in reversed(program):
        new_candidates = set()
        for c in candidates:
            for new_tribit in range(8):
                new_A = (c << 3) + new_tribit
                # If new_A results in a first digit that matches
                # the program digit, it's a candidate
                if run_program(program, new_A)[0] == num:
                    new_candidates.add(new_A)
        candidates = new_candidates
    if not run_program(program, min(candidates)) == program:
        return False
    return min(candidates)

# Run the program with the given A value and return the output
def run_program(program, A):
    prog = Program(A,0,0,program)
    while not prog.terminated:
        prog.execute()
    return prog.output

def day17(lines):
    part1 = 0
    part2 = 0
    A = util.numbers_in_string(lines[0])[0]
    B = util.numbers_in_string(lines[1])[0]
    C = util.numbers_in_string(lines[2])[0]
    program = util.numbers_in_string(lines[4])
    # Part 1: Execute the program and convert to a comma-joined string
    part1 = ",".join(list(map(lambda x: "{}".format(x),run_program(program, A))))
    # Part 2: Reverse engineer a quine
    part2 = quine_find(program)
    print("Part 1:", part1)
    print("Part 2:", part2)
    