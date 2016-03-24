import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class ArmStaticPose(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None

    def perform(self, perception_data):
        if self.state is 'receive_command':
            if self.skill.state is 'succeeded':
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                self.change_state('aborted')

    def static_pose(self, pose):
        rospy.loginfo('set arm pose to ' + pose)
        self.skill = self.skillBook.get_skill(self, 'ArmStaticPose')
        self.skill.static_pose(pose)
        self.change_state('receive_command')
