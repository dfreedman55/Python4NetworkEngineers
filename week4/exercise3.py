#!/usr/bin/env python

import pexpect
import sys

ipadd = '50.76.53.27'
uname = 'pyclass'
pword = '88newclass'
sshpt = 8022
prompt = 'pynet-rtr2#'

connection = pexpect.spawn('ssh -l {} {} -p {}'.format(uname, ipadd, sshpt))
#connection.logfile = sys.stdout
connection.timeout = 3

connection.expect('assword:')
connection.sendline(pword)
connection.expect(prompt)
connection.sendline('terminal length 0')
connection.expect(prompt)
connection.sendline('show ip int brief')	# .sendline automatically adds a new line
connection.expect(prompt)
print connection.before				# prints what was found before the previous expect command and the prior one (output of 'show ip int brief')
print connection.after				# prints what you matched on in the previous expect command (pynet-rtr2#)
