__author__ = 'Nicole'
import rospy
from include.abstract_task import AbstractTask


class TestObjectRecogAndManip(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.point_to_pick = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'PickFromPoint')
            self.change_state('wait_for_object')

        elif self.state is 'wait_for_object':
            if perception_data.device is 'OBJECT':
                self.point_to_pick = perception_data.input.centroid
                rospy.loginfo('found object at ' + self.point_to_pick)
                self.change_state('found_object')

        elif self.state is 'found_object':
            self.subtask.pick_point(self.point_to_pick)
            self.change_state('picking_object')

        elif self.state is 'picking_object':
            if self.subtask.state is 'finish':
                self.change_state('finish')