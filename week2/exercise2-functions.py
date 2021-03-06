#!/usr/bin/env python

import telnetlib
import time


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


def main():
	connection = connect(ipadd, TELNET_PORT, TELNET_TIMEOUT)
	login(connection, uname, pword)
	send_command(connection, 'terminal length 0')
	send_command(connection, 'show ip int brief')

if __name__ == '__main__':
	ipadd = '50.76.53.27'
	uname = 'pyclass'
	pword = '88newclass'
	TELNET_PORT = 23
	TELNET_TIMEOUT = 6
	main()
