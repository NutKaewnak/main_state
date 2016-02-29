#!/usr/bin/env python
import rospy
from controller.inverseKinematics import InverseKinematics
from controller.manipulator_controller import ManipulateController
from task.include.delay import Delay
from std_msgs.msg import Float64


__author__ = 'fptrainnie'


class TestInvKine:
    def __init__(self):
        global invK
        self.delay = Delay()
        rospy.init_node('inverseKinematic')
        invK = InverseKinematics(ManipulateController())
        self.pub_right_gripper = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)
        self.invKine()

    def invKine(self):
        arm_group = "right_arm"
        # arm_group = 'left_arm'

        invK.manipulator_ctrl.init_controller()

        rospy.loginfo("-----ARM NORMAL-----")
        invK.set_normal(arm_group)
        raw_input()

        invK.manipulator_ctrl.manipulate('right_arm', [0.70, -0.14, 0.70])
        object_pos = [0.60, -0.25, 0.77]  # [0.57, -0.07, 0.85]

        rospy.loginfo("-----ARM PREPARE-----")
        invK.manipulator_ctrl.pickobject_prepare()

        rospy.loginfo("-----INIT POSITION-----")
        invK.init_position(object_pos[0], object_pos[1], object_pos[2])
        raw_input()

        rospy.loginfo("-----OPEN GRIPPER-----")
        self.pub_right_gripper.publish(0.8)
        raw_input()

        rospy.loginfo("-----PICK PREPARE-----")
        invK.inverse_kinematics_prepare()
        raw_input()

        rospy.loginfo("-----PICK PREGRASP-----")
        invK.inverse_kinematics_pregrasp()
        raw_input()

        rospy.loginfo("-----CLOSE GRIPPER-----")
        self.pub_right_gripper.publish(0.0)
        raw_input()#

        rospy.loginfo("-----GRASP-----")
        invK.close_gripper()
        raw_input()

if __name__ == '__main__':
    try:
        TestInvKine()
    except rospy.ROSInterruptException:
        pass
