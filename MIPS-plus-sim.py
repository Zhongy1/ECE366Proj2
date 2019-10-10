# ECE 366 Project 2 Fall 2019
# Group 7: Zhongy Chen, Chris Nyauchi, Claire Chappee

instr_logging = True
f = 0

registers = {
        '$0': 0,
        '$8': 0,
        '$9': 0,
        '$10': 0,
        '$11': 0,
        '$12': 0,
        '$13': 0,
        '$14': 0,
        '$15': 0,
        '$16': 0,
        '$17': 0,
        '$18': 0,
        '$19': 0,
        '$20': 0,
        '$21': 0,
        '$22': 0,
        '$23': 0,
        'pc': 0,
        'hi': 0,
        'lo': 0
    }

#Each element in array represents a 4 byte chunk (32 bits)
#Starts at memory location 0x2000 and ends at 0x3000
memory = [0] * 1024

#Each entry refers to a tag name as well as the line it points to
#Example: labelDict['loop1'] might have the value 3, which means the label 'loop1' refers to line 3 in instr_memory
labelDict = {}

#Each element represenets each line in assembly code
#This excludes labels, tags, and empty lines
#doing len(instr_memory) will give you the static instruction count of the program
instr_memory = []

#'options' variable for (reg1, reg2, imm)

