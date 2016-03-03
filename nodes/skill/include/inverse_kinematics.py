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
        angle_max = 0.5
        angle_min = -1.2
    elif joint_name == 'right_shoulder_2_joint':
        angle_max = 1.1
        angle_min = -1.47
    elif joint_name == 'right_elbow_joint':
        angle_max = 0.22
        angle_min = -0.1
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
        angle_min = -3.8
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

    if bool(angle_max) and bool(angle_min):
        return max(min(angle_max, angle), angle_min)


def inverse_kinematic(target_point):
    """
    Using inverse kinematic to calculate angles that arm should manipulate in order to move to target point.
    :param target_point: (geometry/Point)
    :return: (dict()) dict of arm joint and output angle.
    """
    x = target_point.x
    y = target_point.y
    z = target_point.z
    r = math.sqrt(FL * FL - y * y) + VERY_SMALL_NUMBER
    R = math.hypot(x, z)
    cos_theta1 = (R * R - UL * UL - r * r) / (2 * UL * r + VERY_SMALL_NUMBER)

    try:
        try:
            sin_theta1 = math.sqrt(1 - math.pow(cos_theta1, 2))
            print "--> cos_theta1 = " + str(cos_theta1)
            try:
                theta1 = math.atan(sin_theta1 / cos_theta1 + VERY_SMALL_NUMBER)
            except ValueError:
                theta1 = math.acos((R * R - UL * UL - r * r) / (2 * UL * r + VERY_SMALL_NUMBER))
        except ValueError:
            theta1 = math.acos((R * R - UL * UL - r * r) / (2 * UL * r + VERY_SMALL_NUMBER))
        print 'theta1 = ' + str(theta1)

    except ValueError:
        print 'FALSE theta1'
        return False

    try:
        sin_theta2 = UL * math.sin(theta1) / (R + VERY_SMALL_NUMBER)
        if type(sin_theta2) == float:
            cos_theta2 = math.pow(1 - math.sqrt(sin_theta2, 2))
            if type(cos_theta2) == float:
                theta2 = math.atan(sin_theta2 / (cos_theta2 + VERY_SMALL_NUMBER))
            else:
                theta2 = math.asin(UL * math.sin(theta1) / (R + VERY_SMALL_NUMBER))
        else:
            theta2 = math.asin(UL * math.sin(theta1) / (R + VERY_SMALL_NUMBER))
        print 'theta2 = ' + str(theta2)
    except ValueError:
        print 'FALSE theta2'
        return False

    try:
        sin_theta3 = x / (R + VERY_SMALL_NUMBER)
        if type(sin_theta3) == float:
            cos_theta3 = math.sqrt(1 - math.pow(sin_theta3, 2))
            if type(cos_theta3) == float:
                theta3 = math.atan(sin_theta3 / (cos_theta3 + VERY_SMALL_NUMBER))
            else:
                theta3 = math.asin(x / (R + VERY_SMALL_NUMBER))
        else:
            theta3 = math.asin(x / (R + VERY_SMALL_NUMBER))
        as20 = theta3 - theta1 + theta2
        print 'as20 = ' + str(as20)
    except ValueError:
        print 'FALSE'
        return False

    # self.elbow_position = [self.UL * math.sin(self.as20), self.UL * math.cos(self.as20)]

    try:
        as21 = math.atan(y / ((r * math.sin(theta1))+VERY_SMALL_NUMBER))+0.25
        as21 = -as21
        print 'as21 = ' + str(as21)
    except ValueError:
        print 'FALSE'
        return False

    try:
        cos_theta4 = r * math.cos(theta1) / (FL + VERY_SMALL_NUMBER)
        if type(cos_theta4) == float:
            sin_theta4 = math.sqrt(1 - math.pow(cos_theta4, 2))
            if type(sin_theta4) == float:
                theta4 = math.atan(sin_theta4 / (cos_theta4 + VERY_SMALL_NUMBER))
            else:
                theta4 = math.acos(r * math.cos(theta1) / (FL + VERY_SMALL_NUMBER))
        else:
            theta4 = math.acos(r * math.cos(theta1) / (FL + VERY_SMALL_NUMBER))
        ae22 = (math.pi / 2) - theta4
        print 'ae22 = ' + str(ae22)
    except ValueError:
        print 'FFFFFFFFFFFFAAAAAAAAAAAAAAALLLLLLLSSSSSSSSEEEEEEE'
        return False

    try:
        z2 = UL * math.cos(as20) - z
        # print 'z2 = ' + str(self.z2)
    except ValueError:
        print 'FFFFFFFFFFFFAAAAAAAAAAAAAAALLLLLLLSSSSSSSSEEEEEEE'
        return False

    try:
        sin_theta5 = y / (math.hypot(y, z2) + VERY_SMALL_NUMBER)
        if type(sin_theta5) == float:
            cos_theta5 = math.pow(1 - math.pow(sin_theta5, 2), 0.5)
            if type(cos_theta5) == float:
                theta5 = math.atan(sin_theta5 / (cos_theta5 + VERY_SMALL_NUMBER))
            else:
                theta5 = math.asin(y / (math.pow(y * y + z2 * z2, 0.5) + VERY_SMALL_NUMBER))
        else:
            theta5 = math.asin(y / (math.pow(y * y + z2 * z2, 0.5) + VERY_SMALL_NUMBER))
        ah40 = -theta5/3.0
        print 'ah40 = ' + str(ah40)
    except ValueError:
        print 'FFFFFFFFFFFFAAAAAAAAAAAAAAALLLLLLLSSSSSSSSEEEEEEE'
        return False

    try:
        costheta6 = (x - (UL * math.sin(as20))) / (FL + VERY_SMALL_NUMBER)
        if type(costheta6) == float:
            sintheta6 = math.pow(1 - math.pow(costheta6, 2), 0.5)
            if type(sintheta6) == float:
                theta6 = math.atan(sintheta6 / (costheta6 + VERY_SMALL_NUMBER))
            else:
                theta6 = math.acos((x - (UL * math.sin(as20))) / (FL + VERY_SMALL_NUMBER))
        else:
            theta6 = math.acos((x - (UL * math.sin(as20))) / (FL + VERY_SMALL_NUMBER))
    except ValueError:
        print 'FFFFFFFFFFFFAAAAAAAAAAAAAAALLLLLLLSSSSSSSSEEEEEEE'
        return False

    ah41 = theta6
    print 'ah41 = ' + str(ah41)
    ah42 = -ah40
    print 'ah42 = ' + str(ah42)

    out_angles = dict()
    out_angles['right_shoulder_1_joint'] = -1 * as20
    out_angles['right_shoulder_2_joint'] = -1 * as21
    out_angles['right_elbow_joint'] = -1 * ae22
    out_angles['right_wrist_1_joint'] = ah40
    out_angles['right_wrist_2_joint'] = ah41
    out_angles['right_wrist_3_joint'] = ah42

    return out_angles


