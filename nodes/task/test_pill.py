from include.abstract_task import AbstractTask
__author__ = 'nicole'


class TestPill(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            self.subtask = self.subtaskBook.get_subtask(self, 'PillsDetection')
            self.subtask.start()
            self.change_state('detect')

        elif self.state is 'detect':
            if self.subtask.state is 'finish':
                self.change_state('finish')
            # Don't forget to add task to task_book
            # Don't forget to create launch file
