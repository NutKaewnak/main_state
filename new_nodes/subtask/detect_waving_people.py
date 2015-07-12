__author__ = 'nicole'
import rospy
from include.abstract_subtask import AbstractSubtask


class DetectWavingPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.gesture_pos = None
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        # if self.state is not 'succeeded':
        #     rospy.loginfo('DetectPeopleWithGesture : '+self.state)
        if self.state is 'init':
            self.gesture_pos = None
            self.change_state('searching')

        elif self.state is 'searching':
            if perception_data.device is self.Devices.GESTURE:
                rospy.loginfo(type(perception_data.input))
                self.gesture_pos = perception_data.input
                self.change_state('finish')

    def start(self):
        self.gesture_pos = None
        self.change_state('init')

    def get_point(self):
        return self.gesture_pos