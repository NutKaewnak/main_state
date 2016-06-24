from include.abstract_task import AbstractTask

__author__ = 'Nicole'


class SpeechRecognition(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'QuestionAnswer')
            self.change_state('direct_asking')

        elif self.state is 'direct_asking':
            if self.subtask.state is 'finish':
                self.change_state('prepare_for_indirect')

        elif self.state is 'prepare_for_indirect':
            # face detection here NOT FINISH
            # may have change structure of this code
            self.subtask.change_state('init')
            self.change_state('indirect_asking')

        elif self.state is 'indirect_asking':
            if self.subtask.state is 'finish':
                self.change_state('finish')
