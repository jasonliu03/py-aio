#!/usr/bin/env python
#!encoding=utf8

from socket import *
from threading import Thread
import time


THREAD_COUNT = 300
CONN_PER_THREAD = 1000


def worker(count):
    while count > 0:
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(('localhost', 10002))
            sock.send(b'1')
            resp = sock.recv(100)
            sock.close()
            count -= 1
        except Exception as e:
            print "Perf-multiprocess.worker Exception:", e, "\n"


while THREAD_COUNT > 0:
    Thread(target=worker,args=(CONN_PER_THREAD,)).start()
    THREAD_COUNT -= 1

