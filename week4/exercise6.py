#!/usr/bin/env python

import netmiko
import sys

pynetrtr1 = {
	'device_type': 'cisco_ios',
	'ip' = '50.76.53.27',
	'uname' = 'pyclass',
	'pword' = '88newclass',
}

pynetrtr2 = {
	'device_type': 'cisco_ios',
	'ip' = '50.76.53.27',
	'uname' = 'pyclass',
	'pword' = '88newclass',
	'port' = 8022
}

srx = {
	'device_type': 'juniper',
	'ip' = '50.76.53.27',
	'uname' = 'pyclass',
	'pword' = '88newclass',
	'port' = 9822
}

pynet-rtr1 = netmiko.ConnectHandler(**pynetrtr1)		# passes in dictionary key values into the function
pynet-rtr2 = netmiko.ConnectHandler(**pynetrtr2)		# passes in dictionary key values into the function
srx = netmiko.ConnectHandler(**srx)				# passes in dictionary key values into the function

pynet-rtr1.find_prompt()
output = pynet-rtr1.send_command('show arp')
print output

pynet-rtr2.find_prompt()
output = pynet-rtr2.send_command('show arp')
print output

srx.find_prompt()
output = srx.send_command('show arp')
print output
