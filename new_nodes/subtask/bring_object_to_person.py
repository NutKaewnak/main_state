__author__ = 'nicole'
import rospy
from include.abstract_subtask import AbstractSubtask


class BringObjectToPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.name = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.name = None

        elif self.state is 'start':
            self.subtask = self.subtaskBook(self, 'MoveToLocation')
            self.subtask.to_location('LivingRoom')
            self.change_state('moveToLivingRoom')

        elif self.state is 'moveToLivingRoom':
            if self.current_subtask.state is None:
                self.subtask = self.subtaskBook.get_subtask(self, 'DetectAndMoveToPeople')
                self.change_state('detectAndMoveToPeople')

        elif self.state is 'findPeople':
            if self.subtask.state is 'finish':
                pos = self.subtask.getPos()
                self.subtask = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
                self.subtask.setPoint(pos)
                self.change_state('moveToPeople')
            elif self.subtask.state is 'notFound':
                self.skillBook.get_skill('Say').say('I can not found anyone.')
                self.change_state('notFound')

        elif self.change_state('moveToPeople'):
            if self.subtask.state is 'finish':
                # self.subtask = self.subtaskBook.get_subtask(self, 'AskForNameAndCommand')  # must make it
                self.change_state('askForCommand')

    def start(self, name):
        self.name = name
        self.change_state('start')
    # Don't forget to add this subtask to subtask book