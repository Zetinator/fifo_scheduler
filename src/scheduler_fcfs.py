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
        # print ("Starting " + self.name)
        # print("threadID --> " + str(self.threadID))
        # print("status   --> " + str(process.current_state))
        # process.run()
        # process.ready()
        # Get lock to synchronize threads
        threadLock.acquire()
        current_status[self.threadID] = process.current_state
        # print(str(current_status))
        # Free lock to release next thread
        threadLock.release()


class Scheduler:
    def __init__(self):
        print("---------Ready--------")
        for i, process in enumerate(processes):
            process.ready()
        print("\n")

        # state variables
        self.the_one_running = None
        self.waiting_list = []


if __name__ == '__main__':
    threadLock = threading.Lock()
    # initialize processes
    loader = ProcessLoader()
    print("-----Initializing-----")
    processes = loader.load()
    print("\n")

    # status vector
    current_status = []
    for i, process in enumerate(processes):
        current_status.append(None)

    # initialize scheduler
    scheduler = Scheduler()

    # Create new threads
    threads = []
    for i, process in enumerate(processes):
        thread = DerThread(i, process)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("the... "  + str(current_status))
    print ("Exiting Main Thread")
