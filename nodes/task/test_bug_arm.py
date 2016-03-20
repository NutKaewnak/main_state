from include.abstract_task import AbstractTask

__author__ = 'nicole'


class TestBugArm(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
            self.change_state("pub")

        elif self.state is 'pub':
            self.subtask.turn_absolute(0, 0)
