#!/usr/bin/env python

def wfile(data,filename):
	'''
	Write File
	'''
	with open(filename, "w") as f:
		f.write(data)

def rfile(filename):
	'''
	Read File
	'''
	with open(filename) as f:
		mylist = f.read()
	print mylist.strip()

### MAINLINE ###

#templist = [0, 1, 2, 3, 4, 5, 6, 7, 'whatever', 'hello', {'netmask': '255.255.255.0', 'ipaddr': '10.10.10.1', 'attribs': [1, 2, 3, 4]}] 
templist = 'here is a line to write out to file\n'
wfile(templist,"OUTPUT-TEXT.txt")
rfile("OUTPUT-TEXT.txt")
