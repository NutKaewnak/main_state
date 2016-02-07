import rospy
import math


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
        print 'R = ' + str(self.R)
 
        var1 = (self.R * self.R - self.UL * self.UL - self.r * self.r) / (2 * self.UL * self.r)
        print "var1 >> " + str(var1)

        self.Zeta1 = math.acos(0.38020184375)
        print 'Zeta1 = ' + str(self.Zeta1)
        self.Zeta2 = math.asin(self.UL * math.sin(self.Zeta1) / self.R)
        print 'Zeta2 = ' + str(self.Zeta2)
        self.As20 = math.asin(self.x / self.R) - (self.Zeta1 - self.Zeta2)
        print 'As20 = ' + str(self.As20)
        self.elbow_position = [self.UL * math.sin(self.As20), self.UL * math.cos(self.As20)]
        self.As21 = math.atan(self.y / (self.r * math.sin(self.Zeta1)))
        self.As21 = -self.As21
        print 'As21 = ' + str(self.As21)
        self.Ae22 = (math.pi / 2) - math.acos(self.r * math.cos(self.Zeta1) / self.FL)
        print 'Ae22 = ' + str(self.Ae22)
        self.z2 = self.UL * math.cos(self.As20) - self.z
        print 'z2 = ' + str(self.z2)
        self.Ah40 = -(math.asin(self.y / math.pow(self.y * self.y + self.z2 * self.z2, 0.5)))
        print 'Ah40 = ' + str(self.Ah40)
        var2 = (self.x - (self.UL * math.sin(self.As20))) / self.FL
        print "var2 >> " + str(var2)
        self.Ah41 = math.acos(0.57084185908)
        print 'Ah41 = ' + str(self.Ah41)
        self.Ah42 = -self.Ah40
        print 'Ah42 = ' + str(self.Ah42)
        # self.As20 = self.As20 / self.SE
        # print 'As20 = ' + str(self.As20)
        
        return [self.As20, self.As21, self.Ae22, self.Ah40, self.Ah41, self.Ah42]
