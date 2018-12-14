#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy as np
import time
import os
import csv

class PCB:
    def __init__(self, pcb_id, name, pc_burst, vector_status, threadLock):
        try:
            # set-up
            self.pcb_id = pcb_id
            self.name = name
            self.pc_burst = pc_burst
            self.vector_status = vector_status
            self.threadLock = threadLock

            # state variables
            self.states = ["NEW","READY","RUNNING","WAIT","TERMINATED"]
            self.current_state = self.states[0]
            # update
            self.update_vector_status()

            self.running_time = 0
            self.waiting_time = 0

            # initializing...
            self.print_state()

            # go to ready
            self.ready()
        except:
            print("An error ocurred while trying to initialize the given process")


    def ready(self):
        try:
            self.current_state = self.states[1]
            # update
            self.update_vector_status()

            self.print_state()
        except:
            print("An error ocurred while trying to set the given process in the ready state")


    def run(self):
        try:
            self.current_state = self.states[2]
            # update
            self.update_vector_status()

            self.print_state()

            # sleep for a random time
            sweet_dreams = np.random.uniform(1,5,1)
            time.sleep(sweet_dreams)
            # statistics...
            self.running_time += sweet_dreams

            self.pc_burst -= 1
            if (self.pc_burst <= 0):
                self.terminated()
                return(0)
            else:
                print("at: " + str(time.time()) + "\tPROCESS: " + self.name + "\tSTATUS: requesting I/O...")
                self.wait()

        except:
            print("An error ocurred while trying to run the given process")


    def wait(self):
        try:
            self.current_state = self.states[3]
            # update
            self.update_vector_status()

            self.print_state()

            # sleep for a random time
            sweet_dreams = np.random.uniform(1,5,1)
            time.sleep(sweet_dreams)
            # statistics...
            self.waiting_time += sweet_dreams

            print("at: " + str(time.time()) + "\tPROCESS: " + self.name + "\tSTATUS: got it...")
            self.ready()

        except:
            print("An error ocurred while trying to block the given process")


    def terminated(self):
        try:
            self.current_state = self.states[4]
            # update
            self.update_vector_status()

            self.print_state()
        except:
            print("An error ocurred while trying to terminate the given process")

    def update_vector_status(self):
        self.threadLock.acquire()
        self.vector_status[self.pcb_id] = self.current_state
        self.threadLock.release()

    def print_state(self):
        print("at: " + str(time.time()) + "\tPROCESS: " + self.name + "\tSTATUS: " + self.current_state)


class ProcessLoader:
    def __init__(self, vector_status, vector_process, threadLock):
        self.processes = vector_process
        self.vector_status = vector_status
        self.vector_process = vector_process
        self.threadLock = threadLock

    def load (self):
        with open(os.path.join(os.getcwd(), 'inputs.txt'), 'r') as f:
            n = sum(1 for line in f)

        for i in range(n):
            self.threadLock.acquire()
            self.vector_status.append(None)
            self.vector_process.append(None)
            self.threadLock.release()

        with open(os.path.join(os.getcwd(), 'inputs.txt'), 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for i, row in enumerate(reader):
                self.vector_process[i] = PCB(i, row[0], int(row[1]), self.vector_status, self.threadLock)
                print(self.vector_process[i].name + "... created")
        return (0)
