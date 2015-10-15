#!/usr/bin/env python

import paramiko
import time

ipadd = '50.76.53.27'
uname = 'pyclass'
pword = '88newclass'
sshpt = 22

preconnection = paramiko.SSHClient()
preconnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
preconnection.connect(ipadd, port=sshpt, username=uname, password=pword)
connection = preconnection.invoke_shell()
output = connection.recv(5000)
print output

output = connection.send('terminal length 0\nshow run | in logging\n')
time.sleep(1)
print output

output = connection.recv(5000)
print output

output = connection.send('config t\nlogging buffered 32768\nend\n')
time.sleep(1)
print output

output = connection.recv(5000)
print output

output = connection.send('show run | in logging\n')
time.sleep(1)
print output

output = connection.recv(5000)
print output
