#!/usr/bin/env python

import pexpect
import sys

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

connection.sendline('show run | in logg')
connection.expect('pynet-rtr2#')
print connection.before
print connection.after

connection.sendline('conf t')
connection.expect('#')
#connection.expect('pynet-rtr2(config)#')
#connection.expect('Enter configuration commands, one per line.  End with CNTL/Z.\r\npynet-rtr2(config)#')
print connection.before
print connection.after

connection.sendline('logging buffered 32768')
connection.expect('#')
#connection.expect('pynet-rtr2(config)#')
print connection.before
print connection.after

connection.sendline('end')
connection.expect('pynet-rtr2#')
print connection.before
print connection.after

connection.sendline('show run | in logg')
connection.expect('pynet-rtr2#')
print connection.before
print connection.after

