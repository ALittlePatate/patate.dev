from enum import IntEnum
import struct
import argparse

def parse_args() :
    parser = argparse.ArgumentParser(description="Disassembles Guardian-rs VM bytecode")

    parser.add_argument("--print-pc", "-ppc", action="store_true", default=False, 
                        help="Print the program counter (default: False)")
    parser.add_argument("--in", "-i", dest="infile", type=str, required=True, 
                        help="Input bytecode file path")
    parser.add_argument("--out", "-o", dest="outfile", type=str, required=True, 
                        help="Output file path")
                        
    args = parser.parse_args()
    return args

class Opcode(IntEnum):
    Const = 0
    Load = 1
    LoadXmm = 2
    Store = 3
    StoreXmm = 4
    StoreReg = 5
    StoreRegZx = 6
    Add = 7
    Sub = 8
    Div = 9
    IDiv = 10
    Shr = 11
    Mul = 12
    IMul = 13
    And = 14
    Or = 15
    Xor = 16
    Not = 17
    Cmp = 18
    RotR = 19
    RotL = 20
    Jmp = 21
    Vmctx = 22
    VmAdd = 23
    VmMul = 24
    VmSub = 25
    VmReloc = 26
    VmExec = 27
    VmExit = 28


class OpSize(IntEnum):
    Byte = 1
    Word = 2
    Dword = 4
    Qword = 8


class JmpCond(IntEnum):
    Jmp = 0
    Je = 1
    Jne = 2
    Jbe = 3
    Ja = 4
    Jae = 5
    Jle = 6
    Jg = 7


class Register(IntEnum):
    Rax = 0
    Rcx = 1
    Rdx = 2
    Rbx = 3
    Rsp = 4
    Rbp = 5
    Rsi = 6
    Rdi = 7
    R8 = 8
    R9 = 9
    R10 = 10
    R11 = 11
    R12 = 12
    R13 = 13
    R14 = 14
    R15 = 15

def disassemble(program, args):
    s = []
    pc = 0
    last_instr = None
    
    while pc < len(program):
        addr_str = f"0x{format(pc, 'x')}: "

        op = Opcode(program[pc])
        op_size = OpSize(program[pc + 1])

        pc += 2
        
        if args.print_pc :
            s.append(addr_str)
        s.append(op.name)
        s.append(op_size.name[0])
        
        #jmp modifies pc as well, was too lazy to implement
      
        if op == Opcode.VmExec:
            instr_size = OpSize(program[pc])
            pc += 1
            pc += instr_size
        
        if op == Opcode.Const or op == Opcode.VmReloc:
            value = 0
            if op_size == OpSize.Qword:
                value = struct.unpack_from('<Q', program, pc)[0]
                pc += OpSize.Qword
            elif op_size == OpSize.Dword:
                value = struct.unpack_from('<I', program, pc)[0]
                pc += OpSize.Dword
            elif op_size == OpSize.Word:
                value = struct.unpack_from('<H', program, pc)[0]
                pc += OpSize.Word
            elif op_size == OpSize.Byte:
                value = program[pc]
                pc += OpSize.Byte
                
            if last_instr != None and last_instr == Opcode.Vmctx :
                reg_value = (value - 16) // 8
                s.append(f" {Register(reg_value).name}")
            else :
                s.append(f" 0x{format(pc, 'x')}")
            
        if op == Opcode.VmExit:
            break
        
        s.append('\n')
        
        last_instr = op

    return ''.join(s)


args = parse_args()
with open(args.infile, 'rb') as file:
    program = bytearray(file.read())
    
print(f"processing {args.infile}...")
output = disassemble(program, args)

print(f"writing output to {args.outfile}...")
with open(args.outfile, "w") as out :
    out.write(output)

print("done.")