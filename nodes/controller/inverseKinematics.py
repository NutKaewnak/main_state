import math
import rospy
from dynamixel_controllers.srv import SetTorqueLimit
# import moveit_commander
# import sys
from manipulator_controller import ManipulateController

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
        self.arm_group = ''

    def init_position(self, arm_group, x, y, z):
        rospy.loginfo("-----INIT POSITION-----")
        self.arm_group = arm_group
        if self.arm_group == 'right_arm':
            y = y
        elif self.arm_group == 'left_arm':
            y = -y
        self.object_pos = [x, y, z]
        print self.arm_group + ' <----> ' + str(self.object_pos)

    def cal_mani(self, x, y, z):
        pos_x = x-0.1
        pos_y = y+0.17
        pos_z = z-0.8
        angle = self.inv_kinematic(pos_x, pos_y, pos_z)
        return angle

    def inverse_kinematics_prepare(self):
        rospy.loginfo('-----PICK PREPARE-----')
        angle = self.cal_mani(self.object_pos[0]-0.1, self.object_pos[1], 0.82222)
        self.move(angle)

    def inverse_kinematics_pregrasp(self):
        rospy.loginfo('-----PREGRASP-----')
        angle = self.cal_mani(self.object_pos[0], self.object_pos[1], self.object_pos[2])
        self.move(angle)

    def inv_kinematic(self, x, y, z):
        r = math.pow(FL * FL - y * y, 0.5) + 0.000000000000000001
        R = math.pow(x * x + z * z, 0.5)
        cos_theta1 = (R * R - UL * UL - r * r) / (2 * UL * r + 0.00000001)

        try:
            sin_theta1 = math.pow(1 - math.pow(cos_theta1, 2), 0.5)
            print "--> cos_theta1 = " + str(cos_theta1)
            try:
                theta1 = math.atan(sin_theta1 / cos_theta1+0.00000001)
            except ValueError:
                theta1 = math.acos((R * R - UL * UL - r * r) / (2 * UL * r + 0.00000001))
        except ValueError:
            theta1 = math.acos((R * R - UL * UL - r * r) / (2 * UL * r + 0.00000001))
        print 'theta1 = ' + str(theta1)

        sin_theta2 = UL * math.sin(theta1) / (R+0.00000001)
        if type(sin_theta2) == float:
            cos_theta2 = math.pow(1 - math.pow(sin_theta2, 2), 0.5)
            if type(cos_theta2) == float:
                theta2 = math.atan(sin_theta2 / (cos_theta2+0.00000001))
            else:
                theta2 = math.asin(UL * math.sin(theta1) / (R + 0.00000001))
        else:
            theta2 = math.asin(UL * math.sin(theta1) / (R + 0.00000001))
        print 'theta2 = ' + str(theta2)

        sin_theta3 = x / (R + 0.00000001)
        if type(sin_theta3) == float:
            cos_theta3 = math.pow(1 - math.pow(sin_theta3, 2), 0.5)
            if type(cos_theta3) == float:
                theta3 = math.atan(sin_theta3 / (cos_theta3+0.00000001))
            else:
                theta3 = math.asin(x / (R + 0.00000001))
        else:
            theta3 = math.asin(x / (R + 0.00000001))
        as20 = theta3 - theta1 + theta2
        print 'as20 = ' + str(as20)

        # self.elbow_position = [self.UL * math.sin(self.as20), self.UL * math.cos(self.as20)]

        as21 = math.atan(y / ((r * math.sin(theta1))+0.00000001))+0.25
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

        z2 = UL * math.cos(as20) - z
        # print 'z2 = ' + str(self.z2)

        sin_theta5 = y / (math.pow(y * y + z2 * z2, 0.5)+0.00000001)
        if type(sin_theta5) == float:
            cos_theta5 = math.pow(1 - math.pow(sin_theta5, 2), 0.5)
            if type(cos_theta5) == float:
                theta5 = math.atan(sin_theta5 / (cos_theta5+0.00000001))
            else:
                theta5 = math.asin(y / (math.pow(y * y + z2 * z2, 0.5)+0.00000001))
        else:
            theta5 = math.asin(y / (math.pow(y * y + z2 * z2, 0.5)+0.00000001))
        ah40 = -theta5
        print 'ah40 = ' + str(ah40)

        costheta6 = (x - (UL * math.sin(as20))) / (FL+0.00000001)
        if type(costheta6) == float:
            sintheta6 = math.pow(1 - math.pow(costheta6, 2), 0.5)
            if type(sintheta6) == float:
                theta6 = math.atan(sintheta6 / (costheta6+0.00000001))
            else:
                theta6 = math.acos((x - (UL * math.sin(as20))) / (FL+0.00000001))
        else:
            theta6 = math.acos((x - (UL * math.sin(as20))) / (FL+0.00000001))

        ah41 = theta6
        print 'ah41 = ' + str(ah41)

        ah42 = -ah40
        print 'ah42 = ' + str(ah42)
        # self.as20 = self.as20 / self.SE
        # print 'as20 = ' + str(self.as20)

        return [as20, as21, ae22, ah40, ah41, ah42]

    def move(self, angle):
        if self.arm_group == 'right_arm':
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
        elif self.arm_group == 'left_arm':
            l_sh1 = self.inBound('left_shoulder_1_joint', -1*angle[0])
            mnplctrl.movejoint('left_shoulder_1_joint', l_sh1)
            l_sh2 = self.inBound('left_shoulder_2_joint', -1*angle[1])
            mnplctrl.movejoint('left_shoulder_2_joint', l_sh2)
            l_elb = self.inBound('left_elbow_joint', -1*angle[2])
            mnplctrl.movejoint('left_elbow_joint', l_elb)
            l_wr1 = self.inBound('left_wrist_1_joint', angle[3])
            mnplctrl.movejoint('left_wrist_1_joint', l_wr1)
            l_wr2 = self.inBound('left_wrist_2_joint', angle[4])
            mnplctrl.movejoint('left_wrist_2_joint', l_wr2)
            l_wr3 = self.inBound('left_wrist_3_joint', angle[5])
            mnplctrl.movejoint('left_wrist_3_joint', l_wr3)    

    def inBound(self, joint_name, angle):
        if self.arm_group == 'right_arm':
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
        # ---------------------------
        elif self.arm_group == 'left_arm':
            if joint_name == 'left_shoulder_1_joint':
                if angle >= -3.8 and angle <= 0.58:
                    return angle
                else:
                    if angle < -3.8:
                        return -3.8
                    else:
                        return 0.58
            elif joint_name == 'left_shoulder_2_joint':
                if angle >= -1.5 and angle <= 1.0:
                    return angle
                else:
                    if angle < -1.5:
                        return -1.5
                    else:
                        return 1.0
            elif joint_name == 'left_elbow_joint':
                if angle >= -0.88 and angle <= 0.17:
                    return angle
                else:
                    if angle < -0.88:
                        return -0.88
                    else:
                        return 0.17
            elif joint_name == 'left_wrist_1_joint':
                if angle >= -3.1 and angle <= 2.5:
                    return angle
                else:
                    if angle < -3.1:
                        return -3.1
                    else:
                        return 2.5
            elif joint_name == 'left_wrist_2_joint':
                if angle >= -0.6 and angle <= 1.5:
                    return angle
                else:
                    if angle < -0.6:
                        return -0.6
                    else:
                        return 1.5
            elif joint_name == 'left_wrist_3_joint':
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
