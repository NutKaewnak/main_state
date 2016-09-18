from include.abstract_task import AbstractTask
import rospkg
import rospy
from include.delay import Delay
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import GripperCommandAction, GripperCommandGoal
import os

__author__ = 'cindy'


class RightArm:
    def __init__(self):
        self.ra = actionlib.SimpleActionClient('/dynamixel/right_arm_controller/follow_joint_trajectory',
                                                FollowJointTrajectoryAction)
        self.rg = actionlib.SimpleActionClient('/dynamixel/right_gripper_controller/gripper_action',
                                               GripperCommandAction)
        rospy.loginfo('Waiting for joint trajectory action')
        self.ra.wait_for_server()
        self.rg.wait_for_server()
        rospy.loginfo('Found joint trajectory action!')

    def move_right_joint(self, angles):
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ['right_shoulder_1_joint',
                                       'right_shoulder_2_joint',
                                       'right_elbow_joint',
                                       'right_wrist_1_joint',
                                       'right_wrist_2_joint',
                                       'right_wrist_3_joint']
        point = JointTrajectoryPoint()
        point.positions = angles
        point.time_from_start = rospy.Duration(1)

        goal.trajectory.points.append(point)
        self.ra.send_goal(goal)

    def open(self):
        action_open = GripperCommandGoal()
        action_open.command.position = 0.6
        self.rg.send_goal(action_open)
        self.rg.wait_for_result()
        if self.rg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')

    def close(self):
        action_close = GripperCommandGoal()
        action_close.command.position = 0
        self.rg.send_goal(action_close)
        self.rg.wait_for_result()
        if self.rg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')


class LeftArm:
    def __init__(self):
        self.la = actionlib.SimpleActionClient('/dynamixel/left_arm_controller/follow_joint_trajectory',
                                               FollowJointTrajectoryAction)
        self.lg = actionlib.SimpleActionClient('/dynamixel/left_gripper_controller/gripper_action',
                                               GripperCommandAction)
        rospy.loginfo('Waiting for joint trajectory action')
        self.la.wait_for_server()
        rospy.loginfo('Found joint trajectory action!')
        self.lg.wait_for_server()
        rospy.loginfo('Found joint trajectory action!')

    def move_left_joint(self, angles):
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ['left_shoulder_1_joint',
                                       'left_shoulder_2_joint',
                                       'left_elbow_joint',
                                       'left_wrist_1_joint',
                                       'left_wrist_2_joint',
                                       'left_wrist_3_joint']

        point = JointTrajectoryPoint()
        point.positions = angles
        point.time_from_start = rospy.Duration(1)

        goal.trajectory.points.append(point)
        self.la.send_goal(goal)

    def open(self):
        action_open = GripperCommandGoal()
        action_open.command.position = 0.6
        self.lg.send_goal(action_open)
        self.lg.wait_for_result()
        if self.lg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')

    def close(self):
        action_close = GripperCommandGoal()
        action_close.command.position = 0.0
        self.lg.send_goal(action_close)
        self.lg.wait_for_result()
        if self.lg.get_state() == actionlib.SimpleGoalState.DONE:
            rospy.loginfo('opened')
        else:
            rospy.loginfo('error')


