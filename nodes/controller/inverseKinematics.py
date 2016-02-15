import math
import rospy
from dynamixel_controllers.srv import SetTorqueLimit
# import moveit_commander
# import sys
from controller.manipulator_controller import ManipulateController


__author__ = 'fptrainnie'


class InverseKinematics:

    def __init__(self):
        global mnplctrl, FL, UL
        # rospy.init_node('inverseKinematic')
        FL = 0.29 # FL is Forearm Length
        UL = 0.35 # UL is Upperarm Length
        # self.SE = 1.75 #SE is shoulderhack_encoderratio
        self.object_pos = []
        mnplctrl = ManipulateController()
        # mnplctrl.init_controller()
        self.x = None
        self.y = None
        self.z = None

    def init_position(self, x, y, z):
        self.x = x-0.02-0.08
        self.y = y+0.17
        self.z = z-0.8+0.2
        # mani link
        # set_magicNumber
        self.object_pos = [self.x, self.y, self.z]
        rospy.loginfo("-------INIT POSITION-------")

    def inverse_kinematics_prepare(self):
        rospy.loginfo("---PICK PREPARE---")
        angle = self.inv_kinematic(self.object_pos[0]-0.1, self.object_pos[1], 0.8)
        r_sh1 = self.inBound('right_shoulder_1_joint', -1*angle[0])
        mnplctrl.movejoint('right_shoulder_1_joint', r_sh1)
        r_sh2 = self.inBound('right_shoulder_2_joint', -1*angle[1])
        mnplctrl.movejoint('right_shoulder_2_joint', r_sh2)
        r_elb = self.inBound('right_elbow_joint', -1*angle[2])
        mnplctrl.movejoint('right_elbow_joint', r_elb)
        r_wr1 = self.inBound('right_wrist_1_joint', angle[3])
        mnplctrl.movejoint('right_wrist_1_joint', r_wr1)
        r_wr2 = self.inBound('right_wrist_2_joint', angle[4])
        mnplctrl.movejoint('right_wrist_2_joint', r_wr2)
        r_wr3 = self.inBound('right_wrist_3_joint', angle[5])
        mnplctrl.movejoint('right_wrist_3_joint', r_wr3)

    def inverse_kinematics_pregrasp(self):
        angle = self.inv_kinematic(self.object_pos[0], self.object_pos[1], self.object_pos[2])
        r_sh1 = self.inBound('right_shoulder_1_joint', -1*angle[0])
        mnplctrl.movejoint('right_shoulder_1_joint', r_sh1)
        r_sh2 = self.inBound('right_shoulder_2_joint', -1*angle[1])
        mnplctrl.movejoint('right_shoulder_2_joint', r_sh2)
        r_elb = self.inBound('right_elbow_joint', -1*angle[2])
        mnplctrl.movejoint('right_elbow_joint', r_elb)
        r_wr1 = self.inBound('right_wrist_1_joint', angle[3])
        mnplctrl.movejoint('right_wrist_1_joint', r_wr1)
        r_wr2 = self.inBound('right_wrist_2_joint', angle[4])
        mnplctrl.movejoint('right_wrist_2_joint', r_wr2)
        r_wr3 = self.inBound('right_wrist_3_joint', angle[5])
        mnplctrl.movejoint('right_wrist_3_joint', r_wr3)

    def inv_kinematic(self):
        r = math.pow(FL * FL - self.y * self.y, 0.5) + 0.000000000000000001
        # print 'r = ' + str(self.r)
        R = math.pow(self.x * self.x + self.z * self.z, 0.5)
        # print self.x
        # print self.z
        # print 'R = ' + str(self.R)

        cos_theta1 = (R * R - UL * UL - r * r) / (2 * UL * r + 0.00000001)
        # if type(self.cos_theta1) == float:

        try:
            sin_theta1 = math.pow(1 - math.pow(cos_theta1, 2), 0.5)
            print "--> cos_theta1 = " + str(cos_theta1)
            try:
                theta1 = math.atan(sin_theta1 / cos_theta1+0.00000001)
            except ValueError:
                theta1 = math.acos((R * R - UL * UL - r * r) / (2 * UL * r + 0.00000001))
        except ValueError:
            theta1 = math.acos((R * R - UL * UL - r * r) / (2 * UL * r + 0.00000001))
        # print 'theta1 = ' + str(self.theta1)

        sin_theta2 = UL * math.sin(theta1) / (R+0.00000001)
        if type(sin_theta2) == float:
            cos_theta2 = math.pow(1 - math.pow(sin_theta2, 2), 0.5)
            if type(cos_theta2) == float:
                theta2 = math.atan(sin_theta2 / (cos_theta2+0.00000001))
            else:
                theta2 = math.asin(UL * math.sin(theta1) / (R + 0.00000001))
        else:
            theta2 = math.asin(UL * math.sin(theta1) / (R + 0.00000001))
        # print 'theta2 = ' + str(self.theta2)

        sin_theta3 = self.x / (R + 0.00000001)
        if type(sin_theta3) == float:
            cos_theta3 = math.pow(1 - math.pow(sin_theta3, 2), 0.5)
            if type(cos_theta3) == float:
                theta3 = math.atan(sin_theta3 / (cos_theta3+0.00000001))
            else:
                theta3 = math.asin(self.x / (R + 0.00000001))
        else:
            theta3 = math.asin(self.x / (R + 0.00000001))
        as20 = theta3 - theta1 + theta2
        print 'as20 = ' + str(as20)

        # self.elbow_position = [self.UL * math.sin(self.as20), self.UL * math.cos(self.as20)]

        as21 = math.atan(self.y / ((r * math.sin(theta1))+0.00000001))+0.25
        as21 = -as21
        print 'as21 = ' + str(as21)

        cos_theta4 = r * math.cos(theta1) / (FL+0.00000001)
        if type(cos_theta4) == float:
            sin_theta4 = math.pow(1 - math.pow(cos_theta4, 2), 0.5)
            if type(sin_theta4) == float:
                theta4 = math.atan(sin_theta4 / (cos_theta4+0.00000001))
            else:
                theta4 = math.acos(r * math.cos(theta1) / (FL+0.00000001))
        else:
            theta4 = math.acos(r * math.cos(theta1) / (FL+0.00000001))
        ae22 = (math.pi / 2) - theta4
        print 'ae22 = ' + str(ae22)

        z2 = UL * math.cos(as20) - self.z
        # print 'z2 = ' + str(self.z2)

        sin_theta5 = self.y / (math.pow(self.y * self.y + z2 * z2, 0.5)+0.00000001)
        if type(sin_theta5) == float:
            cos_theta5 = math.pow(1 - math.pow(sin_theta5, 2), 0.5)
            if type(cos_theta5) == float:
                theta5 = math.atan(sin_theta5 / (cos_theta5+0.00000001))
            else:
                theta5 = math.asin(self.y / (math.pow(self.y * self.y + z2 * z2, 0.5)+0.00000001))
        else:
            theta5 = math.asin(self.y / (math.pow(self.y * self.y + z2 * z2, 0.5)+0.00000001))
        ah40 = -theta5
        print 'ah40 = ' + str(ah40)

        costheta6 = (self.x - (UL * math.sin(as20))) / (FL+0.00000001)
        if type(costheta6) == float:
            sintheta6 = math.pow(1 - math.pow(costheta6, 2), 0.5)
            if type(sintheta6) == float:
                theta6 = math.atan(sintheta6 / (costheta6+0.00000001))
            else:
                theta6 = math.acos((self.x - (UL * math.sin(as20))) / (FL+0.00000001))
        else:
            theta6 = math.acos((self.x - (UL * math.sin(as20))) / (FL+0.00000001))

        ah41 = theta6
        print 'ah41 = ' + str(ah41)

        ah42 = -ah40
        print 'ah42 = ' + str(ah42)
        # self.as20 = self.as20 / self.SE
        # print 'as20 = ' + str(self.as20)

        return [as20, as21, ae22, ah40, ah41, ah42]


    def inBound(self, joint_name, angle):
        if joint_name == 'right_shoulder_1_joint':
            if angle >= -1.2 and angle <= 0.5:
                return angle
            else:
                if angle < -1.2:
                    return -1.2
                else:
                    return 0.5
        elif joint_name == 'right_shoulder_2_joint':
            if angle >= -1.46 and angle <= 1.1:
                return angle
            else:
                if angle < -1.46:
                    return -1.46
                else:
                    return 1.1
        elif joint_name == 'right_elbow_joint':
            if angle >= -1.0 and angle <= 0.22:
                return angle
            else:
                if angle < -1.0:
                    return -1.0
                else:
                    return 0.22
        elif joint_name == 'right_wrist_1_joint':
            if angle >= -3.1 and angle <= 2.5:
                return angle
            else:
                if angle < -3.1:
                    return -3.1
                else:
                    return 2.5
        elif joint_name == 'right_wrist_2_joint':
            if angle >= -0.6 and angle <= 1.5:
                return angle
            else:
                if angle < -0.6:
                    return -0.6
                else:
                    return 1.5
        elif joint_name == 'right_wrist_3_joint':
            if angle >= -2.64 and angle <= 3.17:
                return angle
            else:
                if angle < -2.64:
                    return -2.64
                else:
                    return 3.17

    # def init_controller(self):
    #     moveit_commander.rospy_initialize(sys.argv)
    #     self.robot = moveit_commander.RobotCommander()
    #     scene = moveit_commander.PlanningSceneInterface()
