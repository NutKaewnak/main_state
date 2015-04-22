__author__ = "AThousandYears"

from rips import RIPS


class TaskBook:
    def __init__(self, planning_module):
        self.book = {}
        self.book['RIPS'] = RIPS(planning_module)

    def set_perception(self, perception_module):
        for task in self.book:
            self.book[task].set_perception(perception_module)