def lui(options):
    registers[options[0]] = (int(options[1], 16 if (options[1].count('x')) else 10) << 16) | (registers[options[0]] & 0xFFFF)
    registers[options[0]] -= pow(2, 32) if ((registers[options[0]] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def ori(options):
    registers[options[0]] = registers[options[1]] | int(options[2], 16 if (options[2].count('x')) else 10)
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def addi(options):
    registers[options[0]] = (registers[options[1]] + int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers[options[0]] -= pow(2, 32) if ((registers[options[0]] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def multu(options):
    t1 = registers[options[0]] & 0xFFFFFFFF
    t2 = registers[options[1]] & 0xFFFFFFFF
    product = t1 * t2
    registers['lo'] = product & 0xFFFFFFFF 
    registers['lo'] -= (pow(2, 32) if ((registers['lo'] >> 31) & 0x1 == 1) else 0)
    registers['hi'] = (product >> 32) & 0xFFFFFFFF
    registers['hi'] -= (pow(2, 32) if ((registers['hi'] >> 31) & 0x1 == 1) else 0)
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tMultiply ' + str(registers[options[0]]) + ' and ' + str(registers[options[1]]) + '\n')
        f.write('\tStore lower half (' + str(registers['lo']) + ') to register lo\n')
        f.write('\tStore upper half (' + str(registers['hi']) + ') to register hi\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def mfhi(options):
    registers[options[0]] = registers['hi']
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tMove ' + str(registers['hi']) + ' to ' + options[0] + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def mflo(options):
    registers[options[0]] = registers['lo']
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tMove ' + str(registers['lo']) + ' to ' + options[0] + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def xor(options):
    registers[options[0]] = (registers[options[1]] ^ registers[options[2]]) & 0xFFFFFFFF
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def bne(options):
    if (registers[options[0]] == registers[options[1]]):
        registers['pc'] += 4
        if (instr_logging):
            f.write('\t' + str(registers[options[0]]) + ' is equal to ' + str(registers[options[1]]) + '\n')
            f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')
    else:
        if (instr_logging):
            f.write('\t' + str(registers[options[0]]) + ' is not equal to ' + str(registers[options[1]]) + '\n')
            f.write('\tPC: ' + str(registers['pc']) + ' --> ' + str(labelDict[options[2]] << 2) + '\n')
        registers['pc'] = labelDict[options[2]] << 2

def beq(options):
    if (registers[options[0]] == registers[options[1]]):
        if (instr_logging):
            f.write('\t' + str(registers[options[0]]) + ' is equal to ' + str(registers[options[1]]) + '\n')
            f.write('\tPC: ' + str(registers['pc']) + ' --> ' + str(labelDict[options[2]] << 2) + '\n')
        registers['pc'] = labelDict[options[2]] << 2
    else:
        registers['pc'] += 4
        if (instr_logging):
            f.write('\t' + str(registers[options[0]]) + ' is not equal to ' + str(registers[options[1]]) + '\n')
            f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def srl(options):
    registers[options[0]] = registers[options[1]] >> int(options[2], 16 if (options[2].count('x')) else 10)
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def srlv(options):
    registers[options[0]] = registers[options[1]] >> registers[options[2]]
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def andi(options):
    registers[options[0]] = registers[options[1]] & int(options[2], 16 if (options[2].count('x')) else 10)
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def sll(options):
    registers[options[0]] = (registers[options[1]] << int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tChange ' + options[0] + ' to ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def sw(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    chunk = int(i / 4)
    memory[chunk] = registers[options[0]]
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tMove ' + str(registers[options[0]]) + ' to memory location ' + options[1] + ' + ' + str(registers[options[2]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def lw(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    chunk = int(i / 4)
    registers[options[0]] = memory[chunk]
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tMove ' + str(registers[options[0]]) + ' to ' + options[0] + ' from memory location ' + options[1] + ' + ' + str(registers[options[2]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def sb(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    chunk = int(i / 4)
    offset = i % 4
    toBeReplaced = memory[chunk] & (0xFF << offset * 8)
    memory[chunk] = memory[chunk] ^ toBeReplaced ^ ((registers[options[0]] & 0xFF) << offset * 8)
    memory[chunk] -= pow(2, 32) if ((memory[chunk] >> 31) & 0x1 == 1) else 0
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tMove ' + str(registers[options[0]] & 0xFF) + ' to memory location ' + options[1] + ' + ' + str(registers[options[2]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def lb(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    chunk = int(i / 4)
    offset = i % 4
    registers[options[0]] = (memory[chunk] & (0xFF << offset * 8)) >> (offset * 8)
    registers[options[0]] = (0xFFFFFF00 if (registers[options[0]] & 0x80 == 0x80) else 0x0) | registers[options[0]]
    registers['pc'] += 4
    if (instr_logging):
        f.write('\tMove ' + str(registers[options[0]]) + ' to ' + options[0] + ' from memory location ' + options[1] + ' + ' + str(registers[options[2]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')

def hash(options):
    a = registers[options[1]] & 0xFFFFFFFF
    b = registers[options[2]] & 0xFFFFFFFF
    for i in range(0, 5):
        product = a * b
        hi = product & 0xFFFFFFFF
        lo = (product >> 32) & 0xFFFFFFFF
        a = hi ^ lo
    c = (a & 0xFFFF) ^ ((a >> 16) & 0xFFFF)
    registers[options[0]] = (c & 0xFF) ^ ((c >> 8) & 0xFF)
    registers['pc'] += 4
    if (instr_logging):
        f.write('*** Special Instruction ***\n')
        f.write('\t' + options[0] + ' = H(' + options[1] + ', ' + options[2] + ')\n')
        f.write('\t' + options[0] + ' = ' + str(registers[options[0]]) + '\n')
        f.write('\tPC: ' + str(registers['pc'] - 4) + ' --> ' + str(registers['pc']) + '\n')
        
    

def initializeInstrMemory(instr_mem_array, labels_dict, asm):
    index = 0
    for line in asm:
        line = line.strip()
        if (line == ''):
            continue
        if (line.count(":")):
            labels_dict[line[0:line.index(":")]] = index
        else:
            index += 1
            instr_mem_array.append(line)

class Instruction:
    func = {
        'lui': lui,
        'ori': ori,
        'addi': addi,
        'multu': multu,
        'mfhi': mfhi,
        'mflo': mflo,
        'xor': xor,
        'bne': bne,
        'beq': beq,
        'srl': srl,
        'srlv': srlv,
        'andi': andi,
        'sll': sll,
        'sw': sw,
        'lw': lw,
        'sb': sb,
        'lb': lb,
        'hash': hash
    }
    def __init__(self, instrStr):
        self.str = instrStr
        instrParts = instrStr.split(' ', 1)
        self.f_type = instrParts[0]
        instrParts = instrParts[1].split(',')
        for i in range(0,len(instrParts)):
            if (instrParts[i].count('(')):
                spec = instrParts[i]
                instrParts.pop()
                instrParts.append(spec[0:spec.index('(')].strip())
                instrParts.append(spec[spec.index('(')+1:spec.index(')')].strip())
                break
            instrParts[i] = instrParts[i].strip()
        self.instrVals = instrParts
    
    def execute(self):
        self.func[self.f_type](self.instrVals)

    def toString(self):
        return self.str

def main():
    global f
    global registers
    global memory
    global labelDict
    global instr_memory

    f1 = open("output-test.txt","w+")
    h1 = open("testcase.asm","r")
    f2 = open("output-default.txt","w+")
    h2 = open("Hash-MIPS-default.asm","r")
    f3 = open("output-plus.txt","w+")
    h3 = open("Hash-MIPS-plus.asm","r")

    if (instr_logging == True):
        f = f1
    asm = h1.readlines() 
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2]
        instr = Instruction(asmLine)
        if (instr_logging == True):
            f1.write('Instruction: ' + instr.toString() + '\n')
        instr.execute()
        dynamInstrCount += 1
    #Testcase Output
    f1.write('ECE 366 Project 2\n')
    f1.write('Created by: Zhongy Chen, Chris Nyauchi, and Claire Chappee\n')
    f1.write('Output for testcase.asm\n')
    f1.write('****************************************************\n')
    for key in registers:
        f1.write(key + ' --> ' + str(registers[key]) + '\n')
    f1.write('****************************************************\n')
    f1.write('The memory contents of 0x2000 - 0x225C are:\n')
    memOutputSize = 12
    for i in range(0, 152):
        if (i != 0 and i % 8 == 0):
            f1.write('\n')
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f1.write(' ')
        f1.write(str(memory[i]) + ' ')
    f1.write('\n****************************************************\n')
    f1.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 1024
    labels_dict = {}
    instr_memory = []


    if (instr_logging == True):
            f = f2
    asm = h2.readlines() 
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2]
        instr = Instruction(asmLine)
        if (instr_logging == True):
            f2.write('Instruction: ' + instr.toString() + '\n')
        instr.execute()
        dynamInstrCount += 1
    #Default Output
    f2.write('ECE 366 Project 2\n')
    f2.write('Created by: Zhongy Chen, Chris Nyauchi, and Claire Chappee\n')
    f2.write('Output for Hash-MIPS-default.asm\n')
    f2.write('****************************************************\n')
    for key in registers:
        f2.write(key + ' --> ' + str(registers[key]) + '\n')
    f2.write('****************************************************\n')
    f2.write('The memory contents of 0x2000 - 0x225C are:\n')
    memOutputSize = 4
    for i in range(0, 152):
        if (i != 0 and i % 8 == 0):
            f2.write('\n')
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f2.write(' ')
        f2.write(str(memory[i]) + ' ')
    f2.write('\n****************************************************\n')
    f2.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))
    #clear memory
    for key in registers:
        registers[key] = 0
    memory = [0] * 1024
    labels_dict = {}
    instr_memory = []
    

    if (instr_logging == True):
        f = f3
    asm = h3.readlines() 
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory)
    dynamInstrCount = 0
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2]
        instr = Instruction(asmLine)
        if (instr_logging == True):
            f3.write('Instruction: ' + instr.toString() + '\n')
        instr.execute()
        dynamInstrCount += 1
    #Plus Default
    f3.write('ECE 366 Project 2\n')
    f3.write('Created by: Zhongy Chen, Chris Nyauchi, and Claire Chappee\n')
    f3.write('Output for Hash-MIPS-plus.asm\n')
    f3.write('****************************************************\n')
    for key in registers:
        f3.write(key + ' --> ' + str(registers[key]) + '\n')
    f3.write('****************************************************\n')
    f3.write('The memory contents of 0x2000 - 0x225C are:\n')
    memOutputSize = 4
    for i in range(0, 152):
        if (i != 0 and i % 8 == 0):
            f3.write('\n')
        for j in range(0, memOutputSize - len(str(memory[i]))):
            f3.write(' ')
        f3.write(str(memory[i]) + ' ')
    f3.write('\n****************************************************\n')
    f3.write('Dynamic Instruction Count --> ' + str(dynamInstrCount))


if __name__ == "__main__":
    main()
