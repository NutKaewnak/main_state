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
        if self.state is not 'finish':
            rospy.loginfo('FindPeopleUsingGesture state : '+self.state)
        if self.state is 'init':
            self.neck.reset()
            self.neck.prepare()
            self.change_state('waitForNeck')

        elif self.state is 'waitForNeck':
            if self.neck.state is 'waitAtStart':
                self.skill = self.skillBook.get_skill(self, 'DetectPeopleWithGesture')
                self.neck.start()
                self.skill.start()
                self.change_state('searching')

        elif self.state is 'searching':
            if self.skill.state is 'succeeded':
                self.neck.stop()
                self.pos = self.skill.get_point()
                self.change_state('finish')
            elif self.neck.state is 'succeeded':
                self.change_state('notFound')

    def get_point(self):
        return self.pos
