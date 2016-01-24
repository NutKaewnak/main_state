from include.abstract_task import AbstractTask

__author__ = 'nicole'


class Test(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'Pick')
            self.change_state('finish')
