from include.abstract_task import AbstractTask
import rospy
__author__ = 'nicole'


class Test(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.pick = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('---in test---')
            self.subtask = self.subtaskBook.get_subtask(self, 'Pick')
            self.subtask.pick_object('right_arm')
            self.change_state('finish')
