__author__ = 'Nicole'
from include.abstract_task import AbstractTask


class SpeechRecognition(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'QuestionAnswer')
            self.change_state('indirect')

        elif self.state is 'indirect':
            # face detection here NOT FINISH
            # may have change structure of this code
            self.subtask.change_state('init')
            self.change_state('finish')