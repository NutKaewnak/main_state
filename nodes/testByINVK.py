#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

from controller.manipulator_controller import ManipulateController
from nodes.skill.include.inverse_kinematics import InverseKinematics
from task.include.delay import Delay

__author__ = 'fptrainnie'


class TestInvKine:
    def __init__(self):
        global invK
        self.delay = Delay()
        rospy.init_node('inverseKinematic')
        invK = InverseKinematics(ManipulateController())
        self.invKine()

    def invKine(self):
        object_pos = [0.63, -0.20, 0.85]  # [0.57, -0.07, 0.85]
        arm_group = "right_arm"
        # arm_group = 'left_arm'

        invK.manipulator_ctrl.init_controller()

        rospy.loginfo("-----ARM NORMAL-----")
        invK.set_normal(arm_group)
        raw_input()

        rospy.loginfo("-----ARM PREPARE-----")
        invK.manipulator_ctrl.pick_object_prepare()
        raw_input()

        rospy.loginfo("-----INIT POSITION-----")
        invK.init_position(object_pos[0], object_pos[1], object_pos[2])
        raw_input()

        rospy.loginfo("-----OPEN GRIPPER-----")
        invK.manipulator_ctrl.pickobject_opengripper()
        raw_input()

        rospy.loginfo("-----PICK PREPARE-----")
        invK.pick_prepare()
        raw_input()

        rospy.loginfo("-----PICK PREGRASP-----")
        invK.inverse_kinematics_pregrasp()
        raw_input()

        rospy.loginfo("-----CLOSE GRIPPER-----")
        invK.manipulator_ctrl.pickobject_grasp()
        raw_input()

        rospy.loginfo("-----AFTER GRASP-----")
        invK.manipulator_ctrl.pick_object_prepare()
        raw_input()

if __name__ == '__main__':
    try:
        TestInvKine()
    except rospy.ROSInterruptException:
        pass
