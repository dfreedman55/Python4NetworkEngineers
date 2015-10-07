#!/usr/bin/env python

from ciscoconfparse import CiscoConfParse

def parsefile(filename):
  return CiscoConfParse(filename)

def findlines(config,text):
  lines = config.find_objects(r"^ + text + ")

### MAINLINE ###

filename = 'CCP-cisco.txt' config = parsefile(filename) print config

text = 'interface' lines = findlines(config,text) print lines
