#!/usr/bin/env python
import rospy
from controller.inverseKinematics import InverseKinematics
from controller.manipulator_controller import ManipulateController
from task.include.delay import Delay

__author__ = 'fptrainnie'


class TestInvKine:
    def __init__(self):
        global invK, mnplctrl
        self.delay = Delay()
        rospy.init_node('inverseKinematic')
        invK = InverseKinematics(ManipulateController())
        self.invKine()
        self.delay.wait(5)

    def invKine(self):
    	#  manipulator_ctrl.manipulate('right_arm', [0.50, -0.14, 0.70])
        object_pos = [0.60, -0.17, 0.77]  # [0.57, -0.07, 0.85]
        arm_group = "right_arm"
        # arm_group = 'left_arm'

        rospy.loginfo("-----INIT POSITION-----")
        invK.init_position(arm_group, object_pos[0], object_pos[1], object_pos[2])
        invK.manipulator_ctrl.init_controller()
        raw_input()

        rospy.loginfo("-----OPEN GRIPPER-----")
        invK.manipulator_ctrl.pickobject_opengripper()

        rospy.loginfo("-----PICK PREPARE-----")
        invK.inverse_kinematics_prepare()
        raw_input()

        rospy.loginfo("-----PICK PREGRASP-----")
        invK.inverse_kinematics_pregrasp()
        raw_input()

        rospy.loginfo("-----GRASP-----")
        invK.manipulator_ctrl.pickobject_grasp()

if __name__ == '__main__':
    try:
        TestInvKine()
    except rospy.ROSInterruptException:
        pass
