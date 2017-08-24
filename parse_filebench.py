import sys
import re
import os
from shutil import copyfile

def add_run():
	(_, _, filenames) = os.walk("./myworkloads/").next()
	for file in filenames:
		fin = open("./myworkloads/" + file, 'r+')
		
		fin.seek(-50, 2)
		last = fin.readlines()[-1]
		
		if "run" not in last:
			print "filename", file
			print "last", last
			fin.seek(0, 2)
			fin.write("run 60\n")
			fin.close()
		fin.close()

def replace_run():
	(_, _, filenames) = os.walk("./myworkloads/").next()
	for file in filenames:
		fin = open("./myworkloads/" + file, 'r+')
		print "filename", file
		text = fin.read()
		text = re.sub("run 60", "run 3600", text)
		fin.seek(0)
		fin.write(text)
		fin.truncate()
		fin.close()

def make_dir_structure():
	(_, _, filenames) = os.walk("./myworkloads/").next()
	for file in filenames:
		dirName = file[0:-2]
		print dirName
		# os.mkdir("./" + dirName)
		# copyfile("./myworkloads/" + file, "./" + dirName + "/" + file)
		


make_dir_structure()