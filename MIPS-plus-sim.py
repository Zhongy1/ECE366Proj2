# ECE 366 Project 2 Fall 2019
# Group 7: Zhongy Chen, Chris Nyauchi, Claire Chappee
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
        'lo': 0,
        'hi': 0,
        'pc': 0
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
    registers[options[0]] = (int(options[2], 16 if (options[2].count('x')) else 10) << 16) & (registers[options[0]] & 0xFFFF)
    registers['pc'] += 4

def ori(options):
    registers[options[0]] = registers[options[1]] | int(options[2], 16 if (options[2].count('x')) else 10)
    registers['pc'] += 4

def addi(options):
    registers[options[0]] = (registers[options[1]] + int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers['pc'] += 4

def multu(options):
    product = registers[options[0]] * registers[options[1]]
    registers['$lo'] = product & 0xFFFFFFFF
    registers['$hi'] = (product >> 32) & 0xFFFFFFFF
    registers['pc'] += 4

def mfhi(options):
    registers[options[0]] = registers['$hi']
    registers['pc'] += 4

def mflo(options):
    registers[options[0]] = registers['$lo']
    registers['pc'] += 4

def xor(options):
    registers[options[0]]= registers[options[1]] ^ registers[options[2]]
    registers['pc'] += 4

def bne(options):
    if (registers[options[0]] == registers[options[1]]):
        registers['pc'] += 4
    else:
        registers['pc'] = labelDict[options[2]] << 2

def beq(options):
    if (registers[options[0]] == registers[options[1]]):
        registers['pc'] = labelDict[options[2]] << 2
    else:
        registers['pc'] += 4

def srl(options):
    registers[options[0]] = registers[options[1]] >> int(options[2], 16 if (options[2].count('x')) else 10)
    registers['pc'] += 4

def andi(options):
    registers[options[0]] = registers[options[1]] & int(options[2], 16 if (options[2].count('x')) else 10)
    registers['pc'] += 4

def sll(options):
    registers[options[0]] = (registers[options[1]] << int(options[2], 16 if (options[2].count('x')) else 10)) & 0xFFFFFFFF
    registers['pc'] += 4

def sw(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    memory[i] = registers[options[0]]
    registers['pc'] += 4

def lw(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    registers[options[0]] = memory[i]
    registers['pc'] += 4

def sb(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    chunk = int(i / 4)
    offset = i % 4
    toBeReplaced = memory[chunk] & (0xFF << offset * 8)
    memory[chunk] = memory[chunk] ^ toBeReplaced ^ (registers[options[0]] << offset * 8)
    registers['pc'] += 4

def lb(options):
    i = int(options[1], 16 if (options[1].count('x')) else 10) - 0x2000 + registers[options[2]]
    chunk = int(i / 4)
    offset = i % 4
    registers[options[0]] = (memory[chunk] & (0xFF << offset * 8)) >> (offset * 8)
    registers['pc'] += 4

def initializeInstrMemory(instr_mem_array, labels_dict, asm):
    index = 0;
    for line in asm:
        line = line.strip();
        if (line == ''):
            continue
        if (line.count(":")):
            labels_dict[line[0:line.index(":")]] = index
        else:
            index += 1
            instr_mem_array.append(line);

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
        'andi': andi,
        'sll': sll,
        'sw': sw,
        'lw': lw,
        'sb': sb,
        'lb': lb
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
            instrParts[i] = instrParts[i].strip();
        self.instrVals = instrParts
    
    def execute(self):
        self.func[self.f_type](self.instrVals)

    def toString(self):
        return self.str;

def main():
    f = open("output.txt","w+")
    h = open("testcase.asm","r")
    asm = h.readlines()
    initializeInstrMemory(instr_memory, labelDict, asm)
    instrCount = len(instr_memory);
    
    while (registers['pc'] >> 2 < instrCount):
        asmLine = instr_memory[registers['pc'] >> 2];
        instr = Instruction(asmLine);
        instr.execute();

    print(memory)
    print(registers['$16'])




if __name__ == "__main__":
    main();
