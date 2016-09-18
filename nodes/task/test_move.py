from include.abstract_task import AbstractTask

__author__ = 'cindy'


class TestMove(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.count = 0

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            print 'init state'
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
            self.subtask.set_position(1.5, 0.0, 0.0)
            self.change_state('move')

        elif self.state is 'move':
            if self.subtask.state is 'finish':
                print 'state finish'
                if self.count < 5 and self.count % 2 == 0:
                    self.subtask = self.subtaskBook.get_subtask(self, 'Say')
                    self.subtask.say('hello, My name is Lumyai')
                    self.change_state('init')
                elif self.count < 5 and self.count % 2 != 0:
                    self.change_state('init')
                else:
                    self.change_state('finish')
            # Don't forget to add task to task_book
            # Don't forget to create launch file
