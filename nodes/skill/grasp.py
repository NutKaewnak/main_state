import rospy
from include.abstract_skill import AbstractSkill
from include.inverse_kinematics import InverseKinematics
from include.arm_status import ArmStatus
from include.set_torque_limit import set_torque_limit

__author__ = 'nuok'


class Grasp(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.manipulator = control_module.manipulator
        self.kinematic = InverseKinematics()
        self.gripper = control_module.gripper
        self.goal_point = None
        self.side = None
        self.move_base = None
        self.arm_device = None
        self.gripper_device = None

    def perform(self, perception_data):
        if self.state is 'init_pick':
            self.manipulator.init_controller()
            self.set_arm_normal()
            self.change_state('arm_normal')

        elif self.state is 'arm_normal':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    # TODO: fix side
                    self.manipulator.static_pose('right_init_picking_normal')
                    self.change_state('prepare_pick')

        elif self.state is 'prepare_pick':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    # TODO: fix side
                    self.manipulator.static_pose('right_picking_prepare')
                    self.change_state('open_gripper')

        elif self.state is 'open_gripper':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded':
                    # TODO: fix side
                    gripper_opened = 0.8
                    self.manipulator.move_joint("right_gripper_joint", gripper_opened)
                    self.change_state('wait_open_gripper')

        elif self.state is 'wait_open_gripper':
            if perception_data.device == self.gripper_device:
                # TODO: may bug
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded':
                    self.change_state('done_prepare')

        # wait for subtask signal to continue on grasp

        elif self.state is 'init_pos':
            print self.goal_point
            if self.goal_point is not None:
                self.kinematic.init_position(self.goal_point)
                self.change_state('prepare_object')

        elif self.state is 'prepare_object':
            self.manipulator.move_arm_group(self.kinematic.pick_prepare())
            self.change_state('pregrasp')

        elif self.state is 'pregrasp':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    self.manipulator.move_arm_group(self.kinematic.inverse_kinematics_pregrasp())
                    self.change_state('grab_object')

        elif self.state is 'grab_object':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # close gripper
                    set_torque_limit()
                    # TODO: fix side
                    self.manipulator.static_pose('right_gripper_close')
                    self.change_state('after_grasp')

        elif self.state is 'after_grasp':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # TODO: fix side
                    self.manipulator.static_pose('right_picking_prepare')
                    self.change_state('wait_succeeded')

        elif self.state is 'wait_succeeded':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # TODO: fix side
                    self.manipulator.pick_object_finish('right_normal')
                    rospy.loginfo('--after_grasp--')
                    print '---current state = ' + self.state + '---'
                    self.change_state('succeeded')
                    print '---next state = ' + self.state + '---'

        elif self.state is 'succeeded':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    self.change_state('succeeded')

    def pick_object(self, point):
        """
        Let skill control manipulation to pick object at design point.
        Please make sure to set desire arm side (Default: 'right_arm').
        :param point: (geometry/Point) goal of the object
        :return: None
        """
        self.goal_point = point
        rospy.loginfo('----pick_object:skill---')
        self.change_state('init_pick')

    def set_side(self, side):
        self.side = side
        if self.side is 'right_arm':
            self.arm_device = 'RIGHT_ARM'
            self.gripper_device = 'RIGHT_GRIPPER'
        elif self.side is 'left_arm':
            self.arm_device = 'LEFT_ARM'
            self.gripper_device = 'LEFT_GRIPPER'
        self.kinematic.arm_group = side

    def set_arm_normal(self):
        if self.side is 'right_arm':
            self.manipulator.static_pose('right_normal')
        elif self.side is 'left_arm':
            self.manipulator.static_pose('left_normal')

    def after_prepare(self):
        self.change_state('init_pos')

    def open_gripper(self):
        self.manipulator.pickobject_opengripper()

    def close_gripper(self):
        self.manipulator.pickobject_closegripper()
