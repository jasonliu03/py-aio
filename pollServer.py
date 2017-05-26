#!/usr/bin/env python
import socket,select
from threading import Thread
import time

from fib import fib

s=socket.socket()
host=""
port=10001
s.bind((host,port))
fdmap={s.fileno():s}
s.listen(5)
p=select.poll()
p.register(s,select.POLLIN|select.POLLERR|select.POLLHUP)

num_users = 0
num_CLIENT_QUIT = 0
num_Exception = 0

def fib_handler(client):
    global p
    global num_users
    global num_CLIENT_QUIT
    global num_Exception
#    while True:
    try:
	req = client.recv(100)
	if not req:
            #print "disconnected:", client.getpeername()
	    p.unregister(client)
	    fdmap.pop(client.fileno())
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
	p.unregister(client)
	fdmap.pop(client.fileno())
	client.close()
        num_users -= 1
        num_Exception += 1
        
	#break
#    else:
#        if req:
#	    n = int(req)
#	    result = fib(n)
#	    resp = str(result).encode('utf8') + b'\n'
#	    client.send(resp)

MONITOR_LOOP_COUNT = 100
num = 0
num_done = 0
num_all = 0
result = {}
num_POLLHUP = 0

def monitor(count):
    global num
    global num_done
    global num_all
    global num_users
    global num_POLLHUP
    global num_CLIENT_QUIT
    global num_Exception
    while count > 0:
        time.sleep(1)
        print "--------------------------------"
        print('request:', num, 'reqs/sec')
        print('finished:', num_done, 'reqs/sec')
        num_all += num
        print('num_all:', num_all)
        print('result.len:', len(result))
        print('num_users:', num_users)
        print('num_POLLHUP:', num_POLLHUP)
        print('num_CLIENT_QUIT:', num_CLIENT_QUIT)
        print('num_Exception:', num_Exception)
        num = 0
        num_done = 0
        count -= 1

Thread(target=monitor,args=(MONITOR_LOOP_COUNT,)).start()

while 1:
    result=p.poll(1)	# return null if timeout (ms)
    for fd,events in result:
	if events & select.POLLIN:
	    if fdmap[fd] is s:
		if events & select.POLLIN:
		    try:
			sock,addr=s.accept()
			#print "connected:", sock.getpeername()
			num_users += 1
			sock.setblocking(0)
			p.register(sock,select.POLLIN|select.POLLERR|select.POLLHUP)
			fdmap[sock.fileno()] = sock
		    except Exception as e:
			print "Server Exception:", e
	    else:
		num += 1
		fib_handler(fdmap[fd])
		num_done += 1
	elif events & select.POLLHUP:
	    p.unregister(sock)
	    fdmap.pop(sock.fileno())
	    sock.close()
	    num_POLLHUP += 1
	    num_users -= 1

