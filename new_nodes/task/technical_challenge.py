__author__ = 'nicole'
from include.abstract_task import AbstractTask
import rospy
from manipulator.srv import manipulator


class TechnicalChallenge(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.action = rospy.ServiceProxy('', manipulator)

    def perform(self, perception_data):
        if self.state is 'init':
            if perception_data.device is 'VOICE':
                if 'introduce yourself' in perception_data.input:
                    self.change_state_with_subtask('introduce', 'Introduce')

        elif self.state is 'introduce':
            if perception_data.device is 'VOICE':
                if 'crack' in perception_data.input and 'egg' in perception_data.input:
                    # publish code for crack the egg
                    self.action('crack')
                    self.subtaskBook.get_subtask(self, 'Say').say('I will crack this egg')
                    self.change_state('finish')
            # Don't forget to add task to task_book