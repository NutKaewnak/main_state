__author__ = 'nicole'
import rospy
from include.abstract_subtask import AbstractSubtask


class FindPeopleUsingGesture(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.neck = self.skillBook.get_skill(self, 'TurnNeckForSearchPeople')
        self.pos = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.neck.prepare()
            self.change_state('waitForNeck')

        elif self.state is 'waitForNeck':
            if self.neck.state is 'waitAtStart':
                self.skill = self.skillBook.get_skill(self, 'DetectPeopleWithGesture')  # must make it
                self.skill.start()
                self.neck.start()
                self.change_state('searching')

        elif self.state is 'searching':
            if self.skill.state is 'found':
                self.neck.stop()
                self.pos = self.skill.getPos()
                self.change_state('finish')
            elif self.neck.state is 'succeed':
                self.change_state('notFound')

    def getPos(self):
        return self.pos
