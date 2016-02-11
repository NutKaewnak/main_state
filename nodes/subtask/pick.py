import rospy
from include.abstract_subtask import AbstractSubtask

__author__ = 'CinDy'


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
            print '*******current state in subtask = ' + self.state + '********'
            self.change_state('move_base')

        elif self.state is 'move_base':
            # print '***************wait_skill_for_open_gripper: in subtask********************'
            # print 'current state in subtask = ' + self.state +'********************'
            if self.skill.state is 'moving':
                rospy.loginfo('******moving:subtask******')
                # self.set_subtask_book()
                self.move_base = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.move_base.set_position(0.8, 0, 0)
                self.change_state('after_move')

        elif self.state is 'after_move':
            # rospy.loginfo('******after_move:subtask******')
            if self.move_base.state is 'finish':
                rospy.loginfo('******finish_move:subtask******')
                self.skill.after_mani()
                self.change_state('detect_object')
            elif self.move_base.state is 'move':
                rospy.loginfo('******move:move_relative*******')

        elif self.state is 'detect_object':
            rospy.loginfo('******detect_object:subtask******')
            if self.skill.state is 'checking':
                rospy.loginfo('******checking:subtask******')
                self.check = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
                self.check.start()
                self.change_state('after_detect')

        elif self.state is 'after_detect':
            rospy.loginfo('******after_detect:subtask******')
            if self.check.state is 'finish':
                rospy.loginfo('******finish_detect:subtask******')
                self.skill.object_pos = self.check.objects
                self.skill.after_mani()
                self.change_state('grasp_object')

        elif self.state is 'grasp_object':
            rospy.loginfo('******grasp_object:subtask******')
            if self.skill.state is 'succeed':
                self.change_state('finish')

                #     self.change_state('receive_object')
                # elif self.state is 'receive_object':
                #     if self.skill.state is 'succeed':
                #         self.change_state('finish')

    def pick_object(self, side):
        rospy.loginfo('------in pick_object:subtask------')
        # self.input_object_pos = goal
        self.side_arm = side
        self.change_state('setting_arm')
