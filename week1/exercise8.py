#!/usr/bin/env python

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse('input-cisco.txt')
lines = config.find_objects(r'^crypto map CRYPTO')
for i in lines:
    print i.text
    for j in i.all_children:
        print j.text
