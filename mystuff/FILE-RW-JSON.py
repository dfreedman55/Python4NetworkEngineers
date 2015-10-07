#!/usr/bin/env python

import json

def wjson(data, filename):
	'''
	Write JSON File
	'''
	with open(filename, 'w') as f:
		json.dump(data, f)

def rjson(filename):
	'''
	Read JSON File
	'''
	with open(filename, 'r') as f:
		mylist = json.load(f)
	print mylist

### MAINLINE ###

templist = [0, 1, 2, 3, 4, 5, 6, 7, 'whatever', 'hello', {'netmask': '255.255.255.0', 'ipaddr': '10.10.10.1', 'attribs': [1, 2, 3, 4]}]
wjson(templist,"OUTPUT-JSON.json")
rjson("OUTPUT-JSON.json")
