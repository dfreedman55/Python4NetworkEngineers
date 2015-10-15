#!/usr/bin/env python

from netmiko import ConnectHandler
import sys

pynetrtr1 = {
	'device_type': 'cisco_ios',
	'ip': '50.76.53.27',
	'username': 'pyclass',
	'password': '88newclass',
}

pynetrtr2 = {
	'device_type': 'cisco_ios',
	'ip': '50.76.53.27',
	'username': 'pyclass',
	'password': '88newclass',
	'port': 8022
}

srx = {
	'device_type': 'juniper',
	'ip': '50.76.53.27',
	'username': 'pyclass',
	'password': '88newclass',
	'port': 9822
}

rtr2 = ConnectHandler(**pynetrtr2)		# passes in dictionary key values into the function

output = rtr2.find_prompt()
print output

output = rtr2.config_mode()
print output

output = rtr2.check_config_mode()
print output
