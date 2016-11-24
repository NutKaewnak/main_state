import math
import rospy


__author__ = 'fptrainnie'


class inverseKinematics:

    def __init__(self):
        rospy.init_node('inverseKinematic')        

    def invKinematic(self, x_endEffector, y_endEffector, z_endEffector):
        x_endEffector = x_endEffector-0.02
        y_endEffector = y_endEffector+0.17
        z_endEffector = z_endEffector-0.8

        self.x = x_endEffector
        self.y = y_endEffector
        self.z = z_endEffector
        self.FL = 0.29
        #FL is Forearm Length
        self.UL = 0.35
        #UL is Upperarm Length       
        self.SE = 1.75 
        #SE is shoulderhack_encoderratio

        self.r = math.pow(self.FL * self.FL - self.y * self.y, 0.5) + 0.000000000000000001
        print 'r = ' + str(self.r)
        self.R = math.pow(self.x * self.x + self.z * self.z, 0.5)
        print self.x
        print self.z
        print 'R = ' + str(self.R)
        
        self.costheta1 = (self.R * self.R - self.UL * self.UL - self.r * self.r) / (2 * self.UL * self.r+0.00000001)
        # if type(self.costheta1) == float:

        try:
            self.sintheta1 = math.pow(1 - math.pow(self.costheta1, 2), 0.5)
            print "--> costheta1 = " + str(self.costheta1)
            try:
                self.theta1 = math.atan(self.sintheta1 / self.costheta1+0.00000001)
            except ValueError:
                self.theta1 = math.acos((self.R * self.R - self.UL * self.UL - self.r * self.r) / (2 * self.UL * self.r+0.00000001))
        except ValueError:
            self.theta1 = math.acos((self.R * self.R - self.UL * self.UL - self.r * self.r) / (2 * self.UL * self.r+0.00000001))
        print 'theta1 = ' + str(self.theta1)

        self.sintheta2 = self.UL * math.sin(self.theta1) / (self.R+0.00000001)
        if type(self.sintheta2) == float:
            self.cosZeta2 = math.pow(1 - math.pow(self.sintheta2, 2), 0.5)
            if type(self.cosZeta2) == float:
                self.theta2 = math.atan(self.sintheta2 / (self.cosZeta2+0.00000001))
            else:
                self.theta2 = math.asin(self.UL * math.sin(self.theta1) / (self.R+0.00000001))
        else:
            self.theta2 = math.asin(self.UL * math.sin(self.theta1) / (self.R+0.00000001))
        print 'theta2 = ' + str(self.theta2)

        self.sintheta3 = self.x / (self.R+0.00000001)
        if type(self.sintheta3) == float:
            self.costheta3 = math.pow(1 - math.pow(self.sintheta3, 2), 0.5)
            if type(self.costheta3) == float:
                self.theta3 = math.atan(self.sintheta3 / (self.costheta3+0.00000001))
            else:
                self.theta3 = math.asin(self.x / (self.R+0.00000001))
        else:
            self.theta3 = math.asin(self.x / (self.R+0.00000001))
        self.As20 = self.theta3 - self.theta1 + self.theta2
        print 'As20 = ' + str(self.As20)

        # self.elbow_position = [self.UL * math.sin(self.As20), self.UL * math.cos(self.As20)]

        self.As21 = math.atan(self.y / ((self.r * math.sin(self.theta1))+0.00000001))+0.25
        self.As21 = -self.As21
        print 'As21 = ' + str(self.As21)

        self.costheta4 = self.r * math.cos(self.theta1) / (self.FL+0.00000001)
        if type(self.costheta4) == float:
            self.sintheta4 = math.pow(1 - math.pow(self.costheta4, 2), 0.5)
            if type(self.sintheta4) == float:
                self.theta4 = math.atan(self.sintheta4 / (self.costheta4+0.00000001))
            else:
                self.theta4 = math.acos(self.r * math.cos(self.theta1) / (self.FL+0.00000001))
        else:
            self.theta4 = math.acos(self.r * math.cos(self.theta1) / (self.FL+0.00000001))
        self.Ae22 = (math.pi / 2) - self.theta4
        print 'Ae22 = ' + str(self.Ae22)

        self.z2 = self.UL * math.cos(self.As20) - self.z
        print 'z2 = ' + str(self.z2)

        self.sintheta5 = self.y / (math.pow(self.y * self.y + self.z2 * self.z2, 0.5)+0.00000001)
        if type(self.sintheta5) == float:
            self.costheta5 = math.pow(1 - math.pow(self.sintheta5, 2), 0.5)
            if type(self.costheta5) == float:
                self.theta5 = math.atan(self.sintheta5 / (self.costheta5+0.00000001))
            else:
                self.theta5 = math.asin(self.y / (math.pow(self.y * self.y + self.z2 * self.z2, 0.5)+0.00000001))
        else:
            self.theta5 = math.asin(self.y / (math.pow(self.y * self.y + self.z2 * self.z2, 0.5)+0.00000001))
        self.Ah40 = -(self.theta5)
        print 'Ah40 = ' + str(self.Ah40)
        
        self.costheta6 = (self.x - (self.UL * math.sin(self.As20))) / (self.FL+0.00000001)
        if type(self.costheta6) == float:
            self.sintheta6 = math.pow(1 - math.pow(self.costheta6, 2), 0.5)
            if type(self.sintheta6) == float:
                self.theta6 = math.atan(self.sintheta6 / (self.costheta6+0.00000001))
            else:
                self.theta6 = math.acos((self.x - (self.UL * math.sin(self.As20))) / (self.FL+0.00000001))
        else:
            self.theta6 = math.acos((self.x - (self.UL * math.sin(self.As20))) / (self.FL+0.00000001))
        
        # self.Ah41 = self.theta6
        self.Ah41 = 0.5
        # print 'Ah41 = ' + str(self.Ah41)
        
        self.Ah42 = -self.Ah40
        print 'Ah42 = ' + str(self.Ah42)
        # self.As20 = self.As20 / self.SE
        # print 'As20 = ' + str(self.As20)
        
        return [self.As20, self.As21, self.Ae22, self.Ah40, self.Ah41, self.Ah42]

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