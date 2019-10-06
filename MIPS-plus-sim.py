
def lui():

def ori():

def addi():

def multu():

def mfhi():

def mflo():

def xor():

def bne():

def srl():

def andi():

def sll():

def sw():

def storeLabels(dict, asm):
    index = 0;
    for line in asm:
        line = line.strip();
        if (line.count(":")):
            dict[line[0:line.index(":")]] = index
        index += 1

class Instruction:
    func = {
        'lui': lui
        'ori': ori
        'addi': addi
        'multu': multu
        'mfhi': mfhi
        'mflo': mflo
        'xor': xor
        'bne': bne
        'srl': srl
        'andi': andi
        'sll': sll
        'sw': sw
    }

def main():
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
    labelDict = {}

    f = open("output.txt","w+")
    h = open("testcase.asm","r")
    asm = h.readlines()
    storeLabels(labelDict, asm)
    # From previous homework, not to be used
    # for line in asm:
    #     instr = Instruction(line, labelDict)
    #     string = instr.toString()
    #     if string != 'InvalidInstruction':
    #         f.write(hex(int(string,2)) + '\n');
    


if __name__ == "__main__":
    main();