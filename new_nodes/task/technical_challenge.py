from geometry_msgs.msg import Vector3
import math

__author__ = 'nicole'
from include.abstract_task import AbstractTask
import rospy
from manipulator.srv import ManipulateAction


class TechnicalChallenge(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.action = rospy.ServiceProxy('/ManipulateAction', ManipulateAction)
        self.set_neck_angle_topic = rospy.Publisher('/hardware_bridge/set_neck_angle', Vector3)

    def perform(self, perception_data):
        if self.state is 'init':
            self.set_neck_angle_topic.publish(Vector3(0, 0, 0))
            if perception_data.device is 'VOICE':
                if 'introduce yourself' in perception_data.input:
                    self.change_state_with_subtask('introduce', 'Introduce')
                    self.action('normal')

        elif self.state is 'introduce':
            if perception_data.device is 'VOICE':
                if 'crack' in perception_data.input and 'egg' in perception_data.input:
                    self.set_neck_angle_topic.publish(Vector3(0, 0.3, 0))
                    self.subtaskBook.get_subtask(self, 'Say').say('I will crack this egg')
                    # publish code for crack the egg
                    self.action('crack')
                    self.change_state('finish')
            # Don't forget to add task to task_book