from include.abstract_subtask import AbstractSubtask
import rospy
__author__ = 'nicole'


class TurnNeck(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'TurnNeck')
        # self.skill.turn(0, 0)

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('wait_for_command')

        elif self.state is 'receive_command':
            if self.skill.state is 'succeeded':
                print 'Succeeded'
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                self.change_state('error')

    def turn_relative(self, pitch, yaw):
        self.skill.turn_relative(pitch, yaw)
        self.change_state('receive_command')

    def turn_absolute(self, pitch, yaw):
        self.skill.turn(pitch, yaw)
        self.change_state('receive_command')
