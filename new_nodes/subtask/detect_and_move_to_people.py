__author__ = 'nicole'
from include.abstract_subtask import AbstractSubtask


class DetectAndMoveToPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'FindPeopleUsingGesture')
            self.change_state('findPeople')

        elif self.state is 'findPeople':
            if self.subtask.state is 'finish':
                pos = self.subtask.getPos()
                self.subtask = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
                self.subtask.setPoint(pos)
                self.change_state('moveToPeople')
            elif self.subtask.state is 'notFound':
                self.skillBook.get_skill('Say').say('I can not found anyone.')
                self.change_state('notFound')