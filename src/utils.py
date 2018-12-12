#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import numpy as np
import time
import os
import csv

class PCB:
    def __init__(self, name, pc_burst):
        try:
            # set-up
            self.name = name
            self.pc_burst = pc_burst

            # state variables
            self.states = ["NEW","READY","RUNNING","WAIT"]
            self.current_state = self.states[0]
            self.running_time = 0
            self.waiting_time = 0

            # initializing...
            self.print_state()
        except:
            print("An error ocurred while trying to initialize the given process")


    def ready(self):
        try:
            self.current_state = self.states[1]
            self.print_state()
        except:
            print("An error ocurred while trying to set the given process in the ready state")


    def run(self):
        try:
            self.current_state = self.states[2]
            self.print_state()

            # sleep for a random time
            sweet_dreams = np.random.uniform(1,5,1)
            time.sleep(sweet_dreams)
            # statistics...
            self.running_time += sweet_dreams

            print("              --> requesting I/O...")
            self.pc_burst -= 1
            self.wait()

        except:
            print("An error ocurred while trying to run the given process")


    def wait(self):
        try:
            self.current_state = self.states[3]
            self.print_state()

            # sleep for a random time
            sweet_dreams = np.random.uniform(1,5,1)
            time.sleep(sweet_dreams)
            # statistics...
            self.waiting_time += sweet_dreams

            print("              --> got it...")
            self.ready()

        except:
            print("An error ocurred while trying to block the given process")

    def print_state(self):
        print("at: " + str(time.time()))
        print("PROCESS   --> " + self.name)
        print("STATUS    --> " + self.current_state)


class ProcessLoader:
    def __init__(self):
        self.processes = []

    def load (self):
        with open(os.path.join(os.getcwd(), 'inputs.txt'), 'r') as f:
            reader = csv.reader(f, delimiter=',')
            self.processes = [PCB(row[0],row[1]) for row in reader]
        return (np.array(self.processes))
