#!/usr/bin/env python

import pickle

def wpickle(data,filename):
	'''
	Write PICKLE File
	'''
	with open(filename, "w") as f:
		pickle.dump(data, f)

def rpickle(filename):
	'''
	Read PICKLE File
	'''
	with open(filename) as f:
		mylist = pickle.load(f)
	print mylist

### MAINLINE ###

templist = [0, 1, 2, 3, 4, 5, 6, 7, 'whatever', 'hello', {'netmask': '255.255.255.0', 'ipaddr': '10.10.10.1', 'attribs': [1, 2, 3, 4]}]
wpickle(templist,"OUTPUT-PICKLE.pkl")
rpickle("OUTPUT-PICKLE.pkl")
