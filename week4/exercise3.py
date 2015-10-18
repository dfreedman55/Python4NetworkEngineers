#!/usr/bin/env python

import pexpect
import sys
import time

ipadd = '50.76.53.27'
uname = 'pyclass'
pword = '88newclass'
port = 8022

connection = pexpect.spawn('ssh -l {} {} -p {}'.format(uname, ipadd, port))
#connection.logfile = sys.stdout
connection.timeout = 3

connection.expect('assword:')
connection.sendline(pword)
connection.expect('pynet-rtr2#')
print connection.after

connection.sendline('terminal length 0')
connection.expect('pynet-rtr2#')
connection.sendline('show ip int brief')
connection.expect('pynet-rtr2#')
print connection.before
print connection.after

connection.sendline('show version')
connection.expect('pynet-rtr2#')
print connection.before
print connection.after


