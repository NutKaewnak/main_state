import math
import rospy
from geometry_msgs.msg import Point

__author__ = 'fptrainnie'

VERY_SMALL_NUMBER = 0.000000000000000001

FL = 0.29  # FL is Forearm Length
UL = 0.35  # UL is Upperarm Length


def in_bound(joint_name, angle):
    angle_max = None
    angle_min = None
    if joint_name == 'right_shoulder_1_joint':
        print 'THIS IS '+joint_name
        angle_max = 0.4
        angle_min = -1.35
    elif joint_name == 'right_shoulder_2_joint':
        angle_max = 1.1
        angle_min = -1.47
    elif joint_name == 'right_elbow_joint':
        angle_max = 0.22
        angle_min = -1.5
    elif joint_name == 'right_wrist_1_joint':
        angle_max = 2.5
        angle_min = -3.1
    elif joint_name == 'right_wrist_2_joint':
        angle_max = 1.5
        angle_min = -0.6
    elif joint_name == 'right_wrist_3_joint':
        angle_max = 3.17
        angle_min = -2.64

    elif joint_name == 'left_shoulder_1_joint':
        angle_max = 0.58
        angle_min = -1.2
    elif joint_name == 'left_shoulder_2_joint':
        angle_max = 1.0
        angle_min = -1.5
    elif joint_name == 'left_elbow_joint':
        angle_max = 0.17
        angle_min = -0.88
    elif joint_name == 'left_wrist_1_joint':
        angle_max = 2.5
        angle_min = -3.1
    elif joint_name == 'left_wrist_2_joint':
        angle_max = 1.5
        angle_min = -0.6
    elif joint_name == 'left_wrist_3_joint':
        angle_max = 3.17
        angle_min = -2.64

    print 'Kuyyyy'
    if bool(angle_max) and bool(angle_min):
        print 'KUYYYY'
        if angle > angle_max or angle < angle_min:
            print '-!-!-!-!-!-!-!-!-!-! SAsssssS OUT OF BOUND --> ' + str(angle)
            return False
        print 'INBOUND na SAssssSSSS --> ' + str(angle)
        return angle


def inverse_kinematic(target_point, orientation = 0.0):
    """
    Using inverse kinematic to calculate angles that arm should manipulate in order to move to target point.
    :param orientation: desired wrist angle respect to (arm_side)_wrist_2_joint
    :param target_point: (geometry/Point)
    :return: (dict()) dict of arm joint and output angle.
    """
    pos_x = float(target_point.x)
    pos_y = float(target_point.y)
    pos_z = float(target_point.z)
    try:
        r = math.sqrt(FL * FL - pos_y * pos_y)
        R = math.hypot(pos_x, pos_z)
        print 'r = ' + str(r)
        print 'R = ' + str(R)

        try:
            cos_theta2 = (R * R - UL * UL - r * r) / (2 * UL * r + VERY_SMALL_NUMBER)
            sin_theta2 = math.sqrt(1 - math.pow(cos_theta2, 2))
            theta2 = math.atan2(sin_theta2, cos_theta2)
            print "THEHA2 = " + str(theta2)
        except ValueError:
            print 'FALSE theta2'
            return False

        try:
            theta1 = math.atan2(pos_x, math.fabs(pos_z)) - math.atan2(r*math.sin(theta2), UL + r*math.cos(theta2))
            as20 = theta1
            as20 *= -1
            print 'as20 = ' + str(as20)
            as25 = as20
            print 'as25 = ' + str(as25)
        except ValueError:
            print 'FALSE as20 as25'
            return False

        try:
            as21 = math.atan2(pos_y, (r + VERY_SMALL_NUMBER))
            print 'as21 = ' + str(as21)
            as26 = -1 * as21
            print 'as26 = ' + str(as26)
        except ValueError:
            print 'FALSE as21 as26'
            return False

        try:
            ae22 = theta2 - 0.5*math.pi
            print 'ae22 = ' + str(ae22)
            ae27 = ae22
            print 'ae27 = ' + str(ae27)
        except ValueError:
            print 'FALSE ae22'
            return False

        try:
            theta_d = 0.5*math.pi - orientation
            theta3 = theta_d - theta1 - theta2
            print 'theta3 = ' + str(theta3)
            ah41 = -theta3
            print "ah41 = " + str(ah41)
            ah46 = ah41
            print 'ah46 = ' + str(ah46)
        except ValueError:
            print 'FALSE ah41'

        right_rotate_wrist = as21
        print 'Right rotate = ' + str(right_rotate_wrist)
        ah40 = right_rotate_wrist / 2.0
        print 'ah40 = ' + str(ah40)
        ah42 = ah40
        print 'ah42 = ' + str(ah42)

        left_rotate_wrist = as26
        print 'Left rotate = ' + str(left_rotate_wrist)
        ah45 = left_rotate_wrist / 2.0
        print 'ah45 = ' + str(ah45)
        ah47 = ah45
        print 'ah47 = ' + str(ah47)

        out_angles = dict()
        out_angles['right_shoulder_1_joint'] = as20
        out_angles['right_shoulder_2_joint'] = as21
        out_angles['right_elbow_joint'] = ae22
        out_angles['right_wrist_1_joint'] = ah40
        out_angles['right_wrist_2_joint'] = ah41
        out_angles['right_wrist_3_joint'] = ah42

        out_angles['left_shoulder_1_joint'] = as25
        out_angles['left_shoulder_2_joint'] = as26
        out_angles['left_elbow_joint'] = ae27
        # out_angles['left_wrist_1_joint'] = ah40
        # out_angles['left_wrist_2_joint'] = ah41
        # out_angles['left_wrist_3_joint'] = ah42
        out_angles['left_wrist_1_joint'] = ah45
        out_angles['left_wrist_2_joint'] = ah46
        out_angles['left_wrist_3_joint'] = ah47

        return out_angles
    except ValueError:
        print "CAN'T CALCULATE R or r"
        return False

class InverseKinematics:
    def __init__(self, arm_group='right_arm'):
        # self.SE = 1.75  # SE is shoulder hack encoder ratio
        self.object_point = Point()
        self.arm_group = arm_group