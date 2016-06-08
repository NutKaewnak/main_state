import rospy
from include.abstract_task import AbstractTask

__author__ = 'Nicole'


class TestObjectRecogAndManip(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.pick = None
        self.recognize_objects = None
        self.point_to_pick = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.pick = self.subtaskBook.get_subtask(self, 'Pick')
            self.change_state('wait_for_object')
            rospy.loginfo('test object manip init')

        elif self.state is 'wait_for_object':
            self.recognize_objects = self.subtaskBook.get_subtask(self, 'RecognizeObjects')
            self.recognize_objects.start('coke')
            self.
            
            self.point_to_pick = perception_data.input.centriods[0]
            rospy.loginfo('found object at ' + str(self.point_to_pick))
            self.change_state('found_object')

        elif self.state is 'found_object':
            self.subtask.pick_object([self.point_to_pick.x, self.point_to_pick.y, self.point_to_pick.z])
            self.change_state('picking_object')

        elif self.state is 'picking_object':
            if self.subtask.state is 'finish':
                self.change_state('finish')
