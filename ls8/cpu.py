"""
CPU functionality.
CPU Emulator
Software that pretends to be hardware
Turing complete--solve any problem for which there is an algorithm 
(this only has 256 bytes of memory and is limited by it)
"""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """
        Construct a new CPU.
        """
        #Add list properties to the CPU class to hold 256 bytes of memory 
        self.memory = [0] * 256

        # and 8 general-purpose registers.
        self.registers = [0] * 8

        #Also add properties for any internal registers you need, e.g. PC
        #Program Counter, address of the currently executing instruction
        self.pc = 0
        
        #is pc on
        self.running = True


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8  save register 3 bytes long
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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

    #ram_read() should accept the address to read and return the value stored there.
    def ram_read(self):
        pass

    #ram_write() should accept a value to write, and the address to write it to
    def ram_write(self):
        pass

    def run(self):
        """Run the CPU."""
        while self.running:
            #Instruction Register, contains a copy of the currently executing instruction
            ir = self.memory[self.pc]

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)