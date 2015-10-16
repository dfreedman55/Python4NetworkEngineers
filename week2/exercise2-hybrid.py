#!/usr/bin/env python

import telnetlib
import time

# NEXT THREE FUNCTIONS REPLACE THE COMMENTED CODE IN THE MAIN FUNCTION BELOW


def connect(ipadd, TELNET_PORT, TELNET_TIMEOUT):
	return telnetlib.Telnet(ipadd, TELNET_PORT, TELNET_TIMEOUT)


def login(connection, uname, pword):
	output = connection.read_until('sername:', TELNET_TIMEOUT)
	print output
	connection.write(uname + '\n')
	time.sleep(1)
	output = connection.read_until('assword:', TELNET_TIMEOUT)
	print output
	connection.write(pword + '\n')
	time.sleep(1)
	output = connection.read_very_eager()
	print output


def send_command(connection, cmd):
	cmd = cmd.strip() + '\n'
	connection.write(cmd)
	time.sleep(1)
	output = connection.read_very_eager()
	print output


# MAIN FUNCTION

def main():

# CONNECT VIA TELNET
	connection = connect(ipadd, TELNET_PORT, TELNET_TIMEOUT)
# connection = telnetlib.Telnet(ipadd, TELNET_PORT, TELNET_TIMEOUT)

# LOGIN (USERNAME & PASSWORD)
	login(connection, uname, pword)
# output = connection.read_until('sername:', TELNET_TIMEOUT)
# print output
# connection.write(uname + '\n')
# time.sleep(1)
# output = connection.read_until('assword:', TELNET_TIMEOUT)
# print output
# connection.write(pword + '\n')
# time.sleep(1)
# output = connection.read_very_eager()
# print output

# SEND COMMAND 'term len 0'
	send_command(connection, 'terminal length 0')
# connection.write('terminal length 0' + '\n')
# time.sleep(1)
# output = connection.read_very_eager()
# print output

# SEND COMMAND 'show ver'
	send_command(connection, 'show ip int brief')
# connection.write('show ip int brief' + '\n')
# time.sleep(1)
# output = connection.read_very_eager()
# print output

# DEFINE SCRIPT INPUTS
if __name__ == '__main__':
	ipadd = '50.76.53.27'
	uname = 'pyclass'
	pword = '88newclass'
	TELNET_PORT = 23
	TELNET_TIMEOUT = 6
	# CALL MAIN FUNCTION, MAIN FUNCTION CALLS SUPPORTING FUNCTIONS
	main()
