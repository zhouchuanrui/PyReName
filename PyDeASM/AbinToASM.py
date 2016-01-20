#!/usr/bin/python
import os
import re
import sys
import pdb

class AbinToASM(object):
    """docstring for AbinToASM"""
    def __init__(self, val):
        super(AbinToASM, self).__init__()
        self.val = val
        self.hexline = []
        self.opc_list = """
00000000000000
00000000000001
00000000000010
00000000000011
00000000000100
00000000000
00000000001000
00000000001001
00000000001010
00000000001011
00000000001100
00000000001101
00000000001110
00000000001111
00000000010000
00000000010001
00000000010010
00000000010011
00000000010100
00000000010101
00000000010110
00000000010111
00000000011000
00000000011001
00000000011010
00000000011100
00000000011101
00000000011110
0000000010
0000001
0000010000
0000010001
0000010010
0000010011
0000011
000010d
000011d
000100
000101
000110
000111
001000
001001
001010
001011
001100
001101
001110
001111
0100
0101
0110
0111
100
110
101000
101001
101100
101101
111000
111010
111011
111100
111101
""".splitlines()

    def getHEX(self, f = "rom.hex"):
        """docstring for getHEX"""
        fd = open(f)
        lines = fd.read().splitlines()
        fd.close()
        self.hexline = []
        line_num = 0
        for l in lines:
            if l != '1'*14:
                self.hexline.append([hex(line_num), l])
            line_num += 1
            if line_num >= 1024:
                break

        #for i in self.hexline:
            #print i
        print "Get hex code from file: ", f
        pass

    def dIntp(self, d):
        """docstring for dIntp
            interpreter value d in opcode
            1 for RAM file
            0 for work register
        """
        if d == '1':
            return 'f'
        elif d == '0':
            return 'w'
        else:
            sys.exit("[EXIT]: Wrong 'd' value in opcode!!")
        pass
        
    def hexParse(self):
        """docstring for hexParse"""
        double_word_flag = False
        for i in self.hexline:
            if double_word_flag:
                double_word_flag = False
                i.append(hex(int(i[1], 2)))
            elif i[1].startswith(self.opc_list[1]):
                i.append("nop")
            elif i[1].startswith(self.opc_list[2]):
                i.append("clrw")
            elif i[1].startswith(self.opc_list[3]):
                i.append("option")
            elif i[1].startswith(self.opc_list[4]):
                i.append("sleep")
            elif i[1].startswith(self.opc_list[5]):
                i.append("clrwdt")
            elif i[1].startswith(self.opc_list[6]):
                f = str(int(i[1][11:], 2))
                i.append("tris "+f)
            elif i[1].startswith(self.opc_list[7]):
                i.append("return")
            elif i[1].startswith(self.opc_list[8]):
                i.append("retfie")
            elif i[1].startswith(self.opc_list[9]):
                i.append("daa")
            elif i[1].startswith(self.opc_list[10]):
                i.append("das")
            elif i[1].startswith(self.opc_list[11]):
                i.append("movwp")
            elif i[1].startswith(self.opc_list[12]):
                i.append("movwp++")
            elif i[1].startswith(self.opc_list[13]):
                i.append("movwp--")
            elif i[1].startswith(self.opc_list[14]):
                i.append("int")
            elif i[1].startswith(self.opc_list[15]):
                double_word_flag = True
                i.append("brsz")
            elif i[1].startswith(self.opc_list[16]):
                double_word_flag = True
                i.append("brcz")
            elif i[1].startswith(self.opc_list[17]):
                double_word_flag = True
                i.append("brsc")
            elif i[1].startswith(self.opc_list[18]):
                double_word_flag = True
                i.append("brcc")
            elif i[1].startswith(self.opc_list[19]):
                double_word_flag = True
                i.append("movlc")
            elif i[1].startswith(self.opc_list[20]):
                double_word_flag = True
                i.append("loop")
            elif i[1].startswith(self.opc_list[21]):
                double_word_flag = True
                i.append("movlt")
            elif i[1].startswith(self.opc_list[22]):
                double_word_flag = True
                i.append("movli")
            elif i[1].startswith(self.opc_list[23]):
                i.append("imov")
            elif i[1].startswith(self.opc_list[24]):
                i.append("imov++")
            elif i[1].startswith(self.opc_list[25]):
                i.append("imov--")
            elif i[1].startswith(self.opc_list[26]):
                i.append("imovf")
            elif i[1].startswith(self.opc_list[27]):
                i.append("imovf++")
            elif i[1].startswith(self.opc_list[28]):
                i.append("imovf--")
            elif i[1].startswith(self.opc_list[29]):
                q = hex(int(i[1][-4:], 2))
                i.append("movlb "+q)
            elif i[1].startswith(self.opc_list[30]):
                f = hex(int(i[1][-7:], 2))
                i.append("movwf "+f)
            elif i[1].startswith(self.opc_list[31]):
                q = hex(int(i[1][-4:], 2))
                i.append("imovw +"+q)
            elif i[1].startswith(self.opc_list[32]):
                q = hex(int(i[1][-4:], 2))
                i.append("imovw -"+q)
            elif i[1].startswith(self.opc_list[33]):
                q = hex(int(i[1][-4:], 2))
                i.append("imovf +"+q)
            elif i[1].startswith(self.opc_list[34]):
                q = hex(int(i[1][-4:], 2))
                i.append("imovf -"+q)
            elif i[1].startswith(self.opc_list[35]):
                f = hex(int(i[1][-7:], 2))
                i.append("clrf "+f)
            elif i[1].startswith(self.opc_list[36]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("subwf "+f+", "+d)
            elif i[1].startswith(self.opc_list[37]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("decf "+f+", "+d)
            elif i[1].startswith(self.opc_list[38]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("iorwf "+f+", "+d)
            elif i[1].startswith(self.opc_list[39]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("andwf "+f+", "+d)
            elif i[1].startswith(self.opc_list[40]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("xorwf "+f+", "+d)
            elif i[1].startswith(self.opc_list[41]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("addwf "+f+", "+d)
            elif i[1].startswith(self.opc_list[42]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("movf "+f+", "+d)
            elif i[1].startswith(self.opc_list[43]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("comf "+f+", "+d)
            elif i[1].startswith(self.opc_list[44]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("incf "+f+", "+d)
            elif i[1].startswith(self.opc_list[45]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("decfsz "+f+", "+d)
            elif i[1].startswith(self.opc_list[46]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("rrf "+f+", "+d)
            elif i[1].startswith(self.opc_list[47]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("rlf "+f+", "+d)
            elif i[1].startswith(self.opc_list[48]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("swapf "+f+", "+d)
            elif i[1].startswith(self.opc_list[49]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("incfsz "+f+", "+d)
            elif i[1].startswith(self.opc_list[50]):
                f = hex(int(i[1][-7:], 2))
                b = str(int(i[1][4:7], 2))
                i.append("bcf "+f+", "+b)
            elif i[1].startswith(self.opc_list[51]):
                f = hex(int(i[1][-7:], 2))
                b = str(int(i[1][4:7], 2))
                i.append("bsf "+f+", "+b)
            elif i[1].startswith(self.opc_list[52]):
                f = hex(int(i[1][-7:], 2))
                b = str(int(i[1][4:7], 2))
                i.append("btfsc "+f+", "+b)
            elif i[1].startswith(self.opc_list[53]):
                f = hex(int(i[1][-7:], 2))
                b = str(int(i[1][4:7], 2))
                i.append("btfss "+f+", "+b)
            elif i[1].startswith(self.opc_list[54]):
                k = hex(int(i[1][-11:], 2))
                i.append("goto "+k)
            elif i[1].startswith(self.opc_list[55]):
                k = hex(int(i[1][-11:], 2))
                i.append("call "+k)
            elif i[1].startswith(self.opc_list[56]):
                k = hex(int(i[1][-8:], 2))
                i.append("sublw "+k)
            elif i[1].startswith(self.opc_list[57]):
                k = hex(int(i[1][-8:], 2))
                i.append("addlw "+k)
            elif i[1].startswith(self.opc_list[58]):
                k = hex(int(i[1][-8:], 2))
                i.append("andlw "+k)
            elif i[1].startswith(self.opc_list[59]):
                k = hex(int(i[1][-8:], 2))
                i.append("xorlw "+k)
            elif i[1].startswith(self.opc_list[60]):
                k = hex(int(i[1][-8:], 2))
                i.append("iorlw "+k)
            elif i[1].startswith(self.opc_list[61]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("adcwf "+f+", "+d)
            elif i[1].startswith(self.opc_list[62]):
                f = hex(int(i[1][-7:], 2))
                d = self.dIntp(i[1][6])
                i.append("sbcwf "+f+", "+d)
            elif i[1].startswith(self.opc_list[63]):
                k = hex(int(i[1][-8:], 2))
                i.append("retlw "+k)
            elif i[1].startswith(self.opc_list[64]):
                k = hex(int(i[1][-8:], 2))
                i.append("movlw "+k)
            else:
                print "Unknown instruction at: ", i
                sys.exit("[EXIT]:ERROR PARSING!!!")
            pass

    def writeFile(self, f = "dec.asm"):
        """docstring for writeFile"""
        fd = open(f, 'w')
        for i in self.hexline:
            if len(i[0]) < 4:
                str = i[0]+'\t'*2+i[2]+'\n'
            else:
                str = i[0]+'\t'+i[2]+'\n'
            print str, 
            fd.writelines(str)
        fd.close()
        print "Result stored in file: ", f
        pass

def main():
    """docstring for main"""
    ata = AbinToASM(0)
    if len(sys.argv) == 1:
        ata.getHEX()
    elif len(sys.argv) == 2:
        file_to_parse = sys.argv[1]
        if os.path.isfile(file_to_parse):
            print "Parsing file:", file_to_parse
            ata.getHEX(file_to_parse)
        else:
            sys.exit("[ERROR]:File does not exist!!!")
    else:
        sys.exit("[ERROR]:Too many arguments!!")

    ata.hexParse()
    ata.writeFile()
    pass

if __name__ == "__main__":
    main()

# 01 00000000000000 : NOP       
# 02 00000000000001 : CLRW     
# 03 00000000000010 : OPTION   
# 04 00000000000011 : SLEEP    
# 05 00000000000100 : CLRWDT   
# 06 00000000000### : TRIS f   
# 07 00000000001000 : RETURN   
# 08 00000000001001 : RETFIE   
# 09 00000000001010 : DAA      
# 10 00000000001011 : DAS      
# 11 00000000001100 : MOVWP    
# 12 00000000001101 : MOVWP++  
# 13 00000000001110 : MOVWP--  
# 14 00000000001111 : INT      
# 15 00000000010000 : BRSZ k13 
# 16 00000000010001 : BRCZ k13 
# 17 00000000010010 : BRSC k13 
# 18 00000000010011 : BRCC k13 
# 19 00000000010100 : MOVLC k13 
# 20 00000000010101 : LOOP K13 
# 21 00000000010110 : MOVLT k13 
# 22 00000000010111 : MOVLI K13 
# 23 00000000011000 : IMOVW    
# 24 00000000011001 : IMOVW++  
# 25 00000000011010 : IMOVW--  
# 26 00000000011100 : IMOVF    
# 27 00000000011101 : IMOVF++  
# 28 00000000011110 : IMOVF--  
# 29 0000000010#### : MOVLB q  
# 30 0000001####### : MOVWF f  
# 31 0000010000#### : IMOVW +q 
# 32 0000010001#### : IMOVW -q 
# 33 0000010010#### : IMOVF +q 
# 34 0000010011#### : IMOVF -q 
# 35 0000011####### : CLRF f   
# 36 000010d####### : SUBWF f, d
# 37 000011d####### : DECF f, d 
# 38 000100######## : IORWF f, d
# 39 000101######## : ANDWF f, d
# 40 000110######## : XORWF f, d
# 41 000111######## : ADDWF f, d
# 42 001000######## : MOVF f, d 
# 43 001001######## : COMF f, d 
# 44 001010######## : INCF f, d 
# 45 001011######## : DECFSZ f, 
# 46 001100######## : RRF f, d 
# 47 001101######## : RLF f, d 
# 48 001110######## : SWAPF f, d
# 49 001111######## : INCFSZ f, 
# 50 0100########## : BCF f, b 
# 51 0101########## : BSF f, b 
# 52 0110########## : BTFSC f, b
# 53 0111########## : BTFSS f, b
# 54 100########### : GOTO k   
# 55 110########### : CALL k   
# 56 101000######## : SUBLW k  
# 57 101001######## : ADDLW k  
# 58 101100######## : ANDLW k  
# 59 101101######## : XORLW k  
# 60 111000######## : IORLW k  
# 61 111010######## : ADCWF f, d
# 62 111011######## : SBCWF f, d
# 63 111100######## : RETLW k  
# 64 111101######## : MOVLW k  


