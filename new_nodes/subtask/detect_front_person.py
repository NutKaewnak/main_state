__author__ = 'Nicole'
import rospy
import math
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
                self.subtask = self.subtaskBook.get_subtask(self, 'PeopleDetect')
                self.delay = Delay()
                self.delay.wait(3)
                self.change_state('detecting')

        elif self.state is 'detecting':
            if self.subtask.is_found:
                if math.abs(self.subtask.nearest_people.y) <= 0.05:
                    self.is_in_front = True
                    self.change_state('found')
            elif not self.delay.is_waiting():
                self.is_in_front = False
                self.change_state('not_found')

    def detect(self):
        self.change_state('start')
