__author__ = 'nicole'
from include.abstract_task import AbstractTask

class Test(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'Introduce')
            self.change_state('finish')