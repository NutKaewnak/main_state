__author__ = 'CinDy'

import rospy
from include.abstract_subtask import AbstractSubtask


class Pick(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'Pick')
        self.input_object_pos = None
        self.side_arm = 'right'
        self.move_base = None

    def perform(self, perception_data):
        if self.state is 'setting_arm':
            self.skill.pick_object(self.side_arm)
            self.change_state('wait_skill_for_open_gripper')

        elif self.state is 'wait_skill_for_open_gripper':
            if self.skill.state is 'open_gripper':
                self.move_base = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.move_base.set_position(0.5, 0, 0)
            self.change_state('receive_object')

        elif self.state is 'receive_object':
            self.skill.after_move()
            if self.skill.state is 'succeed':
                self.change_state('finish')

    def pick_object(self, side):
        rospy.loginfo('------in pick_object:subtask--')
        # self.input_object_pos = goal
        self.side_arm = side
        self.change_state('setting_arm')
