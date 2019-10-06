
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

def lui():

def ori():

def addi(reg1, reg2, imm):
    registers[reg1] = registers[reg2] + imm

def multu():

def mfhi():

def mflo():

def xor():

def bne():

def srl():

def andi():

def sll():

def sw():

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
        'srl': srl,
        'andi': andi,
        'sll': sll,
        'sw': sw
    }
    def __init__(self, instrStr):
        self.str = instrStr
        instrParts = instrStr.split(' ', 1)
        self.f_type = instrParts[0]
        instrParts = instrParts[1].split(',')
        for i in range(0,len(instrParts)):
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




if __name__ == "__main__":
    main();