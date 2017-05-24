#!/usr/bin/env python
#!encoding=utf8

from socket import *
from threading import Thread
import time

n = 0
LOOP_COUNT = 30

THREAD_COUNT = 400
CONN_PER_THREAD = 1000

def monitor(count):
    global n
    i = 0
    while True:
        if i >= count:
            break
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0
        i += 1
#Thread(target=monitor,args=(LOOP_COUNT,)).start()

def worker(count):
    while count > 0:
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(('localhost', 10000))
            sock.send(b'1')
            resp = sock.recv(100)
            sock.close()
            count -= 1
        except Exception as e:
            print "selectPerf-multiprocess.worker Exception:", e, "\n"

#代码非常简单，通过全局变量n来统计qps(req/sec 每秒请求数)

while THREAD_COUNT > 0:
    Thread(target=worker,args=(CONN_PER_THREAD,)).start()
    THREAD_COUNT -= 1

