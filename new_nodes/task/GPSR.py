__author__ = 'nicole'
from include.abstract_task import AbstractTask


class GPSR(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            if self.state is 'init':
