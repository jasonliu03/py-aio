#!/usr/bin/env python
import socket,select
from threading import Thread
import time

from fib import fib

server=socket.socket()
host=""
port=10000
server.bind((host,port))
server.listen(5)
inputs = [server]

num_users = 0
num_CLIENT_QUIT = 0
num_Exception = 0

def fib_handler(client):
    global inputs 
    global num_users
    global num_CLIENT_QUIT
    global num_Exception
#    while True:
    try:
	req = client.recv(100)
	if not req:
            #print "disconnected:", client.getpeername()
            inputs.remove(client)
	    client.close()
            num_users -= 1
            num_CLIENT_QUIT += 1
	    #break
        else:
	    n = int(req)
	    result = fib(n)
	    resp = str(result).encode('utf8') + b'\n'
	    client.send(resp)
    except Exception as e:
	print "Server.fib_handler Exception:", e
        inputs.remove(client)
	client.close()
        num_users -= 1
        num_Exception += 1
        

MONITOR_LOOP_COUNT = 100
num = 0
num_done = 0
num_all = 0
num_ERROR = 0

def monitor(count):
    global num
    global num_done
    global num_all
    global num_users
    global num_ERROR
    global num_CLIENT_QUIT
    global num_Exception
    while count > 0:
        time.sleep(1)
        print "--------------------------------"
        print('request:', num, 'reqs/sec')
        print('finished:', num_done, 'reqs/sec')
        num_all += num
        print('num_all:', num_all)
        print "inputs.len:", len(inputs)
        print('num_users:', num_users)
        print('num_ERROR:', num_ERROR)
        print('num_CLIENT_QUIT:', num_CLIENT_QUIT)
        print('num_Exception:', num_Exception)
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
	        num_users += 1
                inputs.append(clientsock);
            except Exception as e:
                print "selectServer Exception:", e, "\n"
        else:
            num += 1
            fib_handler(r)
            num_done += 1
    for e in es:    
        print "e in es..."
        inputs.remove(e)
        e.close() 
	num_ERROR += 1
        num_users -= 1

