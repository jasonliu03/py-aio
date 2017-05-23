#!/usr/bin/env python
#!encoding=utf8

from socket import *
from threading import Thread
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 10000))

n = 0
LOOP_COUNT = 30

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
Thread(target=monitor,args=(LOOP_COUNT,)).start()


while True:
    start = time.time()
    sock.send(b'2')
    resp = sock.recv(100)
    end = time.time()
    n += 1

#代码非常简单，通过全局变量n来统计qps(req/sec 每秒请求数)