class JoyState(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.right_arm = None
        self.left_arm = None
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init' and perception_data.device is self.Devices.STATE_FLOW:
            self.subtask_name = None
            self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
            rospack = rospkg.RosPack()
            self.path = rospack.get_path('main_state')
            # print self.path
            self.right_arm = RightArm()
            # print 'right_arm', self.right_arm
            self.left_arm = LeftArm()
            # print 'left_arm', self.left_arm

            self.change_state("wait_joy")

        elif self.state is 'wait_joy':
            if perception_data.device is self.Devices.JOY and perception_data.input:
                # print 'input ', perception_data.input
                #LB
                if 'B' in perception_data.input and 'LB' in perception_data.input:
                    self.right_arm.close()
                    self.left_arm.close()
                    self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
                    # self.right_arm.move_right_joint([0, 0, 0, 0, 0, 1.6])
                    # self.left_arm.move_left_joint([0, 0, 0, 0, 0, -1.6])

                    # self.right_arm.move_right_joint([-0.3, 0, 0.1, 0, -0.5, 1.6])
                    # self.left_arm.move_left_joint([0.5, 0, -0.1, -0.5, -1.6])

                    # self.right_arm.move_right_joint([-0.4, 0.3, 0.1, 0, -0.5, 1.6])
                    # self.left_arm.move_left_joint([0.5, -0.35, 0, -0.1, -0.5, -1.6])

                    self.left_arm.move_left_joint([0.7, 0, 0.2, 0, 0, 0])

                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask_name = 'PlaySound'
                    self.subtask.play(os.path.join(self.path, 'sound', 'greeting_jp.wav'))

                    self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.5, 0)
                    self.delay.wait(4)
                    self.change_state("wait_neck_joy")

                elif 'A' in perception_data.input and 'LB' in perception_data.input:
                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask_name = 'PlaySound'
                    self.subtask.play(os.path.join(self.path, 'sound', 'ask_country.wav'))
                    self.change_state('doing')

                elif 'X' in perception_data.input and 'LB' in perception_data.input:
                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask_name = 'PlaySound'
                    self.subtask.play(os.path.join(self.path, 'sound', 'ask_university.wav'))
                    self.change_state('doing')

                elif 'Y' in perception_data.input and 'LB' in perception_data.input:
                    self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                    self.subtask_name = 'PlaySound'
                    self.subtask.play(os.path.join(self.path, 'sound', 'see_you.wav'))
                    self.change_state('doing')

                # RB
                # elif 'B' in perception_data.input and 'RB' in perception_data.input:
                # self.left_arm.move_left_joint([0, 0, 0, 0, 0, 0])
                # # self.right_arm.move_right_joint([0, 0, 0, 0, 0, 0])
                #
                # self.left_arm.move_left_joint([0, 0.1, -0.05, 1.6, -0.7, 1.5])
                # # self.right_arm.move_right_joint([-0.1, 0.1, -0.1, 1.5, 0.5, 1.5])
                #
                # self.left_arm.close()
                # # self.right_arm.close()
                # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>"
                # self.change_state('doing')
                #
                # elif 'A' in perception_data.input and 'RB' in perception_data.input:
                    # self.right_arm = RightArm()
                    # self.left_arm = LeftArm()
                    # self.right_arm.move_right_joint([0, 0, 0, 0, 1.2, 0])
                    # self.left_arm.move_left_joint([0, 0, 0, 0, 1.2, 0])
                    #
                    # self.left_arm.close()
                    # self.right_arm.close()
                    # self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
                    # print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    # self.change_state('doing')
                # elif 'X' in perception_data.input and 'RB' in perception_data.input:
                    # print 'X'
                    # self.left_arm = LeftArm()
                    # self.right_arm = RightArm()
                    # # arm_l.move_left_joint([0, 0, 0, 0.8, 0, 1.5])
                    # # arm_r.move_right_joint([0, 0, 0, 0.8, 0, 1.5])
                    #
                    # self.left_arm.move_left_joint([0, -0.1, -0.1, 1.8, -0.8, 1.5])
                    # self.right_arm.move_right_joint([0, 0.1, -0.1, 1.5, 0.7, 1.5])
                    # self.change_state('doing')
                    # self.delay(0)
                    # self.change_state("wait_joy")
                # elif 'Y' in perception_data.input and 'RB' in perception_data.input:
                #     self.right_arm.close()
                #     self.left_arm.close()
                #     self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
                #     self.right_arm.move_right_joint([0, 0, 0, 0, 0, 1.6])
                #     self.left_arm.move_left_joint([0, 0, 0, 0, 0, -1.6])
                #
                #     self.right_arm.move_right_joint([-0.3, 0, 0.1, 0, -0.5, 1.6])
                #     self.left_arm.move_left_joint([0.5, 0, -0.1, -0.5, -1.6])

                #     self.right_arm.move_right_joint([-0.4, 0.3, 0.1, 0, -0.5, 1.6])
                #     self.left_arm.move_left_joint([0.5, -0.35, 0, -0.1, -0.5, -1.6])
                #     self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.5, 0)
                #     self.delay.wait(4)
                #     self.change_state("wait_neck_joy")

                # LT
                # elif 'B' in perception_data.input and 'LEFT_TRIGGER' in perception_data.input:
                #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                #     self.subtask_name = 'PlaySound'
                #     self.subtask.play(os.path.join(self.path, 'sound', 'loop_next.wav'))
                #     self.change_state('doing')
                # elif 'A' in perception_data.input and 'LEFT_TRIGGER' in perception_data.input:
                #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                #     self.subtask_name = 'PlaySound'
                #     self.subtask.play(os.path.join(self.path, 'sound', 'ask_for_job.wav'))
                #     self.change_state('doing')
                # elif 'X' in perception_data.input and 'LEFT_TRIGGER' in perception_data.input:
                #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                #     self.subtask_name = 'PlaySound'
                #     self.subtask.play(os.path.join(self.path, 'sound', 'what_r_u_doing_here.wav'))
                #     self.change_state('doing')
                # elif 'Y' in perception_data.input and 'LEFT_TRIGGER' in perception_data.input:
                #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                #     self.subtask_name = 'PlaySound'
                #     self.subtask.play(os.path.join(self.path, 'sound', 'can_i_help.wav'))
                #     self.change_state('doing')

                # #RT
                # elif 'B' in perception_data.input and 'RIGHT_TRIGGER' in perception_data.input:
                #     pass
                # elif 'A' in perception_data.input and 'RIGHT_TRIGGER' in perception_data.input:
                #     pass
                # elif 'X' in perception_data.input and 'RIGHT_TRIGGER' in perception_data.input:
                #     pass
                # elif 'Y' in perception_data.input and 'RIGHT_TRIGGER' in perception_data.input:
                #     self.change_state('repeat')

        elif self.state == 'wait_neck_joy' and perception_data.device == self.Devices.STATE_FLOW:
            if not self.delay.is_waiting():
                # self.right_arm.move_right_joint([0, 0, 0, 0, 1.2, 0])
                self.left_arm.move_left_joint([0, 0, 0, 0, 1.2, 0])
                self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
                self.delay.wait(5)
                self.change_state("greet_eng")

        elif self.state == 'greet_eng' and perception_data.device == self.Devices.STATE_FLOW:
            if not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                self.subtask_name = 'PlaySound'
                self.subtask.play(os.path.join(self.path, 'sound', 'greeting_eng.wav'))
                self.delay.wait(5)
                self.change_state("descript")

        elif self.state == 'descript' and perception_data.device == self.Devices.STATE_FLOW:
            if not self.delay.is_waiting():
                self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
                self.subtask_name = 'PlaySound'
                self.subtask.play(os.path.join(self.path, 'sound', 'descript_myself.wav'))
                self.delay.wait(5)
                self.change_state("doing")

        # elif self.state == 'intro' and perception_data.device == self.Devices.STATE_FLOW:
        #     # self.right_arm = RightArm()
        #     # self.left_arm = LeftArm()
        #     self.right_arm.close()
        #     self.left_arm.close()
        #     self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
        #     self.right_arm.move_right_joint([0, 0, 0, 0, 0, 1.6])
        #     self.left_arm.move_left_joint([0, 0, 0, 0, 0, -1.6])
        #
        #     self.right_arm.move_right_joint([0.3, 0, 0.1, 0, -0.5, 1.6])
        #     self.left_arm.move_left_joint([0.5, 0, -0.1, -0.5, -1.6])
        #
        #     self.right_arm.move_right_joint([0.40, 0.3, 0.1, 0, -0.5, 1.6])
        #     self.left_arm.move_left_joint([0.5, -0.35, 0, -0.1, -0.5, -1.6])
        #
        #     self.neck = self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.5, 0)
        #     self.delay.wait(4)
        #
        #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
        #     self.subtask_name = 'PlaySound'
        #     self.subtask.play(os.path.join(self.path, 'sound', 'intro_hello.wav'))
        #
        #     self.change_state('intro_turn_neck')
        #
        # elif self.state is 'intro_turn_neck' and perception_data.device == self.Devices.STATE_FLOW:
        #     if not self.delay.is_waiting():
        #         self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
        #         self.delay.wait(2)
        #         self.change_state("intro_turn_neck_2")
        #
        # elif self.state is 'intro_turn_neck_2' :
        #     if not self.delay.is_waiting():
        #         # self.right_arm = RightArm()
        #         # self.left_arm = LeftArm()
        #         self.right_arm.move_right_joint([0, 0, 0, 0, 1.2, 0])
        #         self.left_arm.move_left_joint([0, 0, 0, 0, 1.2, 0])
        #         self.delay.wait(3)
        #         self.change_state("wait_speak_intro_open")
        #
        # elif self.state is 'wait_speak_intro_open' and perception_data.device == self.Devices.STATE_FLOW:
        #     if self.subtask.state is 'finish' or not self.delay.is_waiting():
        #         self.delay.wait(3)
        #         self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
        #         self.subtask_name = 'PlaySound'
        #         self.subtask.play(os.path.join(self.path, 'sound', 'intro_me.wav'))
        #         self.change_state("wait_speak_intro_open_2")
        #
        # elif self.state is "wait_speak_intro_open_2" and perception_data.device == self.Devices.STATE_FLOW:
        #     if not self.delay.is_waiting():
        #         self.change_state("wait_intro_me")
        #
        # elif self.state is "wait_intro_me" and perception_data.device == self.Devices.STATE_FLOW:
        #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
        #     self.subtask_name = 'PlaySound'
        #     self.subtask.play(os.path.join(self.path, 'sound', 'intro_open.wav'))
        #     self.delay.wait(4)
        #     self.change_state("wait_intro_me_2")
        #
        # elif self.state is "wait_intro_me_2" and perception_data.device == self.Devices.STATE_FLOW:
        #     if not self.delay.is_waiting():
        #         self.change_state("wait_intro_eng")
        #
        # elif self.state is "wait_intro_eng" and perception_data.device == self.Devices.STATE_FLOW:
        #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
        #     self.subtask_name = 'PlaySound'
        #     self.subtask.play(os.path.join(self.path, 'sound', 'intro_eng.wav'))
        #     self.delay.wait(5)
        #     self.change_state("wait_intro_eng_2")
        #
        # elif self.state is 'wait_intro_eng_2' and perception_data.device == self.Devices.STATE_FLOW:
        #     if not self.delay.is_waiting():
        #         self.change_state("wait_intro_next")
        #
        # elif self.state is 'wait_intro_next' and perception_data.device == self.Devices.STATE_FLOW:
        #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
        #     self.subtask_name = 'PlaySound'
        #     self.subtask.play(os.path.join(self.path, 'sound', 'intro_next.wav'))
        #     self.delay.wait(7)
        #     self.change_state('wait_intro_next_2')
        #
        # elif self.state is 'wait_intro_next_2' and perception_data.device == self.Devices.STATE_FLOW:
        #     if not self.delay.is_waiting():
        #         self.change_state("doing")
        #
        # elif self.state is 'repeat' and perception_data.device == self.Devices.STATE_FLOW:
        #     self.subtask = self.subtaskBook.get_subtask(self, 'PlaySound')
        #     self.subtask_name = 'PlaySound'
        #     self.subtask.play(os.path.join(self.path, 'sound', 'loop_engAccent.wav'))
        #     self.delay.wait(120)
        #     self.change_state('wait_repeat')
        #
        # elif self.state is 'wait_repeat' and perception_data.device == self.Devices.STATE_FLOW:
        #     if not self.delay.is_waiting():
        #         self.change_state("repeat")

        elif self.state is 'doing':
            print 'doing'
            if self.subtask_name == 'PlaySound' and (self.subtask.state is 'finish' or self.subtask.state is 'aborted'):
                print '1'
                self.change_state('wait_joy')
            else:
                self.change_state('wait_joy')

        # function terminate
        if perception_data.device is self.Devices.JOY and 'RB' in perception_data.input \
                and 'RIGHT_TRIGGER' in perception_data.input:
            # print dir(self.subtask.subtaskBook)
            if self.subtask_name == 'PlaySound':
                self.subtaskBook.get_subtask(self, 'TurnNeck').turn_absolute(-0.1, 0)
                # self.right_arm.move_right_joint([0, 0, 0, 0, 1.2, 0])
                self.left_arm.move_left_joint([0, 0, 0, 0, 1.2, 0])
                self.subtask.terminate_sound()
                self.subtask_name = None
                self.change_state('wait_joy')
                # print '----------------terminate------------------'
