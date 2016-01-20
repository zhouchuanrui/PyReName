# -*- coding: utf-8 -*-
import sys
import os
import pdb

class OneToFiles(object):
    """docstring for OneToFiles"""
    def __init__(self, arg):
        super(OneToFiles, self).__init__()
        self.arg = arg
        self.header = "zhimakaimen:"
        self.default_dir = "exact/"

    def cdToDefaultDir(self):
        """docstring for cdToDefaultDir"""
        if not os.path.exists(self.default_dir):
            os.mkdir(self.default_dir)
        os.chdir(self.default_dir)
        print("Create ", self.default_dir)
        pass

    def fileUnzip(self, key_file = "AllInOne.txt"):
        """docstring for fileUnzip"""
        buf = ""
        fdr = open(key_file, "r")
        content_lines = fdr.read().splitlines()
        fdr.close()
        self.cdToDefaultDir()
        for l in content_lines:
            if l.startswith(self.header):
                #pdb.set_trace()
                filename = l[len(self.header):]
                dir, file = os.path.split(filename)
                if not os.path.exists(dir) and dir != '':
                    os.makedirs(dir)
                print("Write ..", filename)
                fdw = open(filename, "w")
                fdw.write(buf)
                fdw.close()
                buf = ""
            else:
                buf += l + '\n'
                    
        #print(content_lines)
        pass

def main():
    """docstring for main"""
    otf = OneToFiles(0)
    otf.fileUnzip()
    pass

if __name__ == "__main__":
    main()

