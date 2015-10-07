#!/usr/bin/env python

import telnetlib
import time

ip_addr = '50.76.53.27'
username = 'pyclass'
password = '88newclass'
TELNET_PORT = 23
TELNET_TIMEOUT = 6

remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
output = remote_conn.read_until('sername:', TELNET_TIMEOUT)
print output
remote_conn.write(username + '\n')
output = remote_conn.read_until('assword:', TELNET_TIMEOUT)
print output
remote_conn.write(password + '\n')
time.sleep(1)
output = remote_conn.read_very_eager()
print output

remote_conn.write('terminal length 0\n')
time.sleep(1)
output = remote_conn.read_very_eager()
print output

remote_conn.write('show version\n')
time.sleep(1)
output = remote_conn.read_very_eager()
print output
