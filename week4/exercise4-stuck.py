#!/usr/bin/env python

import pexpect
import sys

ipadd = '50.76.53.27'
uname = 'pyclass'
pword = '88newclass'
sshpt = 8022
prompt = 'pynet-rtr2#'

connection = pexpect.spawn('ssh -l {} {} -p {}'.format(uname, ipadd, sshpt))
# connection.logfile = sys.stdout
connection.timeout = 3

connection.expect('assword:')
connection.sendline(pword)
connection.expect(prompt)
print connection.before
connection.sendline('terminal length 0')
connection.expect(prompt)
print connection.before
connection.sendline('show run | in logging')
connection.expect(prompt)
print connection.before
connection.sendline('config t')
connection.expect(prompt.strip('#') + '(config)#')
# update prompt to include -config#)
print connection.before
connection.sendline('logging buffered 32768')
connection.sendline('end')
connection.expect(prompt)
print connection.before
