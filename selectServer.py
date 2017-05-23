#!/usr/bin/env python
import socket,select
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('',10000))
server.listen(5)
inputs=[server]
#import pdb
#pdb.set_trace()

from fib import fib

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            inputs.remove(client)
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print('Closed')

while 1:
    rs,ws,es=select.select(inputs,[],[],1)
    for r in rs:
        if r is server:
            clientsock,clientaddr=r.accept();
            print "Connected:", clientaddr
            inputs.append(clientsock);
        else:
            #data=r.recv(1024);
            #if not data:
            #    inputs.remove(r);
            #else:
                #print data
                #r.send(data)
	    fib_handler(r)

