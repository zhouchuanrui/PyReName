#!/usr/bin/python
import os
import re
import sys
import pdb

class VerilogParser(object):
    """a Verilog module Parser
        it parses the verilog module recursively by listing where the module locates from top module """
    def __init__(self, arg):
        super(VerilogParser, self).__init__()
        self.arg = arg
        self.list = [] #source file list
        self.dict = {} #module,file dict
        self.dl = [] #dependence file list
        self.uml = [] #undefined module list
        self.exclude_tokens = ["initial", "input", "output", "define", "begin", "endif"]

    def getSourceList(self, path_str):
        self.list = []
        exclude_dirs = [".svn", "dc"] #escape .svn/ and dc/
        for root, dirs, files in os.walk(path_str):
            #pdb.set_trace()
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith('.v') or file.endswith('.sv') or file.endswith('.svh'):
                    print "Find source file: ", file
                    self.list.append(os.path.join(root, file))
        #return self.list

    def escapeComment(self, src_str):
        """docstring for escapeComment
            this function remove // and /**/ comment of the source string
            and keep // and /**/ content inside '' and "" quotes
        """
        pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//.*?\n)"
        regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
        def _replacer(match):
            if match.group(2) is not None:
                return ""
            else:
                return match.group(1)
        return regex.sub(_replacer, src_str)
        pass

    def escapeCommentAndQuote(self, src_str):
        pattern = r"\".*?\"|/\*.*?\*/|//.*?\n"
        regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
        return regex.sub("", src_str)

    def escapeCompileDirective(self, src_str):
        """remove one-line compile directives
            `define
            `include
            `timescale
            `ifdef
            `else
            `endif
        """
        pattern = r"`(define|include|timescale|ifdef|else|endif).*?\n"
        regex = re.compile(pattern, re.DOTALL)
        return regex.sub("", src_str)

    def substringRemove(self, src_str, begin_index, end_index):
        """docstring for substringRemove
            remove a given substring with begin index and end index 
            of source string
            using string slice 
        """
        #print "begin: %d, end: %d, len: %d" %(begin_index, end_index, len(src_str))
        #print type(begin_index)
        #print type(end_index)
        #print type(len(src_str))
        if (begin_index <= 0) or (begin_index > end_index) or (end_index >= len(src_str)):
            sys.exit("[ERROR]:String Index Error in substringRemove")
        else:
            return src_str[:begin_index]+src_str[end_index:]
        pass

    def escapeBeginEnd(self, src_str):
        """docstring for escapeBeginEnd"""
        pattern  = r"\bbegin\b|\bend\b"
        regex = re.compile(pattern)
        begin_end = regex.finditer(src_str)
        match_stack = 0
        pos_list = []
        begin_pos = 0
        end_pos = 0
        for iter in begin_end:
            #print "[%s] in %s" %(iter.group(), iter.span())
            # match begin-end pair station
            if iter.group() == "begin":
                match_stack += 1
                if match_stack == 1:
                    begin_pos = iter.span()[0]
                    #print "Starting a match at ", begin_pos
            elif iter.group() == "end":
                match_stack -= 1
                if match_stack == 0:
                    end_pos = iter.span()[1]
                    #print "Closing a match at ", end_pos
                    pos_list.append((begin_pos, end_pos))
                elif match_stack < 0:
                    sys.exit("[ERROR]:Error end in escapeBeginEnd()")
            else:
                sys.exit("[ERROR]:Error Match in escapeBeginEnd()")
        # reverse position list to do backward substring removal
        # to keep next position right after a removal
        pos_list = pos_list[::-1] 
        for pp in pos_list:
            #print "="*5, pp
            #print src_str[pp[0]:pp[1]]
            src_str = self.substringRemove(src_str, pp[0], pp[1])
        return src_str
        pass
        
    def getModuleDict(self):
        """docstring for getModuleDict
            get modules from source filelist captured 
            by getSourceList
        """
        self.dict = dict()
        if len(self.list) == 0:
            print "No verilog source file!!"
            return
        for f in self.list:
            fd = open(f, 'r')
            src = fd.read()
            fd.close()
            src = self.escapeComment(src)
            regex = re.compile('module\s+\w+')
            if len(regex.findall(src)) == 0:
                print "no module in ", f
                continue
            for mod in regex.findall(src):
                mod = re.sub(r"^module\s+", "", mod)
                print "get module [%s] in %s" %(mod, f)
                self.dict[mod] = f
        return self.dict
        pass

    def getDependenceList(self, file):
        inst_cnt = 0
        catched_insts = [] # locallist to hold non-duplicate insts
        visited_files = [] #

        visited_files.append(file) # in case for infinite recursion
        if file not in self.dl:
            self.dl.append(file)

        fd = open(file, 'r')
        #fd = open('../../rtl/ip/PAD.v', 'r')
        src = fd.read()
        fd.close()
        print "traverse in file:", file
        #print re.findall(r"//.*?\n",src)
        #print re.findall(r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//.*?\n)",src)
        # escapeComment cannot remove // input // output
        # donnot know why
        #src = re.sub(r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//.*?\n)","",src, re.DOTALL)
        #src = re.sub(r"/\*.*?\*/","",src, re.DOTALL)
        src = self.escapeCommentAndQuote(src)
        src = self.escapeCompileDirective(src)
        src = self.escapeBeginEnd(src)
        #if file == "../../rtl/ip/EO001K14PA180SC02.v":
            #src = self.escapeBeginEnd(src)
            #print src

        pat = '\w+\s+\w+\s*\(.*?\)\s*;'
        regex = re.compile(pat , re.DOTALL)
        catch_list = regex.findall(src)
        #if file == "../../rtl/ip/EO001K14PA180SC02.v":
            #for i in catch_list:
                #print "+" * 30
                #print i
        if len(catch_list) == 0:
            print "no module inst in ", file
            return
        for catch_inst in catch_list:
            token = re.split('\s+',catch_inst)[0]
            if token == "module": #"module" in catch_inst
                top_mod = re.split('\s+',catch_inst)[1]
                print "get top module:", top_mod
            elif token in self.exclude_tokens: # deal with initial input output token
                print "Catch wrong token: ", token
            elif token in self.dict:
                if token not in catched_insts: 
                    catched_insts.append(token)
                    inst_cnt += 1
                    print "get a inst of %s in %s" %(token, top_mod)
                    if self.dict[token] not in visited_files:
                        visited_files.append(self.dict[token])
                        self.getDependenceList(self.dict[token]) #recursive routine
                    else:
                        print "Already visited file %s, quit this turn" %self.dict[token]
                else:
                    print "get another inst of %s, already in list" %token
            else:
                if token not in self.uml:
                    self.uml.append(token)
                    print "Cannot find module %s declaration in any source file!!!" %token
                #mod = re.split('\s+',catch_inst)[0]
                #if mod in self.dict and mod not in catched_insts:
                    #catched_insts.append(mod)
                    #inst_cnt = inst_cnt + 1
                    #print "get a inst of %s in %s" %(mod, top_mod)
                    #self.getDependenceList(self.dict[mod])
                #else:
                    #print "Cannot find module %s declaration in any source file!!!" %mod
        print "get %d insts in file %s" %(inst_cnt, file)
        #for i in catched_insts:
            #print i, "; ",

    def parse(self, file, dir_uplevel = 2):
        """docstring for parse"""
        self.list = [] #source file list
        self.dict = {} #module,file dict
        self.dl = [] #dependence file list
        self.uml = [] #undefined module list
        
        dir = ""
        if dir_uplevel < 0:
            sys.exit("[ERROR]:Wrong Directory Level include")
        elif dir_uplevel == 0:
            dir = "."
        elif dir_uplevel == 1:
            dir = "../"
        else:
            dir = ".." + "/.." * (dir_uplevel - 1)

        self.getSourceList(dir)
        self.getModuleDict()
        #pdb.set_trace()
        self.getDependenceList(file)
        
        fd = open("dependency.list", "w")
        for i in self.dl:
            fd.write(i + '\n')
        fd.close()
        pass


