#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
from os import path
import time

from utils import ProcessLoader
from utils import PCB

import threading
import time
import sys
import numpy as np


class DerThread (threading.Thread):
    def __init__(self, threadID, process):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.process = process
    def run(self):
        process.run()
        threadLock.acquire()
        threadLock.release()


class Scheduler:
    def __init__(self):
        print("----Getting Ready-----")
        for i, process in enumerate(processes):
            process.ready()
        print("\n")

        # state variables
        self.the_one_running = None
        self.waiting_list = []


if __name__ == '__main__':
    threadLock = threading.Lock()
    # vector status 
    vector_status = []
    loader = ProcessLoader(vector_status, threadLock)
    for i in range(loader.get_n()):
        vector_status.append(None)

    # initialize processes
    print("-----Initializing-----")
    processes = loader.load()
    print("\n")


    # initialize scheduler
    scheduler = Scheduler()

    # --------------------TESTING--------------------
    threads = []
    for i, process in enumerate(processes):
        thread = DerThread(i, process)
        thread.start()
        threads.append(thread)

    # while (1):
        # print(str(vector_status))

    for t in threads:
        t.join()
    # -----------------ENDTESTING--------------------
    print("the... "  + str(vector_status))
    print ("Exiting Main Thread")
