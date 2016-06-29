from include.abstract_task import AbstractTask

__author__ = 'nicole'


class TestBugArm(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
            self.subtask.static_pose('right_push_chair_push')
            self.change_state('send_pose')