def main():
    """docstring for main"""
    vp = VerilogParser(0)

    sys.setrecursionlimit(10000)

    if len(sys.argv) == 1:
        print """
Script usage: ./VerilogParser.py file_name [up_level = 2]
file_name: a filename string to assign top verilog file to parse
up_level: a digit number to indicate root directory from current working directory  
          0 -> .
          1 -> ..
          2 -> ../..
          3 -> ../../..
          it is an optional argument with a default value of 2 """
        sys.exit("[ERROR]:Please provide at least 1 argument!!!")
    elif len(sys.argv) == 2:
        file_to_parse = sys.argv[1]
        if os.path.isfile(file_to_parse):
            print "Parsing file:", file_to_parse
            dir_uplevel = 2
        else:
            sys.exit("[ERROR]:File does not exist!!!")
    elif len(sys.argv) == 3:
        file_to_parse, dir_uplevel = sys.argv[1], sys.argv[2]
        if os.path.isfile(file_to_parse):
            print "Parsing file:", file_to_parse
        else:
            sys.exit("[ERROR]:File does not exist!!!")
        if dir_uplevel.isdigit():
            dir_uplevel = int(dir_uplevel)
        else:
            sys.exit("[ERROR]:Wrong directory level indicator!!!")
    else:
        sys.exit("[ERROR]:Too many arguments!!")

    print os.getcwd()
    vp.parse(file_to_parse, dir_uplevel)

    return
    path = "../.."
    #os.chdir('../..')
    vp.getModuleDict()
    ls = vp.getSourceList(path)
    vp.getModuleDict()

    vp.getDependenceList('../../rtl/top/pdn1505a_chip.v')
    
    #for i in ls:
        #print "the file:", i 
    #os.chdir('../..')
    #print os.getcwd()

    fd = open('../../rtl/top/pdn1505a_chip.v', 'r')
    #regex = re.compile('\w+\s+\n*\w+\s*\n*\s*\(')
    #regex = re.compile('\w+\s+\n*\w+(\s*\n?)*\(')
    regex = re.compile('\w+\s+\w+\s*\(')
    for item in regex.findall(fd.read()):
        print item + '---END of MATCH'
    fd.close()

    pass

    #tri = os.walk('../../')
    #for root, dirs, files in tri:
        #print "-----Strip Line---"
        #print root, dirs, files, ";"

if __name__ == "__main__":
    main()

