import re
import sys
import argparse

warning_cnt = 0

class Instruction(object):
    """docstring for Instruction"""
    def __init__(self, name, opcode, word_len, opr1_len, opr2_len):
        super(Instruction, self).__init__()
        self.name = name
        self.opcode = opcode
        self.word_len = int(word_len)
        self.opr1_len = int(opr1_len)
        self.opr2_len = int(opr2_len)
        
    def printInstruction(self):
        """docstring for printInstruction"""
        print("Instruction: %s --> %s" %(self.name, self.opcode))
        if self.opr1_len == 0 and self.opr2_len == 0 and self.word_len == 1:
            print("prototype: %s" %self.name)
        elif self.opr1_len == 0 and self.opr2_len == 0 and self.word_len == 2:
            print("prototype: %s op" %self.name)
        elif self.opr1_len != 0 and self.opr2_len == 0:
            print("prototype: %s op" %self.name)
        else:
            print("prototype: %s op1, op2" %self.name)
        pass

class Compiler(object):
    """docstring for Compiler"""
    def __init__(self, arg):
        super(Compiler, self).__init__()
        self.arg = arg
        self.instructions = {} # {opcode:Instruction object} style
        self.source = []
        self.debug_flag = 1
        self.macros = {} # {macro:(define_line_number, const_int)} type
        self.addr_labels = {} # {label:(address, define_line_number)} type
        self.rom_codes = {} # {addr:(DB|INS, ln, tokens)}
        self.compiled_abin = []
        self.addr_limit = 2**11 - 1 # 2KB
        self.word_len = 14
        
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
        illegal_char = re.compile(r'[^_a-zA-Z0-9.,+\-:$ ]')
        ln = 0
        current_addr = 0
        for line in self.source:
            ln += 1
            if illegal_char.findall(line):
                self.dprint(illegal_char.findall(line))
                printErrorAndExit("Illegal char in line: %d\n\t%s"
                        %(ln, line))
            tokens = sp.split(line)

            if len(tokens) == 1 and tokens[0] == '':
                continue

            if tokens[0].lower() == '.local':
                self.parseMacro(tokens[1:], ln)
            elif tokens[0].lower() == '.org':
                new_addr = self.parseOrg(tokens[1:], ln)
                if new_addr < current_addr:
                    printErrorAndExit("Address overlap caused by .ORG in line: %d\n\t%s"
                            %(ln, self.source[ln-1]))

                current_addr = new_addr
                pass
            elif tokens[0].lower()[-1] == ':':
                label = tokens[0].lower()[:-1]
                self.parseLabel(label, ln, current_addr)
                if len(tokens) > 1:
                    current_addr = self.parseInstruction(tokens[1:], ln, current_addr)
                pass
            else:
                current_addr = self.parseInstruction(tokens, ln, current_addr)
                pass

            if current_addr > self.addr_limit:
                printErrorAndExit("Address exceed limit line: %d\n\t%s"
                        %(ln, self.source[ln-1]))
        pass

    def compile(self):
        """docstring for compile"""
        addr = 0

        # fill abin with '111..11''
        for i in range(self.addr_limit+1):
            self.compiled_abin.append("1"*self.word_len)

        for k, v in sorted(self.rom_codes.items()):
            code_addr = k
            code_type, ln, tokens = v
            if code_type == 'DB':
                self.compiled_abin[code_addr] = self.compileDB(v)
            else:
                ins_obj = self.instructions[tokens[0]]
                if ins_obj.word_len == 2:
                    two_word = self.compileTwoWordIns(ins_obj, tokens, ln, code_addr)
                    self.compiled_abin[code_addr] = two_word[0]
                    self.compiled_abin[code_addr+1] = two_word[1]
                elif ins_obj.opr1_len == 0 and ins_obj.opr2_len ==0:
                    self.compiled_abin[code_addr] = self.compileOpc(ins_obj)
                elif ins_obj.opr1_len != 0 and ins_obj.opr2_len ==0:
                    self.compiled_abin[code_addr] = self.compileOneOpr(ins_obj, tokens, ln, code_addr)
                else:
                    self.compiled_abin[code_addr] = self.compileTwoOpr(ins_obj, tokens, ln, code_addr)
        pass

    def compileTwoOpr(self, ins_obj, tokens, ln, caddr):
        """docstring for compileTwoOpr"""
        if len(tokens) != 3:
            printErrorAndExit("Wrong oprands number in line: %d\n\t%s"
                    %(ln, self.source[ln-1]))

        opc, opr2, opr1 = tokens
        regex = re.compile(r'[^01]+')
        abin = regex.sub('', ins_obj.opcode)

        if opr1 in self.addr_labels.keys():
            data1 = self.addr_labels[opr1][0]
        elif opr1 == '$':
            data1 = caddr
        elif opr1 in self.macros.keys():
            data1 = self.macros[opr1][1]
        else:
            data1 = self.parseConst(opr1, ln) 

        if opr2 in self.addr_labels.keys():
            data2 = self.addr_labels[opr2][0]
        elif opr2 == '$':
            data2 = caddr
        elif opr2 in self.macros.keys():
            data2 = self.macros[opr2][1]
        else:
            data2 = self.parseConst(opr2, ln) 

        abin = abin + self.compileData(data1, ins_obj.opr1_len, ln) + self.compileData(data2, ins_obj.opr2_len, ln)

        if len(abin) != self.word_len:
            ins_obj.printInstruction()
            printErrorAndExit("Wrong instruction definition..")

        return abin
        pass

    def compileOneOpr(self, ins_obj, tokens, ln, caddr):
        """docstring for compileOneOpr"""
        if len(tokens) != 2:
            printErrorAndExit("Wrong oprands number in line: %d\n\t%s"
                    %(ln, self.source[ln-1]))

        opc, opr = tokens
        regex = re.compile(r'[^01]+')
        abin = regex.sub('', ins_obj.opcode)

        if opr in self.addr_labels.keys():
            data = self.addr_labels[opr][0]
        elif opr == '$':
            data = caddr
        elif opr in self.macros.keys():
            data = self.macros[opr][1]
        else:
            data = self.parseConst(opr, ln) 

        abin = abin + self.compileData(data, ins_obj.opr1_len, ln)

        if len(abin) != self.word_len:
            ins_obj.printInstruction()
            printErrorAndExit("Wrong instruction definition..")

        return abin
        pass

    def compileOpc(self, ins_obj):
        """docstring for compileOpc"""
        abin = ins_obj.opcode
        if len(abin) != self.word_len:
            ins_obj.printInstruction()
            printErrorAndExit("Wrong instruction definition..")

        return abin
        pass

    def compileTwoWordIns(self, ins_obj, tokens, ln, caddr):
        """docstring for compileTwoWordIns"""
        if len(tokens) != 2:
            printErrorAndExit("Wrong oprands number in line: %d\n\t%s"
                    %(ln, self.source[ln-1]))

        abin = []
        opc, opr = tokens
        abin.append(ins_obj.opcode)
        if len(abin[0]) != self.word_len:
            ins_obj.printInstruction()
            printErrorAndExit("Wrong instruction definition..")

        if opr in self.addr_labels.keys():
            data = self.addr_labels[opr][0]
        elif opr == '$':
            data = caddr
        elif opr in self.macros.keys():
            data = self.macros[opr][1]
        else:
            data = self.parseConst(opr, ln) 

        abin.append(self.compileData(data, self.word_len, ln))
        return abin 
        pass

    def compileDB(self, source):
        """docstring for compileDB"""
        code_type, ln, tokens = source
        abin = bin(tokens)[2:]
        if len(abin) > self.word_len:
            printWarning("DB data exceed max word length in line:%d\n\t%s" 
                    %(ln, self.source[ln-1]));
            return abin[:self.word_len]
        
        return '0'*(self.word_len-len(abin)) + abin
        pass

    def compileData(self, data_int, data_len, ln):
        """docstring for compileData"""
        abin = bin(data_int)[2:]
        if len(abin) > data_len:
            printWarning("Data exceed max word length in line:%d\n\t%s" 
                    %(ln, self.source[ln-1]));
            return abin[:data_len]
        
        return '0'*(data_len-len(abin)) + abin
        pass

    def parseInstruction(self, tokens, ln, addr):
        """docstring for parseInstruction"""
        if (tokens[0].lower() == '.db'):
            self.parseDB(tokens[1:], ln, addr)
            return addr+len(tokens[1:])
        elif tokens[0].lower() not in self.instructions.keys():
            printErrorAndExit("Unrecognized opcode <%s> in line:%d\n\t%s"
                    %(tokens[0], ln, self.source[ln-1]))
            return 0
        else:
            opc = tokens[0].lower()
            self.rom_codes[addr] = ('INC', ln, tokens)
            return addr + self.instructions[opc].word_len
        pass    

    def parseDB(self, datas, ln, addr):
        """docstring for parseDB
            return int DB data
        """
        for i in datas:
            data = self.parseConst(i, ln)
            self.rom_codes[addr] = ('DB', ln, data)
            addr += 1
        pass

    def parseLabel(self, label, ln, addr):
        """docstring for parseLabel"""
        if label == '':
            printErrorAndExit("Empty label in line: %d\n\t%s"
                    %(ln, self.source[ln-1]))

        if label in self.addr_labels.keys():
            printWarning("Duplicate label:%s in \nline[%d]:\t%s\nand line[%d]:\t%s"
                    %(label, ln, self.source[ln-1], self.addr_labels[label][1], self.source[self.addr_labels[label][1]-1]))

        self.addr_labels[label] = (addr, ln)
        pass    

    def parseOrg(self, tokens, ln):
        """docstring for parseOrg"""
        if len(tokens) != 1:
            printErrorAndExit("Wrong arguments number in .local definition in line: %d\n\t%s"
                    %(ln, self.source[ln-1]))
        
        return self.parseConst(tokens[0], ln)
        pass

    def parseMacro(self, tokens, ln):
        """docstring for parseMacros
            parse <.local macro value> type macro definition
            recursive marcro supported
            value should be digital const only
            store results in macros dict
        """
        if len(tokens) != 2:
            printErrorAndExit("Wrong arguments number in .local definition in line: %d\n\t%s"
                    %(ln, self.source[ln-1]))
        
        macro, value = tokens
        if macro in self.macros.keys():
            printWarning("Re-define MACRO:%s in \nline[%d]:\t%s\nand line[%d]:\t%s"
                    %(macro, ln, self.source[ln-1], self.macros[macro][0], self.source[self.macros[macro][0]-1]))
        
        value_int = self.parseValueInMacro(value, ln)
        self.macros[macro] = (ln, value_int)

        pass

    def parseValueInMacro(self, value, ln):
        """docstring for parseValueInMacro"""
        if value in self.macros.keys():
            return self.macros[value][1]

        return self.parseConst(value, ln)
        pass

    def parseConst(self, value, ln):
        """docstring for parseConst
            check format of input value
            and return transformed int
        """
        value = value.lower()
        illegal_char = re.compile(r'[^0-9a-fxhoq]')
        if illegal_char.findall(value):
            self.dprint(illegal_char.findall(value))
            printErrorAndExit("Illegal CONST: %s in line: %d\n\t%s"
                    %(value, ln, self.source[ln-1]))
        
        if value[0:2] == '0x':
            try:
                value_int = int(value[2:], 16)
            except ValueError:
                printErrorAndExit("Illegal 0x.. hex CONST: %s in line: %d\n\t%s"
                        %(value, ln, self.source[ln-1]))
            else:
                return value_int
        elif value[-1] == 'h':
            try:
                value_int = int(value[:-1], 16)
            except ValueError:
                printErrorAndExit("Illegal ..h hex CONST: %s in line: %d\n\t%s"
                        %(value, ln, self.source[ln-1]))
            else:
                return value_int
        elif value[-1] == 'o' or value[-1] == 'q':
            try:
                value_int = int(value[:-1], 8)
            except ValueError:
                printErrorAndExit("Illegal oct CONST: %s in line: %d\n\t%s"
                        %(value, ln, self.source[ln-1]))
            else:
                return value_int
        else:
            try:
                value_int = int(value, 10)
            except ValueError:
                printErrorAndExit("Illegal dec CONST: %s in line: %d\n\t%s"
                        %(value, ln, self.source[ln-1]))
            else:
                return value_int
        pass

    def removeComment(self, s):
        """docstring for removeComment
            remove comment starts with ';'
            and spaces locates at each beginning and end of lines
        """
        return re.sub('\s*;.*$|\s+$|^\s+', '',s)
        pass

    def dprint(self, s):
        """docstring for dprint"""
        if (self.debug_flag):
            print(s)
        pass

def printWarning(s):
    """docstring for printWarning"""
    global warning_cnt
    print("[Warning]: "+s)
    warning_cnt += 1
    pass

def printErrorAndExit(s):
    """docstring for printErrorAndExit"""
    sys.exit("[Error]:"+s)
    pass

def main():
    """docstring for main"""
    global warning_cnt

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
    cc.compile()


    print("Compile done!!\t%d warning(s)" %warning_cnt)

if __name__ == '__main__':
    main()
