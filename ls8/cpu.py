"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for instruction in f:
                    try:
                        instruction = instruction.strip()
                        instruction = instruction.split('#', 1)[0]
                        instruction = int(instruction, 2)
                        # print(instruction)
                        self.ram[address] = instruction
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)


    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            inst = self.ram_read(self.pc)
            if inst == 0b00000001: #HLT
                ## HALT
                running = False
            elif inst == 0b01000111:
                ## PRN print value in giver register
                reg = self.ram_read(self.pc + 1)
                print(self.reg[reg])
                self.pc += 2
            elif inst == 0b10000010:
                ## LDI set register to value
                reg = self.pc + 1
                val = self.pc + 2
                self.reg[self.ram_read(reg)] = self.ram_read(val)
                self.pc += 3
            elif inst == 0b10100010:
                ## MULT regA and regB together, store esults in regA
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu('MUL', reg_a, reg_b)
                self.pc += 3

