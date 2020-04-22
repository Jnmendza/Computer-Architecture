"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b10000111
MUL = 0b10100010

print(sys.argv)
program_filename = sys.argv[1]


# sys.exit()

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # construct RAM REG and PC
        # This builds 8 slots in the list [R0, R1, R2, etc]
        self.reg = [0] * 8
        # This builds 256 slots in the list for memory
        self.ram = [0] * 256
        self.pc = 0
        self.instructions = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            MUL: self.mul
        }

    def hlt(self):
        sys.exit(0)

    def ldi(self, operand_a, operand_b):
        # Set the value of register to an integer
        self.reg[operand_a] = operand_b

    def prn(self, operand_a):
        # print numeric value stored in the given register
        print(self.reg[operand_a])

    def load(self):
        """Load a program into memory."""

        # check for filename arg
        if len(sys.argv) != 2:
            print("ERROR: must have file name")
            sys.exit(1)

        address = 0

        try:
            with open(sys.argv[1]) as f:
                # read all the lines
                for line in f:
                    # parse out comments
                    comment_split = line.strip().split("#")

                    value = comment_split[0].strip()

                    # ignore blank lines
                    if value == "":
                        continue

                    # cast the numbers from strings to ints
                    num = int(value, 2)

                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """
        Run the CPU.
        Need to read the memory address that's stored in register PC
        Store that result in IR - Instruction Register. Local variable
        """
        running = True

        while running:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            inst_len = ((ir & 0b11000000) >> 6) + 1
            if ir in self.instructions:
                self.instructions[ir](operand_a, operand_b)
            else:
                print("Not valid")
            self.pc += inst_len

    def ram_read(self, mar):
        """
        mar - Memory Address Register read or written
        mdr - Memory Data Register that was read or written
        """
        # Where in the 256 individual slots of RAM are you looking?
        # When you find it, what is the value? Return the Value
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
