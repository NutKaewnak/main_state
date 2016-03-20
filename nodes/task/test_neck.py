from include.abstract_task import AbstractTask
from include.delay import Delay
import rospy
__author__ = 'Frank'


class TestNeck(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
        print "Do not set neck in init, Frank"
        # self.subtask.turn_absolute(0, -0.4)
        self.delay = Delay()
        self.delay.wait(10)

    def perform(self, perception_data):
        print self.subtask.state,  self.delay.is_waiting(), self.state, self.subtask.skill.pan
        if self.state is 'init' and not self.delay.is_waiting():
            if self.subtask.state is 'finish':

                self.subtask.turn_relative(0, 0.8)
                self.delay.wait(5)
                self.change_state("init_2")
        if self.state == 'init_2' and not self.delay.is_waiting():
            if self.subtask.state == 'finish':
                self.subtask.turn_relative(0, -0.8)
                self.delay.wait(5)
                self.change_state("init")

        # self.subtask.turn_relative(0, -0.1)
