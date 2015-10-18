#!/usr/bin/env python

import telnetlib
import time
import socket
import sys


class DefineNetworkDevice(object):
	def __init__(self, ip, uname, pword):
		'''
		Object initialization
		'''
		self.ip = ip
		self.uname = uname
		self.pword = pword
		self.TELNET_PORT = 23
		self.TELNET_TIMEOUT = 6

	def TelnetConnect(self):
		'''
		Connect, Receive Username Prompt, Send Username, Receive Password Prompt, Send Password, Receive Router Prompt
		'''
		self.connection = telnetlib.Telnet(self.ip, self.TELNET_PORT, self.TELNET_TIMEOUT)
		# output = self.connection.read_until('sername:', TELNET_TIMEOUT)
		# print output
		self.connection.write(self.uname + '\n')
		time.sleep(1)
		# output = self.connection.read_until('assword:', TELNET_TIMEOUT)
		# print output
		self.connection.write(self.pword + '\n')
		time.sleep(1)
		# output = self.connection.read_very_eager()
		# print output

	def TelnetSendCommand(self, command):
		'''
		Send command to established telnet session
		'''
		self.connection.write(command + '\n')
		time.sleep(1)

	def TelnetReceiveData(self):
		'''
		Receive command output from establish telnet session
		'''
		output = self.connection.read_very_eager()
		print output

# if __name__ == '__main__':

rtr1 = DefineNetworkDevice('50.76.53.27', 'pyclass', '88newclass')
rtr1.TelnetConnect()
rtr1.TelnetSendCommand('terminal length 0')
rtr1.TelnetReceiveData()
rtr1.TelnetSendCommand('show version')
rtr1.TelnetReceiveData()
