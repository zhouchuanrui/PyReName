#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import pdb

class FilesToOne(object):
    """docstring for FilesToOne"""
    def __init__(self, arg):
        super(FilesToOne, self).__init__()
        self.arg = arg
        self.exclude_dirs = [".svn", ".git"]
        self.file_list = []
        self.root_dir_len = ""
        self.header = "zhimakaimen:"
        
    def getFileList(self, root_dir):
        """docstring for getFileList"""
        self.root_dir_len = len(root_dir)
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            for file in files:
                abs_file_name = os.path.join(root, file)
                #print "Find file: ", abs_file_name
                #print abs_file_name
                #split_filename = abs_file_name[len(root_dir):]
                #print split_filename
                self.file_list.append(abs_file_name)
        pass

    def writeToOneFile(self, output_file = "AllInOne.txt"):
        """docstring for writeToOneFile"""
        fdw = open(output_file, "w")
        content = ""
        for file in self.file_list:
            split_filename = file[self.root_dir_len:]
            fdr = open(file, "r")
            buf = fdr.read()
            fdr.close()
            try:
                buf.encode('ascii')
            except UnicodeDecodeError:
                print "Wrong encode of file: ", file, "get rid of it.."
            else:
                content += buf
                content += self.header + split_filename + '\n'
        fdw.write(content)
        fdw.close()
        print "Write all content in ", output_file
        pass

def main():
    """docstring for main"""
    fto = FilesToOne(0)
    fto.getFileList(sys.argv[1])
    fto.writeToOneFile()
    pass

if __name__ == "__main__":
    main()

