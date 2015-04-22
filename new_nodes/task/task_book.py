__author__ = "AThousandYears"

from rips import RIPS
from test import Test

class TaskBook:
    def __init__(self, planning_module):
        self.book = {None}
        self.book['RIPS'] = RIPS(planning_module)
        self.book['Test'] = Test(planning_module)

    def set_perception(self, perception_module):
        for task in self.book:
            self.book[task].set_perception(perception_module)