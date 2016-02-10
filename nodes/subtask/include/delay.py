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
        if self.get_dif() >= self.period:
            return False
        return True

    def get_dif(self):
        current_time = time.localtime()
        return time.mktime(current_time) - time.mktime(self.start_time)