#!/usr/bin/env python

from netmiko import ConnectHandler

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

rtr1 = ConnectHandler(**pynetrtr1)
# passes in dictionary key values into the function
rtr2 = ConnectHandler(**pynetrtr2)
# passes in dictionary key values into the function
srx = ConnectHandler(**srx)
# passes in dictionary key values into the function

output = rtr1.find_prompt()
print output

output = rtr1.send_command('show arp')
print output

output = rtr2.find_prompt()
print output

output = rtr2.send_command('show arp')
print output

output = srx.find_prompt()
print output

output = srx.send_command('show arp')
print output
