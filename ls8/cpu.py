"""
CPU functionality.
"""

'''
SPRINT QUESTIONS:

1. The CALL instruction doesn't allow you to pass any arguments. 
What are some ways to effectively get arguments to a subroutine?
    
    used the self.pc when defining the CPU class. all children have access to the parent class self init. Also used other functions
    that can take arguments inside the CALL function to get values from other places

2. What's the result of bitwise-AND between `0b110` and `0b011`?

 a   1   1   0
 b   0   1   1
     0   1   0 = 1
    False
    Each bit of the output is 1 if the corresponding bit of 
    a AND of b is 1(true), otherwise it’s 0(false).

3. Convert the 8-bit binary number 0bXXXXXXXX (PM's choice) to hex.
    -there are an even number of binary bits per hex digit: 4 bits per hex digit
    -Hexadecimal numbers can be 0-9, or A (10) - F (15), since hexadecimal is base-16 8,4,2,1
    -split into sequences of 4 bits

0000  1010 = 0 + 0 + 2 + 0 + 8 0A
To run test for sprint:
    python3 ls8.py examples/sctest.ls8
'''


import sys
LDI = 0b10000010  # LDI R0,8
PRN = 0b01000111  # PRN R0
HLT = 0b00000001  # HLT
MUL = 0b10100010  # MUL R0,R1
PUSH = 0b01000101  # PUSH R0
POP = 0b01000110  # POP R0
CALL = 0b01010000  # CALL R1
RET = 0b00010001  # RET
ADD = 0b10100000  # ADD
# sprint
CMP = 0b10100111  # CMP
JEQ = 0b01010101  # JEQ
JMP = 0b01010100  # JMP
JNE = 0b01010110  # JNE


class CPU:
    """Main CPU class."""

    def __init__(self):
        """
        Construct a new CPU.
        """
        # Add list properties to the CPU class to hold 256 bytes of memory
        self.ram = [0] * 256

        # and 8 general-purpose registers.
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.reg = [0] * 8
        self.reg[7] = 0xf4

        # The SP points at the value at the top of the stack (most recently pushed),
        # or at address F4 if the stack is empty.
        # R7 is reserved as the stack pointer (SP)
        self.sp = 7

        # Also add properties for any internal registers you need, e.g. PC
        # Program Counter, address of the currently executing instruction
        self.pc = 0

        # he flags register `FL` holds the current flags status. These flags
        # can change based on the operands given to the `CMP` opcode.
        self.flag = 0b00000000

        # is pc on
        self.running = True

        self.branch_table = {
            LDI: self.ldi_fun,
            PRN: self.prn_fun,
            HLT: self.hlt_fun,
            MUL: self.mul_fun,
            PUSH: self.push_fun,
            POP: self.pop_fun,
            CALL: self.call_fun,
            RET: self.ret_fun,
            ADD: self.add_fun,
            # sprint
            CMP: self.cmp_fun,
            JEQ: self.jeq_fun,
            JMP: self.jmp_fun,
            JNE: self.jne_fun
        }

    # mar == Memory Address Register, holds the memory address we're reading or writing
    # mdr == Memory Data Register, holds the value to write or the value just read
    # ram_read() should accept the address to read and return the value stored there.
    def ram_read(self, mar):
        # current index of MAR
        return self.ram[mar]

    # ram_write() should accept a value to write, and the address to write it to
    def ram_write(self, mar, mdr):
        # mdr value at MAR
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""
        try:
            with open(filename) as f:
                address = 0
                for line in f:
                    # get rid of comments in programs
                    line = line.split('#')
                    num_str = line[0].strip()

                    if num_str == "":
                        continue
                    # at line 0, get the value with base 2. default is base 10
                    v = int(num_str, 2)
                    self.ram[address] = v
                    address += 1

        except FileNotFoundError:
            sys.exit(2)

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

        elif op == "CMP":
            # If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001  # HLT
            # If registerA is less than registerB, set the Less-than `L` flag to 1,
            # otherwise set it to 0.
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            #  If registerA is greater than registerB, set the Greater-than `G` flag
            # to 1, otherwise set it to 0
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010

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

    def ldi_fun(self, reg_a, reg_b):
        # if LDI This instruction sets a specified register to a specified value.
        self.reg[reg_a] = reg_b
        # 3 bytes long to move to next
        self.pc += 3

    def prn_fun(self, reg_a, reg_b):
        # if PRN At this point, you should be able to run
        # the program and have it print 8 to the console!
        print(f'Print this: {self.reg[reg_a]}')
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
        # Note: MUL is the responsiblity of the ALU, so it would be nice if your
        # code eventually called the alu() function with appropriate arguments to get the work done.
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def add_fun(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def push_fun(self, reg_a, reg_b):
        # print("pop", reg_a, reg_b)
        # decrement the SP
        self.reg[self.sp] -= 1
        # copy the value in the given register to the address pointed to by SP
        self.ram[self.reg[self.sp]] = self.reg[reg_a]
        self.pc += 2

    def pop_fun(self, reg_a, reg_b):
        # print("pop", reg_a, reg_b)
        # copy the value from the address pointed to by SP to the given reg
        self.reg[reg_a] = self.ram[self.reg[self.sp]]
        # increment SP
        self.reg[self.sp] += 1
        self.pc += 2

    # these args will not be used but are needed for the loop in run
    def call_fun(self, reg_a, reg_b):
        return_add = self.pc + 2
        # decrement the SP
        self.reg[self.sp] -= 1
        # The address of the instruction directly after CALL is pushed onto the stack.
        # This allows us to return to where we left off when the subroutine finishes executing.
        self.ram[self.reg[self.sp]] = return_add
        # The PC is set to the address stored in the given register.
        reg_num = self.ram[self.pc + 1]
        sub_add = self.reg[reg_num]
        self.pc = sub_add

    def ret_fun(self, reg_a, reg_b):
        # Return from subroutine.
        return_address = self.ram[self.reg[self.sp]]
        # Pop the value from the top of the stack
        self.reg[self.sp] += 1
        # and store it in the PC.
        self.pc = return_address

    def cmp_fun(self, reg_a, reg_b):
        # Compare the values in two registers
        # This is handled by ALU with flags
        self.alu("CMP", reg_a, reg_b)
        # 3bit instruction
        self.pc += 3

    def jeq_fun(self, reg_a, reg_b):
        # get the reg_num
        reg_num = self.ram_read(self.pc + 1)
        # If `equal` flag is set (true),
        if self.flag & 0b00000001 == 1:
            # jump to the address stored in the given register
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def jmp_fun(self, reg_a, reg_b):  # these args will not be used but are needed for the loop in run
        # Jump to the address stored in the given register.
        reg_num = self.ram_read(self.pc + 1)
        # Set the `PC` to the address stored in the given register
        self.pc = self.reg[reg_num]

    def jne_fun(self, reg_a, reg_b):
        # get the reg_num
        reg_num = self.ram_read(self.pc + 1)
        # If `E` flag is clear (false, 0),
        if self.flag & 0b00000001 == 0:
            # jump to the address stored in the given register
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        while self.running:
            # Instruction Register, contains a copy of the currently executing instruction
            ir = self.ram[self.pc]

            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            # print("ir", ir, reg_a, reg_b)
            if ir in self.branch_table:
                self.branch_table[ir](reg_a, reg_b)

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
                sys.exit(1)
