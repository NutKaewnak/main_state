import rospy
from include.abstract_skill import AbstractSkill
from include.arm_status import ArmStatus
from include.delay import Delay
from include.set_torque_limit import set_torque_limit
from std_msgs.msg import Float64

__author__ = 'CinDy'


class Pick(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        self.manipulator = control_module.manipulator
        self.object_pos = [0.634993 - 0.05, -0.135707 + 0.11, 0.592334 + 0.05]
        self.side = 'right_arm'
        self.move_base = None
        self.delay = Delay()
        self.goal_name = None
        self.goal_pose = None
        self.device = None

        self.pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)
        self.pub_right_wrist_2 = rospy.Publisher('/dynamixel/right_wrist_2_controller/command', Float64)
        self.pub_right_wrist_3 = rospy.Publisher('/dynamixel/right_wrist_3_controller/command', Float64)
        self.pub_tilt = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        self.pub_pan = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        self.pub_prismatic = rospy.Publisher('/dynamixel/prismatic_controller/command', Float64)

        self.pub_left_gripper = rospy.Publisher('/dynamixel/left_gripper_joint_controller/command', Float64)
        self.pub_left_wrist_2 = rospy.Publisher('/dynamixel/left_wrist_2_controller/command', Float64)
        self.pub_left_wrist_3 = rospy.Publisher('/dynamixel/left_wrist_3_controller/command', Float64)

    def perform(self, perception_data):
        if self.state is 'init_pick':
            self.manipulator.init_controller()
            self.set_static_pos()
            self.change_state('wait_arm_normal')

        elif self.state is 'wait_arm_normal':
            if perception_data.device == 'RIGHT_ARM':
                if ArmStatus.get_state_from_status(perception_data.input) == 'succeeded':
                    # self.gripper s= self.controlModule.gripper
                    self.change_state('arm_normal')

        # TODO: publish pan and tilt shouldn't be here. FIX IT!!
        elif self.state is 'arm_normal':
            rospy.loginfo('---arm_normal---')
            self.manipulator.pick_object_init(self.side, 'object', [0, 0, 0])
            self.delay.wait(3000)
            self.pub_pan.publish(0.0)
            self.pub_tilt.publish(-0.3)
            self.pub_prismatic.publish(0+0.23)
            print '---current state = ' + self.state + '---'
            self.change_state('prepare_pick')
            print '----next state = ' + self.state + '----'
            # rospy.loginfo("Press any key to Continue1..1")
            # raw_input()

        elif self.state is 'prepare_pick':
            rospy.loginfo('---prepare_to_pick---')
            self.manipulator.pickobject_prepare()
            self.delay.wait(3000)
            print '---current state = ' + self.state + '---'
            # self.make_device()
            #
            # if self.device is not None and perception_data.device is self.device:
            #     state = ArmStatus.get_state_from_status(perception_data.input)
            #     if state is 'succeeded':
            self.change_state('open_gripper')
            print '---next state = ' + self.state + '---'
            rospy.loginfo("Press any key to Continue2")
            # raw_input()

        elif self.state is 'open_gripper':
            rospy.loginfo('---open_gripper---')
            self.move_gripper(0.5)
            # if self.side is 'right_arm':
            #     self.pub_right_gripper.publish(1.1)
            # elif self.side is 'left_arm':
            #     self.pub_left_gripper.publish(1.1)
            print '---current state = ' + self.state+'---'
            self.delay.wait(3000)
            # self.manipulator.pickobject_opengripper()
            self.change_state('moving')
            print '---next state = ' + self.state + '---'
            rospy.loginfo("Press any key to Continue3")

        # elif self.state is 'open_gripper':
        #     rospy.loginfo('--open_gripper--')
        #     if self.device is not None and perception_data.device is self.device:
        #         state = ArmStatus.get_state_from_status(perception_data.input)
        #         self.delay.wait(5000)
        #         rospy.loginfo('--open_gripper--')
        #         print 'current state = ' + self.state
        #         rospy.loginfo("Press any key to Continue5")
        #         raw_input()
        #         if state is 'succeeded':
        #             self.change_state('wait_for_subtask_move')
        #             # waiting for move absolute in subtask
        #         elif not self.delay.is_waiting():
        #             rospy.logwarn('open_gripper out of time!')
        #             self.change_state('prepare_open_gripper')
        #     self.change_state('moving')
        #     print "current state = " + self.state + "1------------------------------"
        #     rospy.loginfo("Press any key to Continue6")
        #     raw_input()

        # elif self.state is 'moving':
        #     rospy.loginfo("-----------------in moving :skill------------------------")
        #     self.move_base = self.skillBook.get_skill(self, 'MoveRelative')
        #     self.move_base.set_position(0.5, 0, 0)
        #     self.delay.wait(3000)
        #     print 'current state = ' + self.state+'---------------------------------'
        #     rospy.loginfo("Press any key to Continue7")
        #     raw_input()
        #     self.change_state('prepare_pregrasp')
        #     print 'current state = ' + self.state+'1--------------------------------'
        #     rospy.loginfo("Press any key to Continue8")
        #     raw_input()

        elif self.state is 'check_object':
            rospy.loginfo('---check_object---')
            print '---current state = ' + self.state + '---'
            rospy.loginfo("Press any key to Continue4")
            self.change_state('checking')
            print '---next state = ' + self.state + '---'

        elif self.state is 'pregrasp':
            rospy.loginfo('---pregrasp---')
            self.manipulator.pickobject_pregrasp(self.object_pos)
            self.delay.wait(3000)
            print '---current state = ' + self.state + '---'
            # rospy.loginfo("Press any key to Continue5")
            # raw_input()
            self.change_state('move_to_object_front')
            print '---next state = ' + self.state + '---'
            rospy.loginfo("Press any key to Continue5")
            # raw_input()

        # elif self.state is 'pregrasp':
        #     rospy.loginfo('--pregrasp--')
        #     print 'current state = ' + self.state
        #     if self.device is not None and perception_data.device is self.device:
        #         state = ArmStatus.get_state_from_status(perception_data.input)
        #         rospy.loginfo("Press any key to Continue9")
        #         raw_input()
        #         if state is 'succeeded':
        #     self.change_state('prepare_move_to_object_front')
        #         elif not self.delay.is_waiting():
        #             rospy.logwarn('pregrasp out of time!')
        #             self.change_state('prepare_pregrasp')
        #     rospy.loginfo("Press any key to Continue11")
        #     raw_input()

        elif self.state is 'move_to_object_front':
            rospy.loginfo('---move_to_object_front---')
            self.manipulator.pickobject_movetoobjectfront_1()
            self.delay.wait(1000)
            self.manipulator.pickobject_movetoobjectfront_2()
            self.move_wrist2(-0.2)
            self.delay.wait(1000)
            self.manipulator.pickobject_movetoobjectfront_3()
            self.move_wrist2(-0.2)
            self.delay.wait(1000)
            print '---current state = ' + self.state + '---'
            rospy.loginfo("Press any key to Continue6")
            # raw_input()
            self.change_state('grab_object')
            print '---next state = ' + self.state + '---'
            # rospy.loginfo("Press any key to Continue13")
            # raw_input()

        # elif self.state is 'move_to_object':
            # rospy.loginfo('---move_to_object---')
            # if not self.delay.is_waiting():  # and device state is succeeded
            #     if self.device is not None and perception_data.device is self.device:
            #         state = ArmStatus.get_state_from_status(perception_data.input)
            #         if state is 'succeeded':
            # self.change_state('grab_object')
            # rospy.loginfo("Press any key to Continue14")
            # raw_input()

        elif self.state is 'grab_object':
            # close gripper
            # self.manipulator.pickobject_grasp()
            set_torque_limit()
            rospy.loginfo('---grab_object---')
            print '---current state = ' + self.state + '---'
            self.move_gripper(-0.6)
            self.delay.wait(1000)
            self.move_wrist2(0.0)
            # if self.side is 'right_arm':
            #     self.pub_right_gripper.publish(0.3)
            #     self.delay.wait(1000)
            #     self.pub_right_wrist_2.publish(0.0)
            # elif self.side is 'left_arm':
            #     self.pub_left_gripper.publish(0.3)
            #     self.delay.wait(1000)
            #     self.pub_left_wrist_2.publish(0.0)
            # self.gripper.gripper_close()
            self.change_state('after_grasp')
            print '---next state = ' + self.state + '---'
            rospy.loginfo("Press any key to Continue7")

        elif self.state is 'after_grasp':
            # self.manipulator.pickobject_after_grasp()
            # rospy.loginfo('--after_grasp--')
            print '---current state = ' + self.state + '---'
            self.manipulator.pickobject_prepare()
            self.delay.wait(1000)
            self.change_state('succeed')
            print '---next state = ' + self.state + '---'
            rospy.loginfo("Press any key to Continue8")

        elif self.state is 'succeed':
            self.manipulator.finish()
            rospy.loginfo("Press any key to Continue9")

    # def pick_object(self, side, goal_name='unknown'):
    def pick_object(self, side):
        # self.goal_name = goal_name
        # self.goal_pose = goal_pose
        rospy.loginfo('----pick_object:skill---')
        self.set_side(side)
        # self.controlModule.manipulator.manipulate(side + '_arm', self.goal_pose)
        self.change_state('init_pick')

    def set_side(self, side):
        self.side = side

    def make_device(self):
        if self.side is 'right_arm':
            self.device = 'RIGHT_ARM'
        elif self.side is 'left_arm':
            self.device = 'LEFT_ARM'

    def after_mani(self):
        if self.state is 'moving':
            rospy.loginfo('---after_mani:in_skill---')
            self.delay.wait(1000)
            self.change_state('check_object')
        elif self.state is 'checking':
            rospy.loginfo('---after_mani:in_skill---')
            self.delay.wait(1000)
            self.change_state('pregrasp')

    def move_wrist2(self,value):
        if self.side is 'right_arm':
            self.pub_right_wrist_2.publish(value)
        elif self.side is 'left_arm':
            self.pub_left_wrist_2.publish(value)

    def move_gripper(self,value):
        if self.side is 'right_arm':
            self.pub_right_gripper.publish(value)
        elif self.side is 'left_arm':
            self.pub_left_gripper.publish(value)

    def set_static_pos(self):
        if self.side is 'right_arm':
            self.manipulator.static_pose('right_arm', 'right_normal')
        elif self.side is 'left_arm':
            self.manipulator.static_pose('left_arm', 'left_normal')
