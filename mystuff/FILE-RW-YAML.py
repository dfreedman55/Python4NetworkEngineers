#!/usr/bin/env python

import yaml

def wyaml(data,filename):
	'''
	Write YAML File
	'''
	with open(filename, "w") as f:
		yaml.dump(data, f, default_flow_style=False)

def ryaml(filename):
	'''
	Read YAML File
	'''
	with open(filename) as f:
		mylist = yaml.load(f)
	print mylist

### MAINLINE ###

templist = [0, 1, 2, 3, 4, 5, 6, 7, 'whatever', 'hello', {'netmask': '255.255.255.0', 'ipaddr': '10.10.10.1', 'attribs': [1, 2, 3, 4]}]
wyaml(templist,"OUTPUT-YAML.yaml")
ryaml("OUTPUT-YAML.yaml")
