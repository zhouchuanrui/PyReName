# -*- coding: utf-8 -*-
import sys
import os
import pdb
import argparse

class OneToFiles(object):
    """docstring for OneToFiles"""
    def __init__(self, arg, default_dir = "exact/", key_file = "AllInOne.txt"):
        super(OneToFiles, self).__init__()
        self.arg = arg
        self.header = "zhimakaimen:"
        self.default_dir = default_dir
        self.key_file = key_file

    def cdToDefaultDir(self):
        """docstring for cdToDefaultDir"""
        if not os.path.exists(self.default_dir):
            os.mkdir(self.default_dir)
        os.chdir(self.default_dir)
        print("Create ", self.default_dir)
        pass

    def fileUnzip(self):
        """docstring for fileUnzip"""
        buf = ""
        fdr = open(self.key_file, "r")
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
    global warning_cnt

    apsr = argparse.ArgumentParser()
    apsr.add_argument("-s", "--source", help = "Indicate input source file.")
    apsr.add_argument("-o", "--outputdir", help = "Indicate output directory.")
    args = apsr.parse_args()

    if args.source:
        source_file = args.source
    else:
        source_file = "AllInOne.txt"

    if args.outputdir:
        output_dir = args.outputdir
    else:
        output_dir = "exact/"

    otf = OneToFiles(0, output_dir, source_file)
    otf.fileUnzip()
    pass

if __name__ == "__main__":
    main()

