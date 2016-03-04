#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

from controller.manipulator_controller import ManipulateController
from skill.include import inverse_kinematics
from task.include.delay import Delay

__author__ = 'fptrainnie'


class TestInvKine:
    def __init__(self):
        global invK, manipulator_ctrl
        self.delay = Delay()
        rospy.init_node('inverseKinematic')
        invK = inverse_kinematics.InverseKinematics()
        manipulator_ctrl = ManipulateController()
        self.invKine()

    def invKine(self):
        object_pos = [0.63, -0.20, 0.85]  # [0.57, -0.07, 0.85]
        arm_group = "right_arm"
        # arm_group = 'left_arm'
        manipulator_ctrl.init_controller()

        rospy.loginfo("-----ARM NORMAL-----")
        manipulator_ctrl.pick_object_init(arm_group)
        raw_input()

        # rospy.loginfo("-----ARM PREPARE-----")
        # manipulator_ctrl.pick_object_prepare()
        # raw_input()

        rospy.loginfo("-----INIT POSITION-----")
        invK.init_position(object_pos)
        raw_input()

        rospy.loginfo("-----OPEN GRIPPER-----")
        manipulator_ctrl.pickobject_opengripper()
        raw_input()

        rospy.loginfo("-----PICK PREPARE-----")
        inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(invK.point_pick_prepare()))
        raw_input()

        rospy.loginfo("-----PICK PREGRASP-----")
        manipulator_ctrl.transform_point(invK.point_inverse_kinematics_pregrasp())
        raw_input()

        rospy.loginfo("-----CLOSE GRIPPER-----")
        manipulator_ctrl.pickobject_grasp()
        raw_input()

        rospy.loginfo("-----AFTER GRASP-----")
        manipulator_ctrl.pick_object_prepare()
        raw_input()

if __name__ == '__main__':
    try:
        TestInvKine()
    except rospy.ROSInterruptException:
        pass
