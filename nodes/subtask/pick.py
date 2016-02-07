__author__ = 'CinDy'


import rospy
from include.abstract_subtask import AbstractSubtask


class Pick(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'Pick')
        self.input_object_pos = None
        self.side_arm = 'right_arm'
        self.move_base = None
        self.check = None


    def perform(self, perception_data):
        if self.state is 'setting_arm':
            self.skill.pick_object(self.side_arm)
            print 'current state in subtask = ' + self.state +'********************'
            self.change_state('wait_skill_for_open_gripper')

        elif self.state is 'wait_skill_for_open_gripper':
            print '***************wait_skill_for_open_gripper: in subtask********************'
            print 'current state in subtask = ' + self.state +'********************'
            if self.skill.state is 'moving':
                rospy.loginfo('********moving:subtask************')
                # self.set_subtask_book()
                self.move_base = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.move_base.set_position(0.5, 0, 0)
                self.skill.after_mani()
            elif self.skill.state is 'checking':
                rospy.loginfo('********checking:subtask************')
                self.check = self.skillBook.get_subtask(self, 'DetectObject3Ds')
                self.check.detect()
                self.skill.object_pos = self.check.object
                self.skill.after_mani()
            elif self.skill.state is 'succeed':
                self.change_state('finish')
        #     self.change_state('receive_object')
        #
        # elif self.state is 'receive_object':
        #     if self.skill.state is 'succeed':
        #         self.change_state('finish')

    def pick_object(self, side):
        rospy.loginfo('------in pick_object:subtask------')
        # self.input_object_pos = goal
        self.side_arm = side
        self.change_state('setting_arm')
