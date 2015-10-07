#!/usr/bin/env python

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse('input-cisco.txt')
lines = config.find_objects_wo_child(parentspec=r'^crypto map CRYPTO', childspec=r'set transform-set AES-SHA')
for i in lines:
 print i.parent.text
 print i.children[1].text.split(' ')[3]


# BELOW IS ANOTHER WAY TO ACCOMPLISH THE SAME THING
# NOT AS ELEGANT (MORE LINES OF CODE)
# AND IT DOESN'T LEVERAGE FEATURES OF CISCOCONFPARSE 
# BUT IT REPLACES THE LAST LINE IN THE PROGRAM ABOVE
# AND USES STANDARD STRING PROCESSING METHODS
# AND IT YIELDS THE SAME RESULT
# 
# for j in i.all_children:
#  if 'transform' in j.text:
#   line = j.text
#   print line.strip().split(' ')[-1]
