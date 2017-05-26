#!/usr/bin/env python
#!encoding=utf8

from socket import *
from threading import Thread
import time

THREAD_COUNT = 400
CONN_PER_THREAD = 1000

num_Exception = 0

def worker(count):
    global num_Exception
    bExcep = False
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 10000))
    while count > 0:
        try:
            count -= 1
            sock.send(b'1')
            resp = sock.recv(100)
        except Exception as e:
            print "selectPerf-multiprocess.worker Exception:", e, "\n"
    if bExcep:
        num_Exception += 1
        print "num_Exception:", num_Exception
    sock.close()


while THREAD_COUNT > 0:
    Thread(target=worker,args=(CONN_PER_THREAD,)).start()
    THREAD_COUNT -= 1

