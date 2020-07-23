"""
CPU functionality.
CPU Emulator
Software that pretends to be hardware
Turing complete--solve any problem for which there is an algorithm 
(this only has 256 bytes of memory and is limited by it)
"""

import sys

LDI = 0b10000010  # LDI R0,8
PRN = 0b01000111  # PRN R0
HLT = 0b00000001  # HLT
MUL = 0b10100010  # MUL R0,R1
PUSH = 0b01000101  # PUSH R0
POP = 0b01000110  # POP R0
# Initialize and set default for our StackPointer
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """
        Construct a new CPU.
        """
        # Add list properties to the CPU class to hold 256 bytes of memory 
        self.ram = [0] * 256

        # and 8 general-purpose registers.
        self.reg = [0] * 8
        
        self.reg[SP] = 0xf4

        # Also add properties for any internal registers you need, e.g. PC
        # Program Counter, address of the currently executing instruction
        self.pc = 0
        
        # is pc on
        self.running = True

        self.branch_table = {
            LDI: self.ldi_fun,
            PRN: self.prn_fun,
            HLT: self.hlt_fun,
            MUL: self.mul_fun,
            PUSH: self.push_fun,
            POP: self.pop_fun
        }

    def load(self, filename):
        """Load a program into memory."""
        
        with open(filename) as f:
            address = 0

            for line in f:
                # get rid of comments in programs
                line = line.split('#')

                try:
                    # at line 0, get the value with base 2. default is base 10
                    v = int(line[0], 2)
                except ValueError:
                    continue

                self.ram[address] = v

                address += 1
        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8  save register 3 bytes long
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
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
    # Memory Address Register, holds the memory address we're reading or writing
    # Memory Data Register, holds the value to write or the value just read
    # ram_read() should accept the address to read and return the value stored there.
    def ram_read(self, mar):
        #current index of MAR
        mar_reg = self.ram[mar]
        return mar_reg

    # ram_write() should accept a value to write, and the address to write it to
    def ram_write(self, mar, mdr):
        # value at MAR
        self.ram[mar] = mdr

    def ldi_fun(self, reg_a, reg_b):
        # if LDI This instruction sets a specified register to a specified value.
        # get next value one away
        # reg_num = self.ram_read(self.pc + 1)
        # get next value two away
        # reg_val = self.ram_read(self.pc + 2)
        self.ram_write(reg_a, reg_b)
        # 3 bytes long to move to next
        self.pc += 3

    def prn_fun(self, reg_a, reg_b):
        # if PRN At this point, you should be able to run 
        # the program and have it print 8 to the console!
        # save our MAR to a variable
        # reg_num = self.ram_read(self.pc + 1)
        print(self.ram_read(reg_a))
        # increment to the next command 2 bytes long
        self.pc += 2

    def hlt_fun(self, reg_a, reg_b):
        # if HLT We can consider HLT to be similar to Python's exit() 
        # in that we stop whatever we are doing, wherever we are.
        # 1 byte instruction
        self.pc += 1
        # Set running to false
        self.running = False

    def mul_fun(self, reg_a, reg_b):
        # reg_a = self.ram_read(self.pc + 1)
        # reg_b = self.ram_read(self.pc + 2)
        #Note: MUL is the responsiblity of the ALU, so it would be nice if your 
        # code eventually called the alu() function with appropriate arguments to get the work done.
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def push_fun(self, reg_a, reg_b):
        pass

    def pop_fun(self, reg_a, reg_b):
        pass

    def run(self):
        """Run the CPU."""
        while self.running:
            # Instruction Register, contains a copy of the currently executing instruction
            ir = self.ram[self.pc]
            # print("ir", ir)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if ir in self.branch_table:
                self.branch_table[ir](reg_a, reg_b)
                      
            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)