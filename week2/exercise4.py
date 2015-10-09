#!/usr/bin/env python

from snmp_helper import snmp_get_oid,snmp_extract

# pynet-rtr1 info
# 
a_device = ('50.76.53.27', 'galileo', 7961)
oid1 = '1.3.6.1.2.1.1.1.0'
snmp_data = snmp_get_oid(a_device, oid=oid1)
output = snmp_extract(snmp_data)
print output
oid1 = '1.3.6.1.2.1.1.5.0'
snmp_data = snmp_get_oid(a_device, oid=oid1)
output = snmp_extract(snmp_data)
print output

# pynet-rtr2 info
#
a_device = ('50.76.53.27', 'galileo', 8061)
oid2 = '1.3.6.1.2.1.1.1.0'
snmp_data = snmp_get_oid(a_device, oid=oid2)
output = snmp_extract(snmp_data)
print output
oid2 = '1.3.6.1.2.1.1.5.0'
snmp_data = snmp_get_oid(a_device, oid=oid2)
output = snmp_extract(snmp_data)
print output
