import rospy
from include.abstract_skill import AbstractSkill
from include.arm_status import ArmStatus
from include.delay import Delay
from std_msgs.msg import Float64
from dynamixel_controllers.srv import SetTorqueLimit
from controller.manipulator_controller import ManipulateController
__author__ = 'CinDy'


def set_torque_limit(limit=0.5):
    rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
    try:
        rospy.loginfo('settorque')
        setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
        respTorque = setTorque(limit)
    except rospy.ServiceException, e:
        rospy.logwarn("Service Torque call failed " + str(e))


class Pick(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.manipulator = control_module.manipulator
        self.side = 'right_arm'
        self.delay = Delay()
        self.goal_name = None
        self.goal_pose = None
        self.device = None
        self.pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)
        self.pub_right_wrist_2 = rospy.Publisher('/dynamixel/right_wrist_2_controller/command', Float64)
        self.pub_left_gripper = rospy.Publisher('/dynamixel/left_gripper_joint_controller/command', Float64)
        self.pub_left_wrist_2 = rospy.Publisher('/dynamixel/left_wrist_2_controller/command', Float64)

    def perform(self, perception_data):
        if self.state is 'init':
            # self.manipulator.init_controller()
            # self.gripper = self.controlModule.gripper
            self.change_state('arm_normal')

        elif self.state is 'arm_normal':
            self.manipulator.pickobject_init(self.side, 'object', [0.693 - 0.07, -0.170 + 0.09, 0.7 + 0.2])
            rospy.loginfo('--arm_normal--')
            self.change_state('prepare_to_pick')

        elif self.state is 'prepare_to_pick':
            self.manipulator.pickobject_prepare()
            rospy.loginfo('--prepare_to_pick--')
            # self.make_device()
            #
            # if self.device is not None and perception_data.device is self.device:
            #     state = ArmStatus.get_state_from_status(perception_data.input)
            #     if state is 'succeeded':
            self.change_state('prepare_to_open_gripper')

        elif self.state is 'prepare_to_open_gripper':
            if self.side is 'right_arm':
                self.pub_right_gripper.publish(1.1)
            elif self.side is 'left_arm':
                self.pub_left_gripper.publish(1.1)
            rospy.loginfo('--prepare_to_open_gripper--')
            #   self.manipulator.pickobject_opengripper()
            self.change_state('open_gripper')

        elif self.state is 'open_gripper':
            if self.device is not None and perception_data.device is self.device:
                state = ArmStatus.get_state_from_status(perception_data.input)
                self.delay.wait(15)
                rospy.loginfo('--open_gripper--')
                if state is 'succeeded':
                    self.change_state('wait_for_subtask')
                    # waiting for move absolute in subtask
                elif not self.delay.is_waiting():
                    rospy.logwarn('open_gripper out of time!')
                    self.change_state('prepare_to_open_gripper')

        elif self.state is 'prepare_pregrasp':
            self.manipulator.pickobject_pregrasp()
            rospy.loginfo('--prepare_pregrasp--')
            # self.delay.wait(15)
            self.change_state('pregrasp')

        elif self.state is 'pregrasp':
            rospy.loginfo('--pregrasp--')
            if self.device is not None and perception_data.device is self.device:
                state = ArmStatus.get_state_from_status(perception_data.input)
                if state is 'succeeded':
                    self.change_state('prepare_move_to_object_front')
                elif not self.delay.is_waiting():
                    rospy.logwarn('pregrasp out of time!')
                    self.change_state('prepare_pregrasp')

        elif self.state is 'prepare_move_to_object_front':
            self.manipulator.pickobject_movetoobjectfront_1()
            self.manipulator.pickobject_movetoobjectfront_2()
            self.manipulator.pickobject_movetoobjectfront_3()
            # self.delay.wait(25)
            rospy.loginfo('--prepare_move_to_object_front--')
            self.change_state('move_to_object')

        elif self.state is 'move_to_object':
            rospy.loginfo('--move_to_object--')
            if not self.delay.is_waiting():  # and device state is succeeded
                if self.device is not None and perception_data.device is self.device:
                    state = ArmStatus.get_state_from_status(perception_data.input)
                    if state is 'succeeded':
                        self.change_state('grab_object')

        elif self.state is 'grab_object':
            # close gripper
            # self.manipulator.pickobject_grasp()
            set_torque_limit()
            rospy.loginfo('--grab_object--')
            if self.side is 'right_arm':
                self.pub_right_gripper.publish(0.3)
                self.pub_right_wrist_2.publish(0.0)
            elif self.side is 'left_arm':
                self.pub_left_gripper.publish(0.3)
                self.pub_left_wrist_2.publish(0.0)
            # self.gripper.gripper_close()
            self.change_state('after_grasp')

        elif self.state is 'after_grasp':
            # self.manipulator.pickobject_after_grasp()
            rospy.loginfo('--after_grasp--')
            self.manipulator.pickobject_prepare()
            self.change_state('succeed')

        elif self.state is 'succeed':
            self.manipulator.finish()

    def pick_object(self, side, goal_name='unknown'):
        # self.goal_name = goal_name
        # self.goal_pose = goal_pose
        rospy.loginfo('----pick_object:skill---')
        self.set_side(side)
        # self.controlModule.manipulator.manipulate(side + '_arm', self.goal_pose)
        self.change_state('init')

    def set_side(self, side):
        self.side = side

    def make_device(self):
        if self.side is 'right_arm':
            self.device = 'RIGHT_ARM'
        elif self.side is 'left_arm':
            self.device = 'LEFT_ARM'

    def after_move(self):
        self.change_state('prepare_pregrasp')