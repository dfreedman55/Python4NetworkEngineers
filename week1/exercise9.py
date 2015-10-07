#!/usr/bin/env python

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse('input-cisco.txt')
lines = config.find_objects_w_child(parentspec=r'^crypto map CRYPTO', childspec=r'set pfs group2')
for i in lines:
 print i.parent.text
