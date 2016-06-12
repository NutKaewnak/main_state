import rospy
from geometry_msgs.msg import PoseStamped
from include.abstract_task import AbstractTask

__author__ = 'nicole'


class Test(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.pick = None
        self.object_goal = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'TestSubtaskSkill')
            self.change_state('wait_for_subtask')

        elif self.state is 'wait_for_subtask':
            if self.subtask.state is 'finish':
                self.change_state('finish')
