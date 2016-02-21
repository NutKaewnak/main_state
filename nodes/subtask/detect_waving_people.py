import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class DetectWavingPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.gesture_pos = None
        self.skill = self.current_skill
        self.subtask = self.current_subtask

    def perform(self, perception_data):
        if self.state is 'init':
            self.gesture_pos = None
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.skill.turn(-0.2, 0)
            self.change_state('searching')

        elif self.state is 'searching':
            if perception_data.device is self.Devices.GESTURE:
                self.gesture_pos = perception_data.input
                self.change_state('finish')

    def start(self):
        self.gesture_pos = None
        self.change_state('init')

    def get_point(self):
        return self.gesture_pos
