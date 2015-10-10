import re
import sys
import argparse


class Instruction(object):
    """docstring for Instruction"""
    def __init__(self, name, opcode, word_len, opr1_len, opr2_len):
        super(Instruction, self).__init__()
        self.name = name
        self.opcode = opcode
        self.word_len = int(word_len)
        self.opr1_len = int(opr1_len)
        self.opr2_len = int(opr2_len)
        
class Compiler(object):
    """docstring for Compiler"""
    def __init__(self, arg):
        super(Compiler, self).__init__()
        self.arg = arg
        self.instructions = {}
        self.source = []
        self.debug_flag = 1
        
    def getInstruction(self, name, opcode, word_len, opr1_len, opr2_len):
        """docstring for getInstruction"""
        if name in self.instructions.keys():
            return 1
        else:
            self.instructions[name] = Instruction(name, opcode, word_len, opr1_len, opr2_len)
            self.dprint("get instruction: %s" %name)
            return 0
        pass

    def getSource(self, s):
        """docstring for getSource"""
        self.source.append(self.removeComment(s))
        pass

    def parseSource(self):
        """docstring for parseSource"""
        sp = re.compile(r'\s*,?\s*')
        illegal_char = re.compile(r'[^a-zA-Z0-9\.,\s]')
        ln = 0
        for line in self.source:
            ln += 1
            if illegal_char.match(line):
                printError("Illegal char in line: %d\n\t%s"
                        %(ln, line))
        pass

    def removeComment(self, s):
        """docstring for removeComment"""
        return re.sub('\s*;.*$', '',s)
        pass

    def dprint(self, s):
        """docstring for dprint"""
        if (self.debug_flag):
            print(s)
        pass

def printWarning(s):
    """docstring for printWarning"""
    print("[Warning]: "+s)
    pass

def printError(s):
    """docstring for printError"""
    sys.exit("[Error]:"+s)
    pass

def main():
    """docstring for main"""
    apsr = argparse.ArgumentParser()
    apsr.add_argument("-s", "--source",
            help = "Indicate input asm source file.")
    apsr.add_argument("-i", "--ins",
            help = "Indicate instruction-defining file.")
    apsr.add_argument("-o", "--output",
            help = "Indicate output abin file.")
    args = apsr.parse_args()

    if args.ins:
        ins_file = args.ins
    else:
        ins_file = "mic8s.txt"

    if args.source:
        source_file = args.source
    else:
        source_file = "tb1505a.asm"

    if args.output:
        output_file = args.output
    else:
        output_file = "out.abin"

    cc = Compiler(1)
    fd = open(ins_file)
    line_num = 0
    for line in fd.readlines():
        line_num += 1
        items = re.split('\s+', line)
        if len(items) == 6:
            res = cc.getInstruction(items[1], items[0], items[2], items[3], items[4])
            if res:
                printWarning("Duplicate instructions in line: %d\n\t%s" %(line_num, line));

    fd.close()

    fd = open(source_file)
    for line in fd.readlines():
        cc.getSource(line)
    fd.close()

    cc.parseSource()

if __name__ == '__main__':
    main()
