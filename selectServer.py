#!/usr/bin/env python
import socket,select
from threading import Thread
import time

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('',10000))
server.listen(5)
inputs=[server]

from fib import fib

def fib_handler(client):
    while True:
        try:
            req = client.recv(100)
            if not req:
                inputs.remove(client)
                break
        except Exception as e:
            print "selectServer.fib_handler Exception:", e
            inputs.remove(client)
            break
        else:
            n = int(req)
            result = fib(n)
            resp = str(result).encode('ascii') + b'\n'
            client.send(resp)


MONITOR_LOOP_COUNT = 100
num = 0
num_done = 0
num_all = 0
def monitor(count):
    global num
    global num_done
    global num_all
    while count > 0:
        time.sleep(1)
        print('request:', num, 'reqs/sec')
        print('finished:', num_done, 'reqs/sec')
        num_all += num
        print('num_all:', num_all)
        num = 0
        num_done = 0
        count -= 1

Thread(target=monitor,args=(MONITOR_LOOP_COUNT,)).start()

while 1:
    rs,ws,es=select.select(inputs,[],[],1)
    for r in rs:
        if r is server:
            try:
                clientsock,clientaddr=r.accept();
                #print "Connected:", clientaddr
                inputs.append(clientsock);
            except Exception as e:
                print "selectServer Exception:", e, "\n"
        else:
            num += 1
	    fib_handler(r)
            num_done += 1

