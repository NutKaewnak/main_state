from include.abstract_task import AbstractTask
__author__ = 'nicole'


class TestGesture(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtaskBook.get_subtask(self, 'DetectWavingPeople')
            self.change_state('findPeople')

        elif self.state is 'findPeople':
            if self.current_subtask.state is 'finish':
                point = self.current_subtask.get_point()
                self.subtask = self.change_state_with_subtask('moveToGesture', 'MoveRelative')
                if self.subtask is not None:
                    self.subtask.set_position(point.z, point.y, point.x)