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
        self.process.run()


class Scheduler:
    def __init__(self, processes, vector_status):
        print("----Getting Ready-----")
        for i, process in enumerate(processes):
            process.ready()
        print("\n")


        # state variables
        counter = 0
        self.the_one_running = None
        self.fifo_ready = []
        self.fifo_waiting = []
        while (1):
            for i, pcb in enumerate(processes):
                if (pcb.current_state == 'READY') and not (pcb in self.fifo_ready):
                    self.fifo_ready.append(pcb)
                    # print(pcb.name + " --> fifo_ready")
                if (pcb.current_state == 'READY') and (pcb in self.fifo_waiting):
                    self.fifo_waiting.remove(pcb)
                    # print(pcb.name + " --> from waiting to fifo_ready")
                if (pcb.current_state == 'WAIT') and not (pcb in self.fifo_waiting):
                    self.fifo_waiting.append(pcb)
                    # print(pcb.name + " --> fifo_waiting")
            if len(self.fifo_ready) != 0:
                to_run = self.fifo_ready.pop(0)
                print("to be runned --> " + to_run.name)
                thread = DerThread(counter, to_run)
                thread.start()
                counter += 1



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
    scheduler = Scheduler(processes, vector_status)

    # --------------------TESTING--------------------
    # threads = []
    # for i, process in enumerate(processes):
    #     thread = DerThread(i, process)
    #     thread.start()
    #     threads.append(thread)
    #
    # while (1):
    #     print(str(vector_status))
    #
    # for t in threads:
    #     t.join()
    # -----------------ENDTESTING--------------------
    print("the... "  + str(vector_status))
    print ("Exiting Main Thread")
