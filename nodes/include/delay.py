#!/usr/bin/env python
import time


class Delay:
    def __init__(self):
        self.start_time = time.localtime()
        self.period = 0

    def wait(self, period):
        self.period = period
        self.start_time = time.localtime()

    def is_waiting(self):
        current_time = time.localtime()
        if time.mktime(current_time) - time.mktime(self.start_time) >= self.period:
            return False
        return True

