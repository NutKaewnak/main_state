import rospy
from include.abstract_subtask import AbstractSubtask
from include.pick_available_range import is_in_right_range,is_in_left_range, find_right_arm_available_point, find_left_arm_available_point

__author__ = 'CinDy'

LEFT_ARM_MINIMUM = 0.21

class Pick(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.grasp = None
        self.input_object_pose = None
        self.side_arm = None
        self.neck = None
        self.base = None
        self.object_name = None
        self.is_tried_to_solve = False

    def perform(self, perception_data):
        if self.state is 'init':
            # rospy.loginfo('pick subtask init')
            self.is_tried_to_solve = True
            self.grasp = self.skillBook.get_skill(self, 'Grasp')
            self.change_state('wait_for_skill_init')

        elif self.state is 'wait_for_skill_init':
            if self.grasp.state is 'wait_for_point':
                self.change_state('wait_for_point')

        elif self.state is 'receive_point':
            self.grasp = self.skillBook.get_skill(self, 'Grasp')
            self.grasp.set_side(self.side_arm)
            self.change_state('setting_arm')

        elif self.state is 'setting_arm':
            self.grasp.pick_object(self.input_object_pose)
            self.change_state('wait_for_skill')

        elif self.state is 'wait_for_skill':
            if self.grasp.state is 'done_prepare':
                self.grasp.after_prepare()
            elif self.grasp.state is 'unreachable':
                if not self.is_tried_to_solve:
                    self.is_tried_to_solve = True
                    self.change_state('solve_unreachable')
                else:
                    self.change_state('error')
            elif self.grasp.state is 'succeeded':
                self.change_state('finish')

        elif self.state is 'solve_unreachable':
            if self.side_arm is 'right_arm':
                if not is_in_right_range(self.input_object_pose.pose.position):
                    new_point = find_right_arm_available_point(self.input_object_pose.pose.position)
                    self.base = self.skillBook.get_skill(self, 'MoveBaseRelativeTwist')
                    self.base.set_position(self.input_object_pose.pose.position.x - new_point.x,
                                           self.input_object_pose.pose.position.y - new_point.y,
                                           0
                                           )
                    self.input_object_pose.pose.position = new_point
                    self.change_state('wait_for_twist')
            elif self.side_arm is 'left_arm':
                if not is_in_left_range(self.input_object_pose.pose.position):
                    new_point = find_left_arm_available_point(self.input_object_pose.pose.position)
                    self.base = self.skillBook.get_skill(self, 'MoveBaseRelativeTwist')
                    self.base.set_position(self.input_object_pose.pose.position.x - new_point.x,
                                           self.input_object_pose.pose.position.y - new_point.y,
                                           0
                                           )
                    self.input_object_pose.pose.position = new_point
                    self.change_state('wait_for_twist')

        elif self.state is 'wait_for_twist':
            if self.base.state == 'succeeded':
                self.pick_object(self.input_object_pose, self.object_name)

    def pick_object(self, pose_stamped, object_name='little_big'):
        """
        Let subtask pick object. Please make sure that side arm is already design (Default: 'right_arm').
        :param pose_stamped: (PoseStamped) point of object to pick.
        :param object_name:
        :return: None
        """
        self.input_object_pose = pose_stamped
        self.object_name = object_name
        if self.side_arm is None:
            if input_object_pose.y > LEFT_ARM_MINIMUM :
                self.side_arm = 'left_arm'
            else :
                self.side_arm = 'right_arm'
        self.change_state('receive_point')

    def gripper_open(self):
        self.grasp.gripper_open()

    def gripper_close(self):
        self.grasp.gripper_close()
