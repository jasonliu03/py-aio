#!/usr/bin/env python
#!encoding=utf8

from socket import *
from threading import Thread
import time


THREAD_COUNT = 100
CONN_PER_THREAD = 1000

num_Exception = 0

def worker(count):
    global num_Exception
    bExcep = False
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 10002))
    while count > 0:
        try:
            count -= 1
            sock.send(b'1')
            resp = sock.recv(100)
            #time.sleep(0.1)
        except Exception as e:
            print "Perf-multiprocess.worker Exception:", e, "\n"
            bExcep = True
            break # 1.first [Errno 104] Connection reset by peer 2.the left ones are Broken pipeline

    if bExcep:
        num_Exception += 1
        print "num_Exception:", num_Exception
    
    sock.close()


while THREAD_COUNT > 0:
    Thread(target=worker,args=(CONN_PER_THREAD,)).start()
    THREAD_COUNT -= 1

