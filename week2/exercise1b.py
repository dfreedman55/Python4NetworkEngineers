#!/usr/bin/env python

import pysnmp
import paramiko

pysnmp_version = pysnmp.version
version = []
for item in pysnmp_version:
	version.append(str(item))
pysnmp_version = '.'.join(version)
paramiko_version = paramiko.__version__	

print 'PYSNMP Version: \t' + pysnmp_version
print 'PARAMIKO Version: \t' + paramiko_version
