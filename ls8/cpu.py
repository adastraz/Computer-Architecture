
"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.pc = 0
        self.reg = [None] * 8
        self.running = True
        self.sp = 7
        self.stack_start = 16
        self.stack_end = 240
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.ADD = 0b10100000
        self.SUB = 0b10100001
        self.MUL = 0b10100010
        self.MOD = 0b10100100
        self.PUSH = 0b01000101
        self.POP = 0b01000110

    def load(self, program):
        """Load a program into memory."""
        #    index     value        provide from arg
        for address, instruction in enumerate(program):
            self.ram[address] = instruction
            address += 1

    def run(self):
        """Run the CPU.       
        1. read mem at PC
        2. store result in local var
        3. turn into hash_tables
        """
        
        while self.running is True:
            IR = self.ram[self.pc]
            branch_table = {
                self.LDI: self.ldi,
                self.PRN: self.prn,
                self.HLT: self.hlt,
                self.ADD: self.add,
                self.SUB: self.sub,
                self.MUL: self.mul,
                self.DIV: self.div,
                self.MOD: self.mod,
                self.PUSH: self.push,
                self.POP: self.pop
            }
            if IR in branch_table:
                branch_table[IR]()
            else:
                print(f'Unknown instruction: {IR}, at address PC: {self.pc}')
                sys.exit(1)
            # branch_table.get(IR)()

    def alu(self, op, reg_a, reg_b):
        """ALU operations.
        Algorythmic Logic Units
        # add masking?
            use repl
        """
        self.alu_operations = {
            'MUL': self.mul,
            'ADD': self.add,
            'DIV': self.div,
            'SUB': self.sub,
            'MOD': self.mod
        }

        if op in self.alu_operations:
            self.alu_operations[op](reg_a, reg_b)
        else:
            raise Exception("Unsupported ALU operation")

        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        #     self.pc += 3
        #     print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        # elif op == "SUB":
        #     self.reg[reg_a] -= self.reg[reg_b]
        #     self.pc += 3
        #     print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        # elif op == "MUL":
        #     self.reg[reg_a] *= self.reg[reg_b]
        #     self.pc += 3
        #     print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        # elif op == "DIV":
        #     self.reg[reg_a] /= self.reg[reg_b]
        #     self.pc += 3
        #     print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        # elif op == "MOD":
        #     self.reg[reg_a] %= self.reg[reg_b]
        #     self.pc += 3
        #     print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")
        # else:
        #     raise Exception(f"Unsupported ALU operation: {op}")
        #     self.trace()

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


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def hlt(self):
        self.running = False
        self.pc += 1

    def prn(self):
        MAR = self.ram[self.pc + 1]
        self.reg[0]
        print("Returning", self.reg[MAR])
        self.pc +=2

    def ldi(self):
        MAR = self.ram[self.pc + 1]
        MDR = self.ram[self.pc + 2]
        self.reg[MAR] = MDR
        self.pc += 3

    def add(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]
        self.pc += 3
        print(f"ADD at REG[{reg_a}]: {self.reg[reg_a]}")
    
    def sub(self, reg_a, reg_b):
        self.reg[reg_a] -= self.reg[reg_b]
        self.pc += 3
        print(f"SUB at REG[{reg_a}]: {self.reg[reg_a]}")

    def mul(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]
        self.pc += 3
        print(f"MUL at REG[{reg_a}]: {self.reg[reg_a]}")

    def div(self, reg_a, reg_b):
        self.reg[reg_a] /= self.reg[reg_b]
        self.pc += 3
        print(f"DIV at REG[{reg_a}]: {self.reg[reg_a]}")

    def mod(self, reg_a, reg_b):
        self.reg[reg_a] %= self.reg[reg_b]
        self.pc += 3
        print(f"MOD at REG[{reg_a}]: {self.reg[reg_a]}")

    def push(self):
        # self.reg[7] = 104 reg 0 - 8
        self.reg[self.sp] -= 1 
        reg_id = self.ram[self.pc + 1]
        # value = new ram index after stack push
        value = self.reg[reg_id]
        top_loc = self.reg[self.sp]
        self.ram[top_loc] = value
        print("PC:", self.pc)
        print("RAM:", self.ram)
        print("REG:", self.reg)
        # print("PUSH", "Reg_LOC:", self.sp , "Ram_Loc:",  reg_id, "Val:", self.ram[top_loc])
        self.pc += 2

    def pop(self):
        # OLD Head
        top_loc = self.reg[self.sp] #244
        # lets get the register address

        # NEW HEAD
        reg_id = self.ram[self.pc + 1]
        # overwrite our reg address with the value of our memory address we are looking at
        self.reg[reg_id] = self.ram[top_loc]

        self.reg[self.sp] += 1 #243
        self.pc += 2