#!/usr/bin/env python
import socket,select
from threading import Thread
import time

from fib import fib

num_users = 0 
num_CLIENT_QUIT = 0 
num_Exception = 0 

MONITOR_LOOP_COUNT = 10  
num = 0 
num_done = 0 
num_all = 0 
num_ERROR = 0 

def monitor(count, result):
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
        print('num_all:', num_all)
        print('result.len:', len(result))
        print('num_users:', num_users)
        print('num_ERROR:', num_ERROR)
        print('num_CLIENT_QUIT:', num_CLIENT_QUIT)
        print('num_Exception:', num_Exception)
        num = 0 
        num_done = 0 
        count -= 1

def monitor_start(result):
    Thread(target=monitor,args=(MONITOR_LOOP_COUNT, result)).start()


p = []
fdmap = {}
result = []

def fib_handler(client):
    global p
    global num_users
    global num_CLIENT_QUIT
    global num_Exception
    try:
	req = client.recv(100)
	if not req:
            #print "disconnected:", client.getpeername()
	    p.unregister(client)
	    fdmap.pop(client.fileno())
	    client.close()
            num_users -= 1
            num_CLIENT_QUIT += 1
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
        
def main():
    global p
    global fdmap
    global result
    global num 
    global num_done
    global num_all
    global num_users
    global num_ERROR

    s=socket.socket()
    host=""
    port=10002
    s.bind((host,port))
    fdmap={s.fileno():s}
    s.listen(5)
    p=select.poll()
    p.register(s,select.EPOLLIN|select.EPOLLERR|select.EPOLLHUP)

    monitor_start(result)

    while 1:
        result=p.poll(1)	# return null if timeout (ms)
        for fd,events in result:
            if events & select.EPOLLIN:
                if fdmap[fd] is s:
                    try:
                        sock,addr=s.accept()
                        #print "connected:", sock.getpeername()
                        num_users += 1
                        sock.setblocking(0) # really needed? maybe not because POLLIN means data ready, so won't block
                        p.register(sock,select.POLLIN|select.POLLERR|select.POLLHUP)
                        fdmap[sock.fileno()] = sock
                    except Exception as e:
                        print "Server Exception:", e
                else:
                    num += 1
                    num_all += 1
                    fib_handler(fdmap[fd])
                    num_done += 1
            elif events & select.EPOLLHUP:
                p.unregister(sock)
                fdmap.pop(sock.fileno())
                sock.close()
                num_ERROR += 1
                num_users -= 1

if __name__ == '__main__':
    main()
