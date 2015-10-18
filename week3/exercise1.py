#!/usr/bin/env python

# IMPORT REQUIRED MODULES

import pysnmp
import snmp_helper
import email_helper
import pickle
import yaml
import json
import time

# SNMP INPUTS ###

snmpaddr = '50.76.53.27'		# snmp query device ip address
snmpcomm = 'galileo'			# snmpv1/v2c community string
v3uname = 'pysnmp'			# snmpv3 username
v3authtype = 'sha'			# snmpv3 authentication type
v3authkey = 'galileo1'			# snmpv3 authentication key
v3encrtype = 'aes128'			# snmpv3 encryption type
v3encrkey = 'galileo1'			# snmpv3 encryption key
snmpport = 8061				# snmp port
oid1 = '1.3.6.1.4.1.9.9.43.1.1.1.0' 	# ccmHistoryRunningLastChanged
oid2 = '1.3.6.1.4.1.9.9.43.1.1.2.0' 	# ccmHistoryRunningLastSaved
oid3 = '1.3.6.1.4.1.9.9.43.1.1.3.0' 	# ccmHistorystartupLastChanged
oid4 = '.1.3.6.1.2.1.1.5.0'		# system name

# EMAIL ALERT INPUTS ###
sender = 'week3exercise1@pynet.com'
recipient = 'freedman.dan@gmail.com'
subject = 'CONFIGURATION CHANGE ALERT'
message = '''
pynet-rtr2 configuration has changed within the last 5 minutes
'''


def CheckConfig():
	global timestamp
	snmp_device = (snmpaddr, snmpport)
	snmp_user = (v3uname, v3authkey, v3encrkey)
	snmp_data = snmp_helper.snmp_get_oid_v3(snmp_device, snmp_user, oid1, v3authtype, v3encrtype)
	output = snmp_helper.snmp_extract(snmp_data)
	if bool(timestamp) == False:
		timestamp.append(output)
		print '\nWe have begun monitoring this device for configuration changes.'
		print '%s %s' % ('The timestamp for the device is currently: ', output)
		print 'We will check the device again in 5 minutes.\n'
	elif timestamp[0] != '':
		if output == timestamp[0]:
			print 'The configuration has not changed in the last 5 minutes.'
			print '%s %s' % ('The timestamp for the device is currnetly: ', output)
			print 'We will check the device again in 5 minutes.\n'
		elif output != timestamp[0]:
			timestamp[0] = output
			print 'The configuation has changed.'
			print 'Sending email alert and checking device again in 5 minutes.\n'
			email_helper.send_mail(recipient, subject, message, sender)

timestamp = []
count = 0
while count < 60:
	CheckConfig()
    count += 5
    time.sleep(300)
