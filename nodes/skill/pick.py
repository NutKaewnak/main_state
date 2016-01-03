import rospy
from include.abstract_skill import AbstractSkill
from include.arm_status import ArmStatus
from include.delay import Delay

__author__ = 'Nicole'


class Pick(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.manipulator = None
        self.gripper = None
        self.side = 'right'
        self.delay = Delay()
        self.goal_name = None
        self.goal_pose = None
        self.device = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.manipulator = self.controlModule.manipulator
            self.gripper = self.controlModule.gripper
            self.change_state('waiting_for_goal')

        elif self.state is 'prepare_to_pick':
            self.manipulator.static_pose(self.side + '_arm', self.side + '_normal')  # may change
            self.change_state('arm_normal')

        elif self.state is 'arm_normal':
            self.make_device()

            if self.device is not None and perception_data.device is self.device:
                state = ArmStatus.get_state_from_status(perception_data.input)
                if state is 'succeeded':
                    self.change_state('prepare_move_hand_to_front_of_object')

        elif self.state is 'prepare_move_hand_to_front_of_object':
            self.manipulator.pickobject_pregrasp(self.side + '_arm', self.goal_name, self.goal_pose)
            self.delay.wait(15)
            self.change_state('move_to_in_front_of_object')

        elif self.state is 'move_to_in_front_of_object':
            if self.device is not None and perception_data.device is self.device:
                state = ArmStatus.get_state_from_status(perception_data.input)
                if state is 'succeeded':
                    self.change_state('prepare_to_open_gripper')
                elif not self.delay.is_waiting():
                    rospy.logwarn('move_to_in_front_of_object out of time!')
                    self.change_state('prepare_move_hand_to_front_of_object')

        elif self.state is 'prepare_to_open_gripper':
            self.manipulator.pickobject_opengripper()
            self.change_state('open_gripper')

        elif self.state is 'open_gripper':
            if self.device is not None and perception_data.device is self.device:
                state = ArmStatus.get_state_from_status(perception_data.input)
                self.delay.wait(15)
                if state is 'succeeded':
                    self.change_state('prepare_move_to_object')
                elif not self.delay.is_waiting():
                    rospy.logwarn('open_gripper out of time!')
                    self.change_state('prepare_to_open_gripper')

        elif self.state is 'prepare_move_to_object':
            # problem here
            self.manipulator.pickobject_reach()
            self.delay.wait(25)
            self.change_state('move_to_object')

        elif self.state is 'move_to_object':
            if not self.delay.is_waiting():  # and device state is succeeded
                if self.device is not None and perception_data.device is self.device:
                    state = ArmStatus.get_state_from_status(perception_data.input)
                    if state is 'succeeded':
                        self.change_state('grab_object')

        elif self.state is 'grab_object':
            # close gripper
            self.gripper.gripper_close()
            self.change_state('succeeded')

    def pick_object(self, goal_pose, goal_name='unknown'):
        self.change_state('init')
        self.goal_name = goal_name
        self.goal_pose = goal_pose
        self.controlModule.manipulator.manipulate('right_arm', self.goal_pose)
        self.change_state('prepare_to_pick')

    def set_side(self, side):
        self.side = side

    def make_device(self):
        if self.side is 'right':
            self.device = 'RIGHT_ARM'
        elif self.side is 'left':
            self.device = 'LEFT_ARM'
