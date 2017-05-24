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

def fib_handler(client):
    global p
    while True:
        try:
            req = client.recv(100)
            if not req:
                p.unregister(client)
                #client.close()
                fdmap.pop(client.fileno())
                break
        except Exception as e:
            print "Server.fib_handler Exception:", e
            p.unregister(client)
            #client.close()
            fdmap.pop(client.fileno())
            break
        else:
            n = int(req)
            result = fib(n)
            resp = str(result).encode('utf8') + b'\n'
            client.send(resp)

MONITOR_LOOP_COUNT = 50
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
    result=p.poll()
    if len(result)!=0:
        for fd,events in result:
            if events & select.POLLIN:
                if fdmap[fd] is s:
                    if events & select.POLLIN:
                        try:
                            sock,addr=s.accept()
                            p.register(sock,select.POLLIN|select.POLLERR|select.POLLHUP)
                            fdmap[sock.fileno()] = sock
                        except Exception as e:
                            print "Server Exception:", e
                else:
                    num += 1
                    fib_handler(fdmap[fd])
                    num_done += 1
#            elif events & select.POLLHUP:
#                p.unregister(sock)
#                sock.close()
#                fdmap.pop(sock.fileno())

    #print "no data"
