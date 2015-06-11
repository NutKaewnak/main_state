__author__ = 'Nicole'
from include.abstract_task import AbstractTask


class Manipulation(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            self.subtask = self.subtaskBook.get_subtask(self, 'SearchObjectByVoice')
            self.subtask.search_for()

        if
            self.change_state('finish')
            # Don't forget to add task to task_book
