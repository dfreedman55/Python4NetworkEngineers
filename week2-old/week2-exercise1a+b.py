#!/usr/bin/env python

import pysnmp 
import paramiko

dir(pysnmp) 
dir(paramiko)

snmpver = "".join(str(".".join(str(pysnmp.version).split(','))).split(' ')).lstrip('(').rstrip(')')
paraver = "".join(str(".".join(str(paramiko.__version_info__).split(','))).split(' ')).lstrip('(').rstrip(')')

print 'PySNMP version:\t\t' + str(snmpver)
print 'Paramiko version:\t' + str(paraver)
