import os
import re
import shutil
from sys import argv

def cmd_get():
	"""docstring for cmd_get"""
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
	print("The files are listed as belows:")
	file_list = os.listdir()
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
	file_list = os.listdir()
	file_num = 0
	input("...press enter to move on")
	for file_item in file_list:
		root, ext = os.path.splitext(file_item)
		print(file_item, end = " -> ")
		if ext != ".py" and os.path.isfile(file_item) == True:
			new_name = name + str(file_num) + ext
			print(new_name)
			os.rename(file_item, new_name)
			file_num += intv
	print("There are %d files renamed." %file_num)
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

