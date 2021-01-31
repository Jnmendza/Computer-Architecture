import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # PC
        self.pc = 0
        # REGISTER
        self.reg = [0] * 8
        # RAM
        self.ram = [0] * 256
        self.SP = 7

    def load(self):
        """Load a program into memory."""
        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    # Ignore comments
                    comment_split = line.split('#')
                    # print("commentsplit", comment_split)
                    # Strip out the white space
                    num = comment_split[0].strip()
                    print("num", num)
                    # Ignore blank lines
                    if num == "":
                        continue

                    val = int(num, 2)
                    self.ram[address] = val
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

    # Memory Address Register (MAR)
    # Memory Data Register (MDR).
    def ram_read(self, MAR):  # should accept the address to read and return the value stored there.
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):  # should accept a value to write, and the address to write it to.
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        running = True

        while running:
            ir = self.ram[self.pc]
            # LDI - load "immediate", "set this register to this value".
            if ir == LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                self.pc += 3

            # PRN - a pseudo-instruction that prints the numeric value stored in a register.
            elif ir == PRN:
                num = self.ram[self.pc + 1]
                print(self.reg[num])
                self.pc += 2

            # MUL - # Expected output: 72
            elif ir == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                self.pc += 3

            # PUSH
            elif ir == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                self.SP -= 1
                self.ram[self.SP] = val
                self.pc += 2

            # POP
            elif ir == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.SP]
                self.reg[reg] = val
                self.SP += 1
                self.pc += 2

            # CALL
            elif ir == CALL:
                val = self.pc + 2
                reg = self.ram[self.pc + 1]
                sub = self.reg[reg]
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = val
                self.pc = sub

            # RET
            elif ir == RET:
                pc = self.reg[self.SP]
                self.pc = self.ram[pc]

            # ADD
            elif ir == ADD:
                self.alu('ADD', self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3

            # HLT - halt the CPU and exit the emulator.
            elif ir == HLT:
                running = False
                self.pc += 1

            else:
                print(f'command not found')
                sys.exit(1)
