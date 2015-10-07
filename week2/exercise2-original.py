#!/usr/bin/env python

import telnetlib
import time

def main():
	connection = telnetlib.Telnet(ipadd, TELNET_PORT, TELNET_TIMEOUT)
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

	connection.write('terminal length 0' + '\n')
	time.sleep(1)
	output = connection.read_very_eager()
	print output

	connection.write('show ip int brief' + '\n')
	time.sleep(1)
	output = connection.read_very_eager()
	print output

if __name__ == '__main__':
	ipadd = '50.76.53.27'
	uname = 'pyclass'
	pword = '88newclass'
	TELNET_PORT = 23
	TELNET_TIMEOUT = 6
	main()



