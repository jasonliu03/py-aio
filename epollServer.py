#!/usr/bin/env python
import socket,select
from threading import Thread
import time

from fib import fib

s=socket.socket()
host=""
port=10002
s.bind((host,port))
fdmap={s.fileno():s}
s.listen(5)
p=select.epoll()
p.register(s.fileno(),select.POLLIN|select.POLLERR|select.POLLHUP)

def fib_handler(client):
    global p
    while True:
        try:
            req = client.recv(100)
            if not req:
                p.unregister(client.fileno())
                fdmap.pop(client.fileno())
                client.close()
                break
        except Exception as e:
            print "Server.fib_handler Exception:", e
            p.unregister(client.fileno())
            fdmap.pop(client.fileno())
            client.close()
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
    for fd,events in result:
        if events & select.POLLIN:
            if fdmap[fd] is s:
                if events & select.POLLIN:
                    try:
                        sock,addr=s.accept()
                        p.register(sock.fileno(),select.POLLIN|select.POLLERR|select.POLLHUP)
                        fdmap[sock.fileno()] = sock
                    except Exception as e:
                        print "Server Exception:", e
            else:
                num += 1
                fib_handler(fdmap[fd])
                num_done += 1
        elif events & select.POLLHUP:
            p.unregister(sock.fileno())
            fdmap.pop(sock.fileno())
            sock.close()

    #print "no data"
