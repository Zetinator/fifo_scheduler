#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
from os import path
import time

from utils import Loader
from utils import PCB

import threading
import time
import sys
import numpy as np


class DerThread (threading.Thread):
    def __init__(self, process):
        threading.Thread.__init__(self)
        self.process = process
    def run(self):
        print ("Starting " + self.name)
        # Get lock to synchronize threads
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # Free lock to release next thread
        threadLock.release()


class Scheduler:
    def __init__(self):

        for process in self.processes:
            print("ahi va")

        # state variables
        self.the_one_running = None
        self.waiting_list = []


def main(args):
    # initialize processes
    loader = DerLoader()
    self.processes = loader.load()
    n = len(self.processes)
    for i in n:
        process


    # initialize scheduler
    scheduler = Scheduler()
    threadLock = threading.Lock()
    threads = []

    # Create new threads
    for i in n:
        thread = DerThread(i, self.process[i])
        threads.append(thread)

    # Start new Threads
    thread1.start()
    thread2.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print ("Exiting Main Thread")

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main(sys.argv)
