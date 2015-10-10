#!/usr/bin/env python

### IMPORT REQUIRED MODULES

import pysnmp
import snmp_helper
import time
import pygal

### SNMP INPUTS ###

snmpaddr = '50.76.53.27'                # snmp query device ip address
snmpcomm = 'galileo'                    # snmpv1/v2c community string
v3uname = 'pysnmp'                      # snmpv3 username
v3authtype = 'sha'                      # snmpv3 authentication type
v3authkey = 'galileo1'                  # snmpv3 authentication key
v3encrtype = 'aes128'                   # snmpv3 encryption type
v3encrkey = 'galileo1'                  # snmpv3 encryption key
snmpport = 8061                         # snmp port
oid1 = '1.3.6.1.2.1.2.2.1.10.5'		# Fa4 interface in octets
oid2 = '1.3.6.1.2.1.2.2.1.11.5'		# Fa4 interface in packets
oid3 = '1.3.6.1.2.1.2.2.1.16.5'		# Fa4 interface out octets
oid4 = '1.3.6.1.2.1.2.2.1.17.5'		# Fa4 interface out packets
oid5 = '1.3.6.1.2.1.2.2.1.2.5'		# Fa4 interface description

def CheckInterfaceStats(oid, value):
        global in_octets,in_packets,out_octets,out_packets
        snmp_device = (snmpaddr, snmpport)
        snmp_user = (v3uname, v3authkey, v3encrkey)
	snmp_data = snmp_helper.snmp_get_oid_v3(snmp_device, snmp_user, oid, v3authtype, v3encrtype)
	output = snmp_helper.snmp_extract(snmp_data)
	output = int(output)
	if value == '1':
		in_octets.append(output)
	if value == '2':
		in_packets.append(output)
	if value == '3':
		out_octets.append(output)
	if value == '4':
		out_packets.append(output)

def PrepNewList(newnamelist,namelist):
	for i,v in enumerate(namelist):
		if i == 0:
			newnamelist.append((v-v))
		if i > 0:
			newnamelist.append((v) - (namelist[(i - 1)]))
	print newnamelist

def BuildGraph(number):
	global new_in_octets,new_out_octets,new_in_packets,new_out_packets
	line_chart = pygal.Line()
	line_chart.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
	if number == '1':
		new_in_octets.pop(0)
		new_out_octets.pop(0)
		line_chart.title = 'Input/Output Octets'
		line_chart.add('InOctets', new_in_octets)
		line_chart.add('OutOctets', new_out_octets)
		line_chart.render_to_file('octets.svg')
	if number == '2':
		new_in_packets.pop(0)
		new_out_packets.pop(0)
		line_chart.title = 'Input/Output Packets'
		line_chart.add('InPackets', new_in_packets)
		line_chart.add('OutPackets', new_out_packets)
		line_chart.render_to_file('packets.svg')

# BUILD LIST - LIST OF VALUES GATHERED FROM DEVICES EVERY 5 MINUTES FOR 60 MINUTES

in_octets = []
in_packets = []
out_octets = []
out_packets = []
count = 0
while count < 65:
        CheckInterfaceStats(oid1, '1')
	CheckInterfaceStats(oid2, '2')
	CheckInterfaceStats(oid3, '3')
	CheckInterfaceStats(oid4, '4')
	print 'For one hour, INTERFACE STATISTICS will be updated once every 5 minutes.  Current timer: %s minutes.  Current time: %s' % (count, time.ctime().split(' ')[-2])
	print 'In Octets: %s' % in_octets
	print 'In Packets: %s' % in_packets
	print 'Out Octets: %s' % out_octets
	print 'Out Packets: %s' % out_packets
        count += 5
        time.sleep(300)

# PREP NEWLIST - ADD THE DIFFERENCE BETWEEN TWO CONSECUTIVE LIST ITEMS TO A NEW LIST

new_in_octets = []
new_in_packets = []
new_out_octets = []
new_out_packets = []
PrepNewList(new_in_octets, in_octets)
PrepNewList(new_in_packets, in_packets)
PrepNewList(new_out_octets, out_octets)
PrepNewList(new_out_packets, out_packets)

# BUILD GRAPH1 (INPUT/OUTPUT OCTETS - INT Fa4) AND GRAPH2 (INPUT/OUTPUT PACKETS - INT Fa4) - USE THE NEW LIST AS INPUT

BuildGraph('1')
BuildGraph('2')
