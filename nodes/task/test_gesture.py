from include.abstract_task import AbstractTask

__author__ = 'Frank'


class TestRecognition(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'RecognizeObjects')
            self.change_state('findObject')

        elif self.state is 'findObject':
            if self.current_subtask.state is 'finish':
                point = self.current_subtask.get_point()
                self.subtask = self.change_state_with_subtask('moveToGesture', 'MoveRelative')

                # TODO: move the code below to subtask
                if self.subtask is not None:
                    magic_number = 0
                    if point.y > 0:
                        magic_number = -0.2
                    elif point.y < 0:
                        magic_number = 0.2
                    self.subtask.set_position(point.x - 0.15, point.y + magic_number, atan(point.y/point.x))