def prepare_point_to_invert_kinematic(point):
    """
    Prepare the point for invert kinematic calculation.
    :param point: (geometry/Point)
    :return: (geometry/Point) tuned point for inverse kinematic method.
    """
    # TODO: fix this tf
    out_point = Point()
    out_point.x = point.x-0.1
    out_point.y = point.y+0.14
    out_point.z = point.z-0.69
    return out_point


class InverseKinematics:
    def __init__(self, arm_group='right_arm'):
        # self.SE = 1.75  # SE is shoulder hack encoder ratio
        self.object_point = Point()
        self.arm_group = arm_group

    def init_position(self, point):
        """
        Init position and flip y-axis for invert kinematic
        :param point: (geometry/Point)
        :return: None
        """
        rospy.loginfo("-----INVK INIT POSITION-----")
        if self.arm_group == 'right_arm':
            pass
        elif self.arm_group == 'left_arm':
            point.y *= -1
        self.object_point = point
        print self.arm_group + ' <----> ' + str(self.object_point)

    def pick_prepare(self):
        """
        Move arm to 10cm. in front of the target point.
        :return: (dict()) Dict of arm joint and angle to move on.
        """
        rospy.loginfo('-----PICK PREPARE-----')
        point_to_calculate = Point()
        point_to_calculate.x = self.object_point.x - 0.1
        point_to_calculate.y = self.object_point.y
        point_to_calculate.z = self.object_point.z
        return inverse_kinematic(prepare_point_to_invert_kinematic(point_to_calculate))

    def inverse_kinematics_pregrasp(self):
        """
        Move arm to  the target point.
        :return: (dict()) Dict of arm joint and angle to move on.
        """
        rospy.loginfo('-----PREGRASP-----')
        point_to_calculate = Point()
        point_to_calculate.x = self.object_point.x
        point_to_calculate.y = self.object_point.y
        point_to_calculate.z = self.object_point.z
        return inverse_kinematic(prepare_point_to_invert_kinematic(point_to_calculate))
