import rospy
from include.abstract_task import AbstractTask
from std_msgs.msg import Float64
from subprocess import call
from dynamixel_controllers.srv import SetTorqueLimit

__author__ = 'nicole'


class RoboZoo(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.arm_pos = [0, 0, 0, 0, 0, 0]

    def perform(self, perception_data):
        if self.state is 'init':
            self.arm_init()
            self.neck_init()
            self.normal()
            self.set_torque_limit(0.3)
            self.change_state('waiting_for_command')
            self.count_start = 0
            self.isTray = False
            self.pub_tilt.publish(0)
            self.pub_pan.publish(0)
            self.check_instruct = ''

        elif self.state is 'waiting_for_command':
            if perception_data.device is self.Devices.JOY:
                print perception_data.input
                if 'RIGHT_TRIGGER' in perception_data.input:
                    side = RIGHT
                elif 'LEFT_TRIGGER' in perception_data.input:
                    side = LEFT
                else:
                    side = None

                if 'X' in perception_data.input:
                    self.mama()	
                #     if 'UP' in perception_data.input:
                #         self.goods_high()
                #         self.check_instruct = 'HIGH'
                #     elif 'RIGHT' in perception_data.input:
                #         self.goods_mid()
                #         self.check_instruct = 'MID'
                #     elif 'LEFT' in perception_data.input:
                #         if self.check_instruct == 'HIGH':
                #             self.pub_right_wrist_2.publish(0.5)
                #             self.check_instruct = ''
                #         elif self.check_instruct == 'MID':
                #             self.pub_right_wrist_2.publish(0.0)
                #             self.check_instruct = ''
                #         elif self.check_instruct == 'LOW':
                #             self.pub_right_wrist_2.publish(-0.3)
                #             self.check_instruct = ''
                #         else:
                #             pass
                #     elif 'DOWN' in perception_data.input:
                #         self.goods_low()
                #         self.check_instruct = 'LOW'
                        # call(['play', '~/SKUBAVOICE/Intro_all.mp3'])
                
                # if 'Y' in perception_data.input:
                #     self.arm_pos = [-0.15, 0.38, 0.3, 0.15, -0.13, -0.3]
                #     # self.respect()
                #     # self.pub_tilt.publish(-0.3)
                #     # call(['play', '~/SKUBAVOICE/welcome_news.mp3'])
                #     self.wai()
                #     rospy.sleep(1.5)
                #     self.pub_pan.publish(0.0)
                #     self.pub_tilt.publish(-0.3)
                #     self.pub_right_gripper.publish(-0.8)
                #     self.pub_left_gripper.publish(0.0)
                #     call(['play', '~/SKUBAVOICE/Hello.mp3'])
                #     rospy.sleep(0.5)
                #     self.subtaskBook.get_subtask(self, 'Say').say('Good afternoon. My name is Lamyai.')
                #     rospy.sleep(1.0)
                #     self.pub_tilt.publish(0)
                    # self.normal()

                # elif 'B' in perception_data.input:
                #     if 'RIGHT' in perception_data.input:
                #         self.basket()
                #     elif 'LEFT' in perception_data.input:
                #         if self.isTray:
                #             self.pub_right_wrist_1.publish(0.0)
                #             self.pub_right_wrist_2.publish(0.0)
                #             self.pub_right_wrist_3.publish(0.0)
                #             rospy.sleep(0.3)
                #             self.pub_left_wrist_1.publish(0.0)
                #             self.pub_left_wrist_2.publish(0.0)
                #             self.pub_left_wrist_3.publish(0.0)
                #             self.isTray = False
                #         else:
                #             self.tray()
                #             self.isTray = True
                #     elif 'UP' in perception_data.input:
                #         self.dust()
                #     elif 'DOWN' in perception_data.input:
                #         self.clean_window()
                #         # self.arm_pos = [0, 0, 0, 0, 0, 0]
                elif 'A' in perception_data.input:
                    self.pub_right_shoulder_2.publish(0.0)
                    # self.pub_left_shoulder_2.publish(0.0)
                    rospy.sleep(0.5)
                    self.arm_pos = [0, 0, 0, 0, 0, 0]
                    self.normal()
                    self.pub_tilt.publish(0)

                elif 'BACK' in perception_data.input:
                    self.count_start = 0
                    self.pub_right_gripper.publish(0.8)

                elif 'START' in perception_data.input:
                    self.count_start += 1
                    if self.count_start == 1:
                        self.pub_right_gripper.publish(-0.3)
                    elif self.count_start == 2:
                        self.pub_right_gripper.publish(-0.4)
                    elif self.count_start == 3:
                        self.pub_right_gripper.publish(-0.6)
                    elif self.count_start == 4:
                        self.pub_right_gripper.publish(-0.8)
                    else:
                        pass

                # if side is RIGHT:
                #     if 'LB' in perception_data.input:
                #         if 'UP' in perception_data.input:
                #             self.arm_pos[2] += 0.1
                #             self.pub_right_elbow.publish(self.arm_pos[2])
                #         elif 'DOWN' in perception_data.input:
                #             self.arm_pos[2] -= 0.1
                #             self.pub_right_elbow.publish(self.arm_pos[2])
                #     elif 'UP' in perception_data.input:
                #         self.arm_pos[0] -= 0.1
                #         print self.arm_pos
                #         self.pub_right_shoulder_1.publish(self.arm_pos[0])
                #     elif 'DOWN' in perception_data.input:
                #         self.arm_pos[0] += 0.1
                #         print(self.arm_pos)
                #         self.pub_right_shoulder_1.publish(self.arm_pos[0])
                #     elif 'LEFT' in perception_data.input:
                #         self.arm_pos[1] += 0.1
                #         self.pub_right_shoulder_2.publish(self.arm_pos[1])
                #     elif 'RIGHT' in perception_data.input:
                #         self.arm_pos[1] -= 0.1
                #         self.pub_right_shoulder_2.publish(self.arm_pos[1])

                # if side is LEFT:
                #     if 'LB' in perception_data.input:
                #         if 'UP' in perception_data.input:
                #             self.arm_pos[5] += 0.1
                #             self.pub_left_elbow.publish(self.arm_pos[2])
                #         elif 'DOWN' in perception_data.input:
                #             self.arm_pos[5] -= 0.1
                #             self.pub_left_elbow.publish(self.arm_pos[2])
                #     elif 'UP' in perception_data.input:
                #         self.arm_pos[3] -= 0.1
                #         print self.arm_pos
                #         self.pub_left_shoulder_1.publish(self.arm_pos[0])
                #     elif 'DOWN' in perception_data.input:
                #         self.arm_pos[3] += 0.1
                #         print(self.arm_pos)
                #         self.pub_left_shoulder_1.publish(self.arm_pos[0])
                #     elif 'LEFT' in perception_data.input:
                #         self.arm_pos[4] += 0.1
                #         self.pub_left_shoulder_2.publish(self.arm_pos[1])
                #     elif 'RIGHT' in perception_data.input:
                #         self.arm_pos[4] -= 0.1
                #         self.pub_left_shoulder_2.publish(self.arm_pos[1])

    def arm_init(self):
        self.pub_right_shoulder_1 = rospy.Publisher('/dynamixel/right_shoulder_1_controller/command', Float64)
        self.pub_right_shoulder_2 = rospy.Publisher('/dynamixel/right_shoulder_2_controller/command', Float64)
        self.pub_right_elbow = rospy.Publisher('/dynamixel/right_elbow_controller/command', Float64)
        self.pub_right_wrist_1 = rospy.Publisher('/dynamixel/right_wrist_1_controller/command', Float64)
        self.pub_right_wrist_2 = rospy.Publisher('/dynamixel/right_wrist_2_controller/command', Float64)
        self.pub_right_wrist_3 = rospy.Publisher('/dynamixel/right_wrist_3_controller/command', Float64)
        self.pub_right_gripper = rospy.Publisher('dynamixel/right_gripper_joint_controller/command', Float64)
        # self.pub_left_shoulder_1 = rospy.Publisher('/dynamixel/left_shoulder_1_controller/command', Float64)
        # self.pub_left_shoulder_2 = rospy.Publisher('/dynamixel/left_shoulder_2_controller/command', Float64)
        # self.pub_left_elbow = rospy.Publisher('/dynamixel/left_elbow_controller/command', Float64)
        # self.pub_left_wrist_1 = rospy.Publisher('/dynamixel/left_wrist_1_controller/command', Float64)
        # self.pub_left_wrist_2 = rospy.Publisher('/dynamixel/left_wrist_2_controller/command', Float64)
        # self.pub_left_wrist_3 = rospy.Publisher('/dynamixel/left_wrist_3_controller/command', Float64)
        # self.pub_left_gripper = rospy.Publisher('dynamixel/left_gripper_joint_controller/command', Float64)

    def neck_init(self):
        self.pub_tilt = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        self.pub_pan = rospy.Publisher('/dynamixel/pan_controller/command', Float64)

    def normal(self):
        self.pub_right_shoulder_1.publish(0.0)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(0.0)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(1.2)
        self.pub_right_wrist_3.publish(0.0)
    	self.pub_right_gripper.publish(-0.8)
    	# self.pub_left_gripper.publish(0.0)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.0)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(1.3)
        # self.pub_left_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        self.pub_tilt.publish(0.0)
        self.pub_pan.publish(0.0)

    def goods_high(self):
        self.pub_right_shoulder_1.publish(-0.7)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(0.2)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(0.7)
        self.pub_right_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.0)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(1.2)
        # self.pub_left_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        self.pub_tilt.publish(0.0)
        self.pub_pan.publish(0.0)

    def goods_mid(self):
        self.pub_right_shoulder_1.publish(-0.6)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(0)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(0.3)
        self.pub_right_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.0)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(1.2)
        # self.pub_left_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        self.pub_tilt.publish(0.0)
        self.pub_pan.publish(0.0)

    def goods_low(self):
        self.pub_right_shoulder_1.publish(-0.5)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(-0.1)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(0.2)
        self.pub_right_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.0)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(1.2)
        # self.pub_left_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        self.pub_tilt.publish(0.0)
        self.pub_pan.publish(0.0)

    def mama(self):
    	self.pub_right_shoulder_1.publish(-0.6)
    	self.pub_right_shoulder_2.publish(0.0)
    	self.pub_right_elbow.publish(0.3)
    	self.pub_right_wrist_1.publish(0.0)
    	self.pub_right_wrist_2.publish(0.6)
    	self.pub_right_wrist_3.publish(0.0)
    	self.pub_right_gripper.publish(-0.8)

    def wai(self):
    	#step1
    	self.pub_right_shoulder_1.publish(0.0)
    	# self.pub_left_shoulder_1.publish(0.0)
    	self.pub_right_shoulder_2.publish(0.0)
    	# self.pub_left_shoulder_2.publish(0.0)
    	self.pub_right_elbow.publish(0.0)
    	# self.pub_left_elbow.publish(0.0)
    	self.pub_right_wrist_1.publish(0.0)
    	# self.pub_left_wrist_1.publish(0.0)
    	self.pub_right_wrist_2.publish(0.0)
    	# self.pub_left_wrist_2.publish(0.0)
    	self.pub_right_wrist_3.publish(0.0)
    	# self.pub_left_wrist_3.publish(0.0)
    	self.pub_right_gripper.publish(-0.8)
    	# self.pub_left_gripper.publish(0.0)
    	rospy.sleep(0.8)
    	#step2
    	self.pub_right_shoulder_1.publish(-0.1)
    	# self.pub_left_shoulder_1.publish(-0.3)
    	self.pub_right_shoulder_2.publish(0.0)
    	# self.pub_left_shoulder_2.publish(0.0)
    	self.pub_right_elbow.publish(0.2)
    	# self.pub_left_elbow.publish(0.0)
    	self.pub_right_wrist_1.publish(0.0)
    	# self.pub_left_wrist_1.publish(0.0)
    	self.pub_right_wrist_2.publish(0.0)
    	# self.pub_left_wrist_2.publish(0.0)
    	self.pub_right_wrist_3.publish(0.0)
    	# self.pub_left_wrist_3.publish(0.0)
    	self.pub_right_gripper.publish(-0.8)
    	# self.pub_left_gripper.publish(0.0)
    	rospy.sleep(0.8)
    	#step3
    	self.pub_right_shoulder_1.publish(-0.15)
    	# self.pub_left_shoulder_1.publish(-0.4)
    	self.pub_right_shoulder_2.publish(0.45)
    	# self.pub_left_shoulder_2.publish(0.2)
    	rospy.sleep(0.5)
    	self.pub_right_elbow.publish(0.3)
    	# self.pub_left_elbow.publish(0.4)
    	self.pub_right_wrist_1.publish(0.0)
    	# self.pub_left_wrist_1.publish(0.0)
    	self.pub_right_wrist_2.publish(-0.8)
    	# self.pub_left_wrist_2.publish(-0.9)
    	self.pub_right_wrist_3.publish(1.3)
    	# self.pub_left_wrist_3.publish(-1.2)
    	self.pub_right_gripper.publish(-0.8)
    	# self.pub_left_gripper.publish(0.0)
    	rospy.sleep(2.0)
    	# self.pub_right_shoulder_2.publish(0.4)
    	# self.pub_left_shoulder_2.publish(0.25)
        rospy.sleep(0.2)
    	# self.pub_left_shoulder_2.publish(0.3)
        rospy.sleep(0.2)
    	# self.pub_left_shoulder_2.publish(0.35)
        rospy.sleep(0.2)
    	# self.pub_left_shoulder_2.publish(0.4)

    def respect(self):
        self.pub_tilt.publish(0)
        self.pub_pan.publish(-0.5)
        rospy.sleep(2.0)
        self.pub_pan.publish(0.5)
        rospy.sleep(2.0)
        self.pub_pan.publish(0)
        rospy.sleep(2.0)
        self.pub_right_shoulder_1.publish(-0.08)
        self.pub_right_shoulder_1.publish(-0.15)
        self.pub_right_shoulder_2.publish(0.08)
        self.pub_right_shoulder_2.publish(0.15)
        self.pub_right_shoulder_2.publish(0.23)
        self.pub_right_shoulder_2.publish(0.32)
        self.pub_right_elbow.publish(0.08)
        self.pub_right_elbow.publish(0.15)
        self.pub_right_elbow.publish(0.23)
        self.pub_right_elbow.publish(0.4)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(-0.8)
        self.pub_right_wrist_3.publish(1.4)
        # rospy.sleep(0.5)
        # self.pub_left_shoulder_1.publish(0.08)
        # self.pub_left_shoulder_1.publish(0.15)
        # self.pub_left_shoulder_2.publish(-0.07)
        # self.pub_left_shoulder_2.publish(-0.15)
        # self.pub_left_elbow.publish(-0.08)
        # self.pub_left_elbow.publish(-0.15)
        # self.pub_left_elbow.publish(-0.23)
        # self.pub_left_elbow.publish(-0.3)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(-1.8)
        # self.pub_left_wrist_3.publish(1.6)

    def tray(self):
        self.pub_right_shoulder_1.publish(-0.08)
        self.pub_right_shoulder_1.publish(-0.15)
        self.pub_right_shoulder_1.publish(-0.23)
        self.pub_right_shoulder_1.publish(-0.3)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(-0.1)
        self.pub_right_elbow.publish(-0.2)
        self.pub_right_elbow.publish(-0.3)
        self.pub_right_elbow.publish(-0.4)
        self.pub_right_wrist_1.publish(1.6)
        self.pub_right_wrist_2.publish(0.3)
        self.pub_right_wrist_3.publish(1.6)
        self.pub_right_gripper.publish(-0.8)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.08)
        # self.pub_left_shoulder_1.publish(0.15)
        # self.pub_left_shoulder_1.publish(0.23)
        # self.pub_left_shoulder_1.publish(0.3)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.08)
        # self.pub_left_elbow.publish(0.15)
        # self.pub_left_elbow.publish(0.23)
        # self.pub_left_elbow.publish(0.3)
        # self.pub_left_elbow.publish(0.5)
        # self.pub_left_wrist_1.publish(1.7)
        # self.pub_left_wrist_2.publish(-0.7)
        # self.pub_left_wrist_3.publish(1.6)

    def basket(self):
        self.pub_right_shoulder_1.publish(-0.1)
        self.pub_right_shoulder_1.publish(-0.2)
        self.pub_right_shoulder_1.publish(-0.3)
        self.pub_right_shoulder_1.publish(-0.4)
        self.pub_right_shoulder_1.publish(-0.5)
        self.pub_right_shoulder_1.publish(-0.6)
        self.pub_right_shoulder_1.publish(-0.7)
        self.pub_right_shoulder_1.publish(-0.8)
        self.pub_right_shoulder_2.publish(-0.08)
        self.pub_right_shoulder_2.publish(-0.15)
        self.pub_right_shoulder_2.publish(-0.23)
        self.pub_right_shoulder_2.publish(-0.3)
        self.pub_right_elbow.publish(0.04)
        self.pub_right_wrist_1.publish(1.1)
        self.pub_right_wrist_2.publish(-0.4)
        self.pub_right_wrist_3.publish(0.3)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.1)
        # self.pub_left_elbow.publish(0.2)
        # self.pub_left_elbow.publish(0.3)
        # self.pub_left_elbow.publish(0.4)
        # self.pub_left_elbow.publish(0.5)
        # self.pub_left_elbow.publish(0.6)
        # self.pub_left_elbow.publish(0.7)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(0.6)
        # self.pub_left_wrist_3.publish(0.0)

    def wave(self):
        self.pub_right_shoulder_1.publish(-0.8)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(0.2)
        self.pub_right_wrist_1.publish(1.4)
        self.pub_right_wrist_2.publish(0.5)
        self.pub_right_wrist_3.publish(1.8)
        self.pub_right_gripper.publish(-0.7)
        rospy.sleep(3.0)
        self.pub_right_wrist_2.publish(-0.5)
        rospy.sleep(2)
        self.pub_right_wrist_2.publish(0.5)
        rospy.sleep(2)
        self.pub_right_wrist_2.publish(-0.5)
        rospy.sleep(2)
        self.pub_right_wrist_2.publish(0.5)
        rospy.sleep(2)
        self.pub_right_wrist_2.publish(-0.5)
        rospy.sleep(2)
        self.pub_right_wrist_2.publish(0.0)    

    def clean_window(self):
        self.pub_right_shoulder_1.publish(-0.1)
        self.pub_right_shoulder_1.publish(-0.2)
        self.pub_right_shoulder_1.publish(-0.3)
        self.pub_right_shoulder_1.publish(-0.4)
        self.pub_right_shoulder_1.publish(-0.5)
        self.pub_right_shoulder_1.publish(-0.6)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(0.0)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(-0.5)
        self.pub_right_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.1)
        # self.pub_left_elbow.publish(0.2)
        # self.pub_left_elbow.publish(0.3)
        # self.pub_left_elbow.publish(0.4)
        # self.pub_left_elbow.publish(0.5)
        # self.pub_left_elbow.publish(0.6)
        # self.pub_left_elbow.publish(0.7)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(0.6)
        # self.pub_left_wrist_3.publish(0.0)
        rospy.sleep(2.0)
        self.pub_right_shoulder_2.publish(0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(-0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(-0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(-0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(0)

    def dust(self):
        self.pub_right_shoulder_1.publish(-0.1)
        self.pub_right_shoulder_1.publish(-0.2)
        self.pub_right_shoulder_1.publish(-0.3)
        self.pub_right_shoulder_1.publish(-0.4)
        self.pub_right_shoulder_1.publish(-0.5)
        self.pub_right_shoulder_1.publish(-0.6)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(0.0)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(1.5)
        self.pub_right_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(0.1)
        # self.pub_left_elbow.publish(0.2)
        # self.pub_left_elbow.publish(0.3)
        # self.pub_left_elbow.publish(0.4)
        # self.pub_left_elbow.publish(0.5)
        # self.pub_left_elbow.publish(0.6)
        # self.pub_left_elbow.publish(0.7)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(0.6)
        # self.pub_left_wrist_3.publish(0.0)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(-0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(-0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(-0.3)
        rospy.sleep(0.7)
        self.pub_right_shoulder_2.publish(0)

    def dance(self):
        self.pub_right_shoulder_1.publish(-0.1)
        self.pub_right_shoulder_1.publish(-0.2)
        self.pub_right_shoulder_1.publish(-0.3)
        self.pub_right_shoulder_1.publish(-0.4)
        self.pub_right_shoulder_1.publish(-0.5)
        self.pub_right_shoulder_1.publish(-0.6)
        self.pub_right_shoulder_1.publish(-0.7)
        self.pub_right_shoulder_1.publish(-0.8)
        self.pub_right_shoulder_1.publish(-0.9)
        self.pub_right_shoulder_1.publish(-1.0)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_elbow.publish(0.1)
        self.pub_right_elbow.publish(0.2)
        self.pub_right_elbow.publish(0.3)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(1.5)
        self.pub_right_wrist_3.publish(0.0)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(0.1)
        # self.pub_left_shoulder_1.publish(0.2)
        # self.pub_left_shoulder_1.publish(0.3)
        # self.pub_left_shoulder_1.publish(0.4)
        # self.pub_left_shoulder_1.publish(0.5)
        # self.pub_left_shoulder_1.publish(0.6)
        # self.pub_left_shoulder_1.publish(0.7)
        # self.pub_left_shoulder_1.publish(0.8)
        # self.pub_left_shoulder_1.publish(0.9)
        # self.pub_left_shoulder_1.publish(1.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_elbow.publish(-0.1)
        # self.pub_left_elbow.publish(-0.2)
        # self.pub_left_elbow.publish(-0.3)
        # self.pub_left_elbow.publish(-0.4)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(1.2)
        # self.pub_left_wrist_3.publish(0.0)
        rospy.sleep(0.5)
        self.pub_right_shoulder_1.publish(-1.0)
        self.pub_right_shoulder_2.publish(-0.3)
        self.pub_right_wrist_1.publish(-0.3)
        self.pub_right_wrist_2.publish(1.8)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(1.0)
        # self.pub_left_shoulder_2.publish(0.12)
        # self.pub_left_wrist_1.publish(0.3)
        # self.pub_left_wrist_2.publish(1.2)
        rospy.sleep(0.5)
        self.pub_right_shoulder_1.publish(-1.0)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(1.5)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(1.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(1.2)
        rospy.sleep(0.5)
        self.pub_right_shoulder_1.publish(-1.0)
        self.pub_right_shoulder_2.publish(-0.3)
        self.pub_right_wrist_1.publish(-0.3)
        self.pub_right_wrist_2.publish(1.8)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(1.0)
        # self.pub_left_shoulder_2.publish(0.12)
        # self.pub_left_wrist_1.publish(0.3)
        # self.pub_left_wrist_2.publish(1.2)
        rospy.sleep(0.5)
        self.pub_right_shoulder_1.publish(-1.0)
        self.pub_right_shoulder_2.publish(0.0)
        self.pub_right_wrist_1.publish(0.0)
        self.pub_right_wrist_2.publish(1.5)
        rospy.sleep(0.3)
        # self.pub_left_shoulder_1.publish(1.0)
        # self.pub_left_shoulder_2.publish(0.0)
        # self.pub_left_wrist_1.publish(0.0)
        # self.pub_left_wrist_2.publish(1.2)

    @staticmethod
    def set_torque_limit(limit=0.3):
        rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
        try:
            rospy.loginfo('set torque')
            set_torque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit',
                                            SetTorqueLimit)
            set_torque(limit)
        except rospy.ServiceException, e:
            rospy.logwarn("Service Torque call failed " + str(e))


RIGHT = 'right'
LEFT = 'left'
