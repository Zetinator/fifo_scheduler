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
        print ("Starting " + self.name)
        # process.run()
        # Get lock to synchronize threads
        threadLock.acquire()
        current_status[threadID] = process.current_state
        # Free lock to release next thread
        threadLock.release()


class Scheduler:
    def __init__(self):

        # for process in processes:
            # print("ahi va")

        # state variables
        self.the_one_running = None
        self.waiting_list = []


def main(args):
    # initialize processes
    threadLock = threading.Lock()
    loader = ProcessLoader()
    processes = loader.load()
    current_status = []

    for i, process in enumerate(processes):
        current_status.append(None)
        print("si esta bien --> " + str(i))

    # initialize scheduler
    scheduler = Scheduler()
    threads = []

    # Create new threads
    for i, process in enumerate(processes):
        thread = DerThread(i, process)
        thread = start()
        threads.append(thread)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print ("Exiting Main Thread")

if __name__ == '__main__':
    main(sys.argv)
