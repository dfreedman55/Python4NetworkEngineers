#!/usr/bin/env python

import paramiko
import time

ipadd = '50.76.53.27'
uname = 'pyclass'
pword = '88newclass'
sshpt = 8022

preconnection = paramiko.SSHClient()
preconnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
preconnection.connect(ipadd, port=sshpt, username=uname, password=pword)
connection = preconnection.invoke_shell()
output = connection.recv(5000)
print output

output = connection.send('terminal length 0\n')
time.sleep(1)
print output

output = connection.recv(5000)
print output

output = connection.send('show version\n')
time.sleep(1)
print output

output = connection.recv(65535)
print output
