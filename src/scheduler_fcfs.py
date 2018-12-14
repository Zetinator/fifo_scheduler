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


class DerThreadLoader (threading.Thread):
    def __init__(self, threadID, loader, vector_status, vector_process):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.vector_status = vector_status
        self.vector_process = vector_process
    def run(self):

        # print(vector_status)
        # initialize processes
        print("-----Initializing-----")
        loader.load()

class DerThreadPCB (threading.Thread):
    def __init__(self, threadID, process):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.process = process
    def run(self):
        self.process.run()


class Scheduler:
    def __init__(self, vector_process, vector_status):
        # state variables
        aux_counter = 0
        self.the_one_running = None
        self.fifo_ready = []
        self.fifo_waiting = []
        self.fifo_terminated = []

        while ((len(self.fifo_terminated) == 0) or (len(self.fifo_terminated) != len(vector_process))):
            for i, pcb in enumerate(vector_process):
                if (pcb.current_state == 'READY') and not (pcb in self.fifo_ready):
                    self.fifo_ready.append(pcb)
                if (pcb.current_state == 'READY') and (pcb in self.fifo_waiting):
                    self.fifo_waiting.remove(pcb)
                if (pcb.current_state == 'WAIT') and not (pcb in self.fifo_waiting):
                    self.fifo_waiting.append(pcb)
                if (pcb.current_state == 'TERMINATED') and not (pcb in self.fifo_terminated):
                    self.fifo_terminated.append(pcb)
            if len(self.fifo_ready) != 0:
                self.the_one_running = self.fifo_ready.pop(0)
                print("TO BE RUNNED --> " + self.the_one_running.name)
                thread = DerThreadPCB(aux_counter, self.the_one_running)
                thread.start()
                while (self.the_one_running.current_state == 'RUNNING'):
                    pass
                aux_counter += 1



if __name__ == '__main__':
    threadLock = threading.Lock()
    # vector status
    vector_status = []
    # vector_processes
    vector_process = []

    # initialize the loader
    loader = ProcessLoader(vector_status, vector_process, threadLock)

    # go for it boy (#threadZeit)
    thread = DerThreadLoader(0, loader, vector_process, vector_status)
    thread.start()

    # initialize scheduler
    scheduler = Scheduler(vector_process, vector_status)

    print("\nFINAL_STATUS_VECTOR: "  + str(vector_status))
    print ("Exiting Main Thread... das war alles")
