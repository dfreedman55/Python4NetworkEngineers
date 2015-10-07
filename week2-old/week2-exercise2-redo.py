#!/usr/bin/env python

import telnetlib
import time
import socket

### VARIABLES ###

ip_addr = '50.76.53.27' 
username = 'pyclass' 
password = '88newclass' 
TELNET_PORT = 23 
TELNET_TIMEOUT = 6

### FUNCTIONS ###

def telnet_connect(ip_addr, TELNET_PORT, TELNET_TIMEOUT):
	try:
		return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
	except socket.timeout:
		print 'Connection timed-out'

def telnet_login(remote_conn, username, password):
	output = remote_conn.read_until('sername:', TELNET_TIMEOUT)
	print output
	remote_conn.write(username + '\n')
	output = remote_conn.read_until('assword:', TELNET_TIMEOUT)
	print output
	remote_conn.write(password + '\n')
	time.sleep(1)
	output = remote_conn.read_very_eager()
	print output

def send_command(remote_conn, cmd):
	remote_conn.write(cmd + '\n')
	time.sleep(1)
	output = remote_conn.read_very_eager()
	print output

### MAINLINE ###

remote_conn = telnet_connect(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
telnet_login(remote_conn, username, password)
send_command(remote_conn, 'terminal length 0')
send_command(remote_conn, 'show version')
remote_conn.close()
