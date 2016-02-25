from include.abstract_task import AbstractTask
__author__ = 'nicole'


class TestSpeech(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            if self.current_subtask is None:
                self.subtask = self.subtaskBook.get_subtask(self, 'ExtractObjectLocation')
            self.change_state('finish')
            # Don't forget to add task to task_book
