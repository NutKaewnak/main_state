__author__ = 'Nicole'
import rospy
from include.delay import Delay
from include.abstract_subtask import AbstractSubtask


class TurnNeckSearching(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'TurnNeck')
        self.minute = Delay()
        self.timer = Delay()

    def perform(self, perception_data):
        print('Angle : '+str(self.angle))
        rospy.loginfo('Turn Neck state : '+self.state)
        self.minute.wait(60)
        if self.state is 'start':
            if self.timer.is_waiting():
                return
            self.skill.turn(0, 0.3)

            if not self.minute.is_waiting():
                self.change_state('succeeded')

        elif self.state is 'stop':
                self.change_state('stopped')

    def start(self):
        self.change_state('start')
        rospy.loginfo('Neck starting')

    def stop(self):
        self.change_state('stop')
