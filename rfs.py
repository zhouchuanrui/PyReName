import os
import re
import shutil
from sys import argv

def cmd_get():
	"""Get command"""
	print("-----")
	print(">1.List file(s)")
	print(">2.Rename file(s)")
	print(">q.Quit")
	cmd = input("Choose your next move:")
	if cmd not in ['1', '2', 'q']:
		print(">>> Wrong Command!!! Please choose a right move~")
		cmd = cmd_get()
	return cmd
	pass

def cmd_dealing(cmd):
	"""docstring for cmd_dealing"""
	if cmd == "1":
		list_flies()
	elif cmd == "2":
		rename_files()
	#pass

def list_flies():
	"""docstring for list_flies"""
	print("-----")

	print("The files are listed as belows(files only):")
	file_list = file_filter(os.listdir(), ["",".py"])
	list_num = 0
	for file_item in file_list:
		print("+%d. %s" %(list_num, file_item))
		list_num += 1
	print("There are %d files." %list_num)
	pass

def rename_files():
	"""docstring for rename_files"""
	print("-----")
	name = get_name()
	intv = get_intv()
	#file_list = os.listdir()
	#exclude .py source files and hidden file(.gitignore like) and directories
	file_list = file_filter(os.listdir(), ["",".py"])
	file_num = len(file_list)
	if file_num == 0:
		print("No files in this directory!!")
		return

	max_str_len = len(str(file_num))
	file_index = 0
	input("...press enter to move on")
	for file_item in file_list:
		root, ext = os.path.splitext(file_item)
		print(file_item, end = " -> ")
		zeros = "0"*(max_str_len - len(str(file_index)))
		new_name = name + zeros +str(file_index) + ext
		print(new_name)
		#input("..next-->") # a debug line
		os.rename(file_item, new_name)
		file_index += intv
	print("There are %d files renamed." %file_index)
	pass

def file_filter(dir_list, exclude_types):
	"""docstring for file_filter"""
	file_list = []
	for i in dir_list:
		# elcude directories and indicated types 
		root, ext = os.path.splitext(i)
		if ext not in exclude_types and os.path.isfile(i) == True:
			file_list.append(i)
	return file_list
	pass	

def get_name():
	"""docstring for get_name"""
	name = input("Input base name([tmp] if skipped): ")
	if name == '':
		name = "tmp"
	return name
	pass

def get_intv():
	intv = input("Input interval unit([1] if skipped):")
	if intv == '':
		intv = '1'
	return int(intv)

def main():
	"""docstring for main"""
	cmd = 0
	while cmd != 'q':
		cmd = cmd_get()
		cmd_dealing(cmd)
	input("Bye~")
	pass

if __name__ == "__main__":
	main()


#input("displsy script name<<")
#print(argv)
#input("-----")

#input("-----display file name:")
#print(os.path.abspath(argv[0]))

#input("-----display directory name:")
#print(os.path.basename(argv[0]))

#print(os.listdir())

#l = os.listdir()

#print("-----")
#input("list dir:")
#print("-----")

#print(l) 
	
#print("-----")
#input("list dir again:")
#print("-----")

#for i in l:
	#root, ext = os.path.splitext(i)
	#print(i)
	#print(root, ext)

#print (re.split('[!.]+',i))

#[filename, fileext] = re.split('[!.]+',i)

#print("-----")
#input("list filename and fileext of last file:")
#print("-----")

#print(filename)
#print(fileext)

## os.rename(i,'haha.txt')

#list = os.listdir()

#intv = 1
#init = 0 

#for file in list:
	#filename, fileext = re.split('[!.]+',file)
	#if fileext != 'py':
		#input("RENAMING:")
		#print("-----")
		#print(filename, fileext)
		#os.rename(file, 'yiwuoa'+str(init)+'.'+fileext)
		#init += intv
			
#print("-----")
#input("list renamed files:")
#print("-----")

#list = os.listdir()
#for file in list:
	#print(file)

