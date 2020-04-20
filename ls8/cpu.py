"""CPU functionality."""

import sys


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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

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
        """Run the CPU."""
        pass

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
