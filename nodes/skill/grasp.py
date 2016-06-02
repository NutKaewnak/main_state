import rospy
from include.abstract_skill import AbstractSkill
from include import inverse_kinematics
from include.arm_status import ArmStatus
from include.set_torque_limit import set_torque_limit

__author__ = 'nuok'


class Grasp(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.kinematic = inverse_kinematics.InverseKinematics()
        self.right_arm = control_module.right_arm
        self.gripper = control_module.right_gripper
        self.goal_point = None
        self.side = None
        self.move_base = None
        self.arm_device = None
        self.gripper_device = None
        self.is_init = False
        self.is_done_init = False
        self.state_to_print = ""

    def perform(self, perception_data):
        if self.state_to_print != self.state:
            self.state_to_print = self.state
            print self.state_to_print

        if self.state is 'init':
            if not self.is_init:
                self.is_init = True
                if not self.is_done_init:
                    self.right_arm.init_controller()
                    self.is_done_init = True
                    print 'done init right side'
                    self.change_state('wait_for_point')

        elif self.state is 'prepare_arm_normal':
            print "self.side:", self.side
            if self.side is 'right_arm':
                self.right_arm.static_pose('right_normal')
            elif self.side is 'left_arm':
                self.right_arm.static_pose('left_normal')
            # edit pass arm_normal state
            self.change_state('arm_normal')
            # self.change_state('prepare_pick')

        elif self.state is 'arm_normal':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                print arm_status, "--------------------"
                if arm_status == 'succeeded' or arm_status == "preempted":
                    # TODO: fix side
                    self.right_arm.static_pose('right_init_picking_normal')
                    self.change_state('prepare_pick')

        elif self.state is 'prepare_pick':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    # TODO: fix side
                    self.right_arm.static_pose('right_picking_prepare')
                    self.change_state('init_pos')

        elif self.state is 'init_pos':
            print 'goal_point', self.goal_point
            if self.goal_point is not None:
                self.goal_point.y += 0.00
                self.goal_point.z -= 0.00
                self.right_arm.init_position(self.goal_point)
                self.change_state('open_gripper')

        elif self.state is 'open_gripper':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded':
                    # TODO: fix side
                    self.gripper.gripper_open()
                    self.change_state('wait_open_gripper')

        elif self.state is 'wait_open_gripper':
            if perception_data.device == self.gripper_device:
                # TODO: may bug
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                print 'arm status', arm_status
                if arm_status == 'succeeded':
                    # cannot use invk yet
                    # self.change_state('done_prepare')
                    self.change_state('done')

        elif self.state is 'first_pick':
            self.right_arm.move_arm_pick_object_first()
            self.change_state('wait_for_first_pick')

        elif self.state is 'wait_for_first_pick':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    # TODO: fix side
                    self.right_arm.move_arm_pick_object_second()
                    self.change_state('wait_for_second_pick')

        elif self.state is 'wait_for_second_pick':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    # TODO: fix side
                    gripper_closed = 0.0
                    self.gripper.move_joint("right_gripper_joint", gripper_closed)
                    self.change_state('wait_for_close_gripper')

        elif self.state is 'wait_for_close_gripper':
            # print self.gripper_device
            # print perception_data.device == self.gripper_device
            if perception_data.device == self.gripper_device:
                # TODO: may bug
                gripper_status = ArmStatus.get_state_from_status(perception_data.input)
                if gripper_status == 'succeeded':
                    self.right_arm.static_pose('right_picking_prepare')
                    self.change_state('wait_for_pick_up')

        elif self.state is 'wait_for_pick_up':
            if perception_data.device == self.arm_device:
                arm_status = ArmStatus.get_state_from_status(perception_data.input)
                if arm_status == 'succeeded' or arm_status == "preempted":
                    self.change_state('succeeded')

        elif self.state is 'prepare_object':
            angles = inverse_kinematics.inverse_kinematic(self.kinematic.pick_prepare())
            print angles
            for x in angles:
                inverse_kinematics.in_bound(x, angles[x])
            print angles
            self.right_arm.move_arm_group(angles)
            self.change_state('pregrasp')

        elif self.state is 'pregrasp':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    angles = inverse_kinematics.inverse_kinematic(self.kinematic.point_inverse_kinematics_pregrasp())
                    self.right_arm.move_arm_group(angles)
                    self.change_state('grab_object')

        elif self.state is 'grab_object':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # close gripper
                    set_torque_limit()
                    # TODO: fix side
                    self.right_arm.static_pose('right_gripper_close')
                    self.change_state('after_grasp')

        elif self.state is 'after_grasp':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # TODO: fix side
                    self.right_arm.static_pose('right_picking_prepare')
                    self.change_state('wait_succeeded')

        elif self.state is 'wait_succeeded':
            if perception_data.device == self.arm_device:
                print ArmStatus.get_state_from_status(perception_data.input)
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # TODO: fix side
                    self.right_arm.pick_object_finish('right_normal')
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
        :param point: (geometry_msgs.msg.Point) goal of the object
        :return: None
        """
        self.goal_point = point
        rospy.loginfo('----pick_object:skill---')
        self.change_state('prepare_arm_normal')

    def set_side(self, side):
        self.side = side
        if self.side is 'right_arm':
            self.arm_device = 'RIGHT_ARM'
            self.gripper_device = 'RIGHT_GRIPPER'
        elif self.side is 'left_arm':
            self.arm_device = 'LEFT_ARM'
            self.gripper_device = 'LEFT_GRIPPER'
        self.kinematic.arm_group = side

    def after_prepare(self):
        self.change_state('first_pick')

    def open_gripper(self):
        self.gripper.gripper_open()

    def close_gripper(self):
        self.gripper.gripper_close()
