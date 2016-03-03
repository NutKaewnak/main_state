from include.abstract_task import AbstractTask
import rospy
__author__ = 'nicole'


class Test(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.pick = None
        self.object_goal = None

    def perform(self, perception_data):
        if self.state is 'init':
            rospy.loginfo('---in test---')
            self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
            self.subtask.turn(-0.4, 0)
            self.change_state('find_object')

        elif self.state is 'find_object':
            self.subtask = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
            self.subtask.start()
            self.change_state('wait_for_object')

        elif self.state is 'wait_for_object':
            if self.subtask.state is 'finish':
                self.object_goal = self.subtask.objects[0].point
                self.change_state('pick')

        elif self.state is 'pick':
            self.pick = self.subtaskBook.get_subtask(self, 'Pick')
            self.pick.side_arm = 'right_arm'
            self.pick.pick_object(self.object_goal)
            self.change_state('wait_for_pick')

        elif self.state is 'wait_for_pick':
            if self.pick.state is 'finish':
                self.change_state('finish')
