#!/usr/bin/env python

import paramiko
import time

ipadd = '50.76.53.27'
uname = 'pyclass'
pword = '88newclass'
port = 8022

preconnection = paramiko.SSHClient()
preconnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
preconnection.connect(ipadd, port=port, username=uname, password=pword)
connection = preconnection.invoke_shell()
output = connection.recv(5000)
print output
connection.send('terminal length 0\nshow version\n')
time.sleep(1)
output = connection.recv(5000)
print output
