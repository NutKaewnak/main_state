import rospy
from geometry_msgs.msg import PoseStamped
from include.abstract_skill import AbstractSkill
from include.arm_status import ArmStatus
from include.delay import Delay

__author__ = 'nuok'


class Grasp(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.right_arm = control_module.right_arm
        self.gripper = control_module.right_gripper
        self.side = None
        self.arm_device = None
        self.gripper_device = None

        self.object_pose = PoseStamped()
        self.object_name = ""

        self.is_init = False
        self.is_done_init = False
        self.state_to_print = ""
        self.timer = Delay()

        self.result = 0

    def perform(self, perception_data):
        if self.state_to_print != self.state:
            self.state_to_print = self.state
            print self.state_to_print

        if self.state is 'init':
            self.object_pose = None
            self.object_name = ""
            self.gripper_close()
            if not self.is_init:
                self.is_init = True
                if not self.is_done_init:
                    self.right_arm.init_controller()
                    self.is_done_init = True
                    self.change_state('wait_for_point')

        elif self.state is 'prepare_arm_normal':
            if self.side is 'right_arm':
                self.right_arm.static_pose('right_normal')
            elif self.side is 'left_arm':
                self.right_arm.static_pose('left_normal')
            self.change_state('arm_normal')

        elif self.state is 'arm_normal':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    # TODO: fix side
                    self.change_state('done_prepare')

        elif self.state is 'receive_pick_object':
            self.gripper_open()
            if self.side is 'right_arm':
                self.right_arm.static_pose('right_pregrasp')
            elif self.side is 'left_arm':
                self.right_arm.static_pose('left_pregrasp')
            self.change_state('open_gripper')

        elif self.state is 'open_gripper':
            if perception_data.device == self.gripper_device:
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # TODO: fix side
                    self.change_state('pick_object')

        elif self.state is 'pick_object':
            if self.object_pose is None:
                rospy.logerr('No object_pose to pick')
                self.change_state('rejected')
                return
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    self.result = self.right_arm.pick(self.object_pose, self.object_name)
                    self.change_state('wait_succeeded')

        elif self.state is 'wait_succeeded':
            if self.result == -1:
                self.change_state('unreachable')
                return

            if perception_data.device == self.arm_device:
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # TODO: fix side
                    self.gripper_close()
                    self.right_arm.static_pose('right_normal')
                    rospy.loginfo('--after_grasp--')
                    print '---current state = ' + self.state + '---'
                    self.change_state('succeeded')
                    print '---next state = ' + self.state + '---'

        elif self.state is 'succeeded':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    self.change_state('succeeded')

    def pick_object(self, pose_stamped, object_name='big_dick'):
        """
        Let skill control manipulation to pick object at design point.
        :param object_name: (str)
        :param pose_stamped: (PoseStamped) goal of the object
        :return: None
        """
        self.object_pose = pose_stamped
        self.object_name = object_name
        rospy.loginfo('----pick_object:grasp_skill---')
        self.change_state('receive_pick_object')

    def set_side(self, side='right_arm'):
        self.side = side
        if self.side is 'right_arm':
            self.arm_device = 'RIGHT_ARM'
            self.gripper_device = 'RIGHT_GRIPPER'
        elif self.side is 'left_arm':
            self.arm_device = 'LEFT_ARM'
            self.gripper_device = 'LEFT_GRIPPER'

    def after_prepare(self):
        self.change_state('receive_pick_object')

    def gripper_open(self):
        self.gripper.gripper_open()

    def gripper_close(self):
        self.gripper.gripper_close()
