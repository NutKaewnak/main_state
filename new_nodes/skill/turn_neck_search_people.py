__author__ = 'nicole'

from include.abstract_skill import AbstractSkill
from include.delay import Delay
import rospy
import math


class TurnNeckForSearchPeople(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.neck = self.controlModule.neck
        self.minute = Delay()
        self.minute.wait(60)
        self.timer = Delay()
        self.angle = -1.57

    def perform(self, perception_data):
        print('Angle : '+str(self.angle))
        rospy.loginfo('Turn Neck state : '+self.state)
        if self.state is 'start':
            if self.timer.is_waiting():
                return
            self.angle += 0.3
            self.neck.set_neck_angle(0, self.angle)
            self.timer.wait(5)
            if self.angle >= 90*math.pi/180:
                self.angle = -90*math.pi/180
                self.neck.set_neck_angle(0, self.angle)

            if not self.minute.is_waiting():
                self.change_state('succeeded')
        elif self.state is 'stop':
                self.change_state('stopped')

    def prepare(self):
        # self.neck.set_neck_angle(0, 0)
        self.angle = -90*math.pi/180
        self.neck.set_neck_angle(0, self.angle)
        self.change_state('waitAtStart')
        self.timer.wait(2)
        rospy.loginfo('Neck Preparing')

    def start(self):
        if self.state is not 'waitAtStart':
            return
        self.change_state('start')
        self.timer.wait(0)
        rospy.loginfo('Neck starting')

    def stop(self):
        self.change_state('stop')
        self.timer.wait(0)
