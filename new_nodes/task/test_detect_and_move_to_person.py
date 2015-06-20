__author__ = 'Nicole'
from include.abstract_task import AbstractTask


class TestDetectAndMoveToPerson(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.device is 'VOICE' and perception_data.input is 'start':
                self.change_state('ready')

        elif self.state is 'ready':
            self.subtask = self.subtaskBook.get_subtask(self, 'DetectAndMoveToPeople')
            if self.subtask.state is 'finish':
                self.change_state('finish')
            # Don't forget to add task to task_book
            # Don't forget to create launch file