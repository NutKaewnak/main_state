__author__ = 'Nicole'
import rospy
from include.delay import Delay
from include.abstract_subtask import AbstractSubtask


class DetectFrontPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.delay = None
        self.is_in_front = False

    def perform(self, perception_data):
        if self.state is 'start':
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.skill.turn(0, 0)
            self.is_in_front = False
            self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            if self.skill.state is 'succeeded':
                rospy.loginfo('turn_neck succeeded')
                self.subtask = self.subtaskBook.get_subtask(self, 'PeopleDetect')
                self.delay = Delay()
                self.delay.wait(3)
                rospy.loginfo('DetectFrontPerson: detecting')
                self.change_state('detecting')

        elif self.state is 'detecting':
            if self.subtask.is_found:
                if abs(self.subtask.nearest_people.y) <= 0.03:
                    self.is_in_front = True
                    rospy.loginfo('DetectFrontPerson: found')
                    self.change_state('found')
                else:
                    self.subtask.is_found = False
            elif not self.delay.is_waiting():
                self.is_in_front = False
                rospy.loginfo('DetectFrontPerson: not_found')
                self.change_state('not_found')

    def detect(self):
        self.change_state('start')
