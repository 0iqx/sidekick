"""
Sidekick's code without any human modifications.
"""

class SimpleVM:
    def __init__(self, bytecode, stack_size=1024, memory_size=1024):
        self.ip = 0
        self.bytecode = bytecode
        self.stack = [0] * stack_size
        self.stack_top = 0
        self.memory = [0] * memory_size
        self.result = 0

    def next_op(self):
        op = self.bytecode[self.ip]
        self.ip += 1
        return op

    def next_arg(self):
        arg = (self.bytecode[self.ip] << 8) + self.bytecode[self.ip + 1]
        self.ip += 2
        return arg

    def pop(self):
        self.stack_top -= 1
        return self.stack[self.stack_top]

    def push(self, val):
        self.stack[self.stack_top] = val
        self.stack_top += 1

    def peek(self):
        return self.stack[self.stack_top - 1]

    def tos_ptr(self):
        return self.stack_top - 1

    def interpret(self):
        while self.ip < len(self.bytecode):
            instruction = self.next_op()
            if instruction == 0x00:  # OP_RETURN_4
                print("OP_RETURN_4: Return 4")
                return 4
            elif instruction == 0x01:  # OP_PUSH_IMMEDIATE
                arg = self.next_arg()
                self.push(arg)
                print(f"OP_PUSH_IMMEDIATE: Pushed 0x{arg:04x} onto the stack")
            elif instruction == 0x02:  # OP_PUSH_MEMORY
                addr = self.next_arg()
                val = self.memory[addr]
                self.push(val)
                print(f"OP_PUSH_MEMORY: Pushed value 0x{val:016x} from memory address 0x{addr:04x} onto the stack")
            elif instruction == 0x03:  # OP_PUSH_MEMORY_ALT
                addr = self.next_arg()
                val = self.memory[addr]
                self.push(val)
                print(f"OP_PUSH_MEMORY_ALT: Pushed value 0x{val:016x} from memory address 0x{addr:04x} onto the stack")
            elif instruction == 0x04:  # OP_STORE_MEMORY
                addr = self.next_arg()
                val = self.pop()
                self.memory[addr] = val
                print(f"OP_STORE_MEMORY: Stored 0x{val:016x} into memory address 0x{addr:04x}")
            elif instruction == 0x05:  # OP_PUSH_MEMORY_2
                addr = self.pop()
                val = self.memory[addr]
                self.push(val)
                print(f"OP_PUSH_MEMORY_2: Pushed value 0x{val:016x} from memory address 0x{addr:04x} onto the stack")
            elif instruction == 0x06:  # OP_STORE_MEMORY_2
                val = self.pop()
                addr = self.pop()
                self.memory[addr] = val
                print(f"OP_STORE_MEMORY_2: Stored 0x{val:016x} into memory address 0x{addr:04x}")
            elif instruction == 0x07:  # OP_DUP
                val = self.peek()
                self.push(val)
                print(f"OP_DUP: Duplicated top stack value 0x{val:016x}")
            elif instruction == 0x08:  # OP_POP
                val = self.pop()
                print(f"OP_POP: Popped top stack value 0x{val:016x}")
            elif instruction == 0x09:  # OP_POP_STORE
                val = self.pop()
                print(f"OP_POP_STORE: Popped and stored value 0x{val:016x}")
            elif instruction == 0x0A:  # OP_ADD_IMMEDIATE
                arg = self.next_arg()
                self.stack[self.tos_ptr()] += arg
                print(f"OP_ADD_IMMEDIATE: Added 0x{arg:04x} to top stack value")
            elif instruction == 0x0B:  # OP_SUB
                val1 = self.pop()
                val2 = self.pop()
                result = val2 - val1
                self.push(result)
                print(f"OP_SUB: Subtracted 0x{val1:016x} from 0x{val2:016x}, result 0x{result:016x}")
            elif instruction == 0x0C:  # OP_DIV
                val1 = self.pop()
                val2 = self.pop()
                if val1 == 0:
                    print("OP_DIV: Division by zero error")
                    return 1
                result = val2 // val1
                self.push(result)
                print(f"OP_DIV: Divided 0x{val2:016x} by 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x0D:  # OP_MUL
                val1 = self.pop()
                val2 = self.pop()
                result = val2 * val1
                self.push(result)
                print(f"OP_MUL: Multiplied 0x{val2:016x} by 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x0E:  # OP_JUMP
                addr = self.next_arg()
                self.ip = addr
                print(f"OP_JUMP: Jumped to address 0x{addr:04x}")
            elif instruction == 0x0F:  # OP_JUMP_IF_ZERO
                addr = self.next_arg()
                if self.pop() == 0:
                    self.ip = addr
                    print(f"OP_JUMP_IF_ZERO: Jumped to address 0x{addr:04x} because top stack value was zero")
            elif instruction == 0x10:  # OP_JUMP_IF_NONZERO
                addr = self.next_arg()
                if self.pop() != 0:
                    self.ip = addr
                    print(f"OP_JUMP_IF_NONZERO: Jumped to address 0x{addr:04x} because top stack value was non-zero")
            elif instruction == 0x11:  # OP_CMP_EQ
                val1 = self.pop()
                val2 = self.pop()
                result = int(val2 == val1)
                self.push(result)
                print(f"OP_CMP_EQ: Compared 0x{val2:016x} == 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x12:  # OP_CMP_LT
                val1 = self.pop()
                val2 = self.pop()
                result = int(val2 < val1)
                self.push(result)
                print(f"OP_CMP_LT: Compared 0x{val2:016x} < 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x13:  # OP_CMP_LE
                val1 = self.pop()
                val2 = self.pop()
                result = int(val2 <= val1)
                self.push(result)
                print(f"OP_CMP_LE: Compared 0x{val2:016x} <= 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x14:  # OP_CMP_GT
                val1 = self.pop()
                val2 = self.pop()
                result = int(val2 > val1)
                self.push(result)
                print(f"OP_CMP_GT: Compared 0x{val2:016x} > 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x15:  # OP_CMP_GE
                val1 = self.pop()
                val2 = self.pop()
                result = int(val2 >= val1)
                self.push(result)
                print(f"OP_CMP_GE: Compared 0x{val2:016x} >= 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x16:  # OP_CONDITIONAL_JUMP
                addr = self.next_arg()
                if self.pop():
                    self.ip = addr
                    print(f"OP_CONDITIONAL_JUMP: Jumped to address 0x{addr:04x} based on comparison")
            elif instruction == 0x17:  # OP_STORE_LOCATION
                val = self.pop()
                print(f"OP_STORE_LOCATION: Stored value 0x{val:016x}")
            elif instruction == 0x18:  # OP_RETURN_0
                print("OP_RETURN_0: Return 0")
                return 0
            elif instruction == 0x19:  # OP_STORE_LOCATION_ALT
                val = self.pop()
                print(f"OP_STORE_LOCATION_ALT: Stored value 0x{val:016x}")
            elif instruction == 0x1A:  # OP_XOR
                val1 = self.pop()
                val2 = self.pop()
                result = val2 ^ val1
                self.push(result)
                print(f"OP_XOR: XORed 0x{val2:016x} with 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x1B:  # OP_OR
                val1 = self.pop()
                val2 = self.pop()
                result = val2 | val1
                self.push(result)
                print(f"OP_OR: ORed 0x{val2:016x} with 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x1C:  # OP_AND
                val1 = self.pop()
                val2 = self.pop()
                result = val2 & val1
                self.push(result)
                print(f"OP_AND: ANDed 0x{val2:016x} with 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x1D:  # OP_MOD
                val1 = self.pop()
                val2 = self.pop()
                result = val2 % val1
                self.push(result)
                print(f"OP_MOD: 0x{val2:016x} modulo 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x1E:  # OP_SHL
                val1 = self.pop()
                val2 = self.pop()
                result = val2 << val1
                self.push(result)
                print(f"OP_SHL: Left shifted 0x{val2:016x} by 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x1F:  # OP_SHR
                val1 = self.pop()
                val2 = self.pop()
                result = val2 >> val1
                self.push(result)
                print(f"OP_SHR: Right shifted 0x{val2:016x} by 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x20:  # OP_ROL
                val1 = self.pop()
                val2 = self.pop()
                result = (val2 << val1) | (val2 >> (32 - val1))
                self.push(result)
                print(f"OP_ROL: Rotated left 0x{val2:016x} by 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x21:  # OP_ROR
                val1 = self.pop()
                val2 = self.pop()
                result = (val2 >> val1) | (val2 << (32 - val1))
                self.push(result)
                print(f"OP_ROR: Rotated right 0x{val2:016x} by 0x{val1:016x}, result 0x{result:016x}")
            elif instruction == 0x22:  # OP_ROL_16
                val = self.pop()
                result = (val << 16) | (val >> (32 - 16))
                self.push(result)
                print(f"OP_ROL_16: Rotated left 0x{val:016x} by 16 bits, result 0x{result:016x}")
            elif instruction == 0x23:  # OP_ROR_16
                val = self.pop()
                result = (val >> 16) | (val << (32 - 16))
                self.push(result)
                print(f"OP_ROR_16: Rotated right 0x{val:016x} by 16 bits, result 0x{result:016x}")
            elif instruction == 0x24:  # OP_ROL_8
                val = self.pop()
                result = (val << 8) | (val >> (32 - 8))
                self.push(result)
                print(f"OP_ROL_8: Rotated left 0x{val:016x} by 8 bits, result 0x{result:016x}")
            elif instruction == 0x25:  # OP_ROR_8
                val = self.pop()
                result = (val >> 8) | (val << (32 - 8))
                self.push(result)
                print(f"OP_ROR_8: Rotated right 0x{val:016x} by 8 bits, result 0x{result:016x}")
            elif instruction == 0x26:  # OP_SPECIAL
                print("OP_SPECIAL: Performed special operation")
                # Perform special operation
            else:
                print(f"Unknown instruction: 0x{instruction:02x}")
                break


# Example usage


# Bytecode from the first image.
bytecode = [0x01, 0x00, 0x00, 0x01, 0xBB, 0xAA, 0x06, 0x01, 0x00, 0x01, 0x01, 0xDD, 0xCC, 0x06, 0x01, 0x00,
    0x02, 0x01, 0xFF, 0xEE, 0x06, 0x01, 0x00, 0x03, 0x01, 0xAD, 0xDE, 0x06, 0x01, 0x00, 0x04, 0x01,
    0xEF, 0xBE, 0x06, 0x01, 0x00, 0x05, 0x01, 0xFE, 0xCA, 0x06, 0x01, 0x00, 0x06, 0x01, 0xBE, 0xBA,
    0x06, 0x01, 0x00, 0x07, 0x01, 0xCD, 0xAB, 0x06, 0x01, 0x00, 0x0A, 0x01, 0x61, 0x44, 0x06, 0x01,
    0x00, 0x0B, 0x01, 0x75, 0x34, 0x06, 0x01, 0x00, 0x0C, 0x01, 0x69, 0x62, 0x06, 0x01, 0x00, 0x0D,
    0x01, 0x6C, 0x63, 0x06, 0x01, 0x00, 0x0E, 0x01, 0x31, 0x65, 0x06, 0x01, 0x00, 0x0F, 0x01, 0x66,
    0x69, 0x06, 0x01, 0x00, 0x10, 0x01, 0x62, 0x65, 0x06, 0x01, 0x00, 0x11, 0x01, 0x62, 0x30, 0x06,
    0x01, 0x00, 0x08, 0x01, 0x00, 0x03, 0x05, 0x01, 0x00, 0x30, 0x1E, 0x01, 0x00, 0x02, 0x05, 0x01,
    0x00, 0x20, 0x1E, 0x1B, 0x01, 0x00, 0x01, 0x05, 0x01, 0x00, 0x10, 0x1E, 0x1B, 0x01, 0x00, 0x00,
    0x05, 0x1B, 0x06, 0x01, 0x00, 0x09, 0x01, 0x00, 0x07, 0x05, 0x01, 0x00, 0x30, 0x1E, 0x01, 0x00,
    0x06, 0x05, 0x01, 0x00, 0x20, 0x1E, 0x1B, 0x01, 0x00, 0x05, 0x05, 0x01, 0x00, 0x10, 0x1E, 0x1B,
    0x01, 0x00, 0x04, 0x05, 0x1B, 0x06, 0x01, 0x00, 0x12, 0x01, 0x00, 0x0D, 0x05, 0x01, 0x00, 0x30,
    0x1E, 0x01, 0x00, 0x0C, 0x05, 0x01, 0x00, 0x20, 0x1E, 0x1B, 0x01, 0x00, 0x0B, 0x05, 0x01, 0x00,
    0x10, 0x1E, 0x1B, 0x01, 0x00, 0x0A, 0x05, 0x1B, 0x06, 0x01, 0x00, 0x13, 0x01, 0x00, 0x11, 0x05,
    0x01, 0x00, 0x30, 0x1E, 0x01, 0x00, 0x10, 0x05, 0x01, 0x00, 0x20, 0x1E, 0x1B, 0x01, 0x00, 0x0F,
    0x05, 0x01, 0x00, 0x10, 0x1E, 0x1B, 0x01, 0x00, 0x0E, 0x05, 0x1B, 0x06, 0x01, 0x00, 0x14, 0x01,
    0x00, 0x00, 0x06, 0x01, 0x00, 0x18, 0x01, 0x00, 0x01, 0x06, 0x01, 0x00, 0x17, 0x01, 0x00, 0x00,
    0x06, 0x01, 0x00, 0x19, 0x01, 0x00, 0x00, 0x06, 0x01, 0x00, 0x18, 0x05, 0x01, 0x00, 0x01, 0x11,
    0x10, 0x02, 0x41, 0x01, 0x00, 0x14, 0x05, 0x01, 0x00, 0x08, 0x12, 0x10, 0x01, 0x50, 0x01, 0x00,
    0x15, 0x01, 0x00, 0x08, 0x05, 0x01, 0x00, 0x08, 0x01, 0x00, 0x14, 0x05, 0x0D, 0x1F, 0x06, 0x01,
    0x00, 0x16, 0x01, 0x00, 0x12, 0x05, 0x01, 0x00, 0x08, 0x01, 0x00, 0x14, 0x05, 0x0D, 0x1F, 0x06,
    0x01, 0x00, 0x14, 0x05, 0x01, 0x00, 0x07, 0x14, 0x10, 0x01, 0x7D, 0x01, 0x00, 0x15, 0x01, 0x00,
    0x09, 0x05, 0x01, 0x00, 0x08, 0x01, 0x00, 0x14, 0x05, 0x0D, 0x1F, 0x06, 0x01, 0x00, 0x16, 0x01,
    0x00, 0x13, 0x05, 0x01, 0x00, 0x08, 0x01, 0x00, 0x14, 0x05, 0x0D, 0x1F, 0x06, 0x01, 0x00, 0x15,
    0x01, 0x00, 0x15, 0x05, 0x01, 0x00, 0xFF, 0x1C, 0x06, 0x01, 0x00, 0x16, 0x01, 0x00, 0x16, 0x05,
    0x01, 0x00, 0xFF, 0x1C, 0x06, 0x01, 0x00, 0x14, 0x05, 0x01, 0x00, 0x02, 0x11, 0x10, 0x01, 0xAC,
    0x01, 0x00, 0x16, 0x01, 0x00, 0x16, 0x05, 0x01, 0x00, 0x04, 0x24, 0x06, 0x01, 0x00, 0x14, 0x05,
    0x01, 0x00, 0x09, 0x11, 0x10, 0x01, 0xC3, 0x01, 0x00, 0x16, 0x01, 0x00, 0x16, 0x05, 0x01, 0x00,
    0x02, 0x25, 0x06, 0x01, 0x00, 0x14, 0x05, 0x01, 0x00, 0x0D, 0x11, 0x10, 0x01, 0xDA, 0x01, 0x00,
    0x16, 0x01, 0x00, 0x16, 0x05, 0x01, 0x00, 0x07, 0x24, 0x06, 0x01, 0x00, 0x14, 0x05, 0x01, 0x00,
    0x0F, 0x11, 0x10, 0x01, 0xF1, 0x01, 0x00, 0x16, 0x01, 0x00, 0x16, 0x05, 0x01, 0x00, 0x07, 0x24,
    0x06, 0x01, 0x00, 0x15, 0x05, 0x01, 0x00, 0x16, 0x05, 0x11, 0x01, 0x00, 0x00, 0x11, 0x10, 0x02,
    0x08, 0x01, 0x00, 0x18, 0x01, 0x00, 0x00, 0x06, 0x01, 0x00, 0x15, 0x05, 0x01, 0x00, 0x16, 0x05,
    0x11, 0x10, 0x02, 0x20, 0x01, 0x00, 0x17, 0x01, 0x00, 0x17, 0x05, 0x01, 0x00, 0x01, 0x09, 0x06,
    0x01, 0x00, 0x14, 0x01, 0x00, 0x14, 0x05, 0x01, 0x00, 0x01, 0x09, 0x06, 0x01, 0x00, 0x14, 0x05,
    0x01, 0x00, 0x0F, 0x14, 0x10, 0x02, 0x3E, 0x01, 0x00, 0x18, 0x01, 0x00, 0x00, 0x06, 0x0E, 0x01,
    0x18, 0x01, 0x00, 0x17, 0x05, 0x01, 0x00, 0x10, 0x11, 0x10, 0x02, 0x53, 0x01, 0x00, 0x19, 0x01,
    0x00, 0x01, 0x06, 0x01, 0x00, 0x19, 0x05, 0x19, 0x18]
vm = SimpleVM(bytecode)
vm.interpret()
