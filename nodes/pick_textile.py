#!/usr/bin/env python
import rospy
from controller.manipulator_controller import ManipulateController
from skill.include import inverse_kinematics
from task.include.delay import Delay
from geometry_msgs.msg import Point


__author__ = 'fptrainnie'


class PickTextile:
    def __init__(self):
        global invK, manipulator_ctrl
        self.delay = Delay()
        rospy.init_node('pick_textile')
        invK = inverse_kinematics.InverseKinematics()
        manipulator_ctrl = ManipulateController()
        self.invKine()

    def invKine(self):
        self.obj_pos = Point()
        self.obj_pos.x = 0.6
        self.obj_pos.y = -0.25
        self.obj_pos.z = 0.6

        rospy.loginfo("-----ARM NORMAL-----")
        manipulator_ctrl.static_pose('right_normal')
        raw_input()

        rospy.loginfo("-----ARM PREPARE-----")
        manipulator_ctrl.static_pose('right_picking_prepare')
        raw_input()

        rospy.loginfo("-----INIT POSITION-----")
        invK.init_position(self.obj_pos)
        raw_input()

        rospy.loginfo("-----OPEN GRIPPER-----")
        self.pub_right_gripper.publish(0.8)
        raw_input()

        out_angle = inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(self.obj_pos), 0)
        raw_input()
        print 'ANGLE = ' + str(out_angle['right_shoulder_1_joint'])
        manipulator_ctrl.move_joint('right_shoulder_1_joint', inverse_kinematics.in_bound('right_shoulder_1_joint', out_angle['right_shoulder_1_joint']))
        manipulator_ctrl.move_joint('right_shoulder_2_joint', inverse_kinematics.in_bound('right_shoulder_2_joint', out_angle['right_shoulder_2_joint']))
        manipulator_ctrl.move_joint('right_elbow_joint', inverse_kinematics.in_bound('right_elbow_joint', out_angle['right_elbow_joint']))
        manipulator_ctrl.move_joint('right_wrist_1_joint', inverse_kinematics.in_bound('right_wrist_1_joint', out_angle['right_wrist_1_joint']))
        manipulator_ctrl.move_joint('right_wrist_2_joint', inverse_kinematics.in_bound('right_wrist_2_joint', out_angle['right_wrist_2_joint']))
        manipulator_ctrl.move_joint('right_wrist_3_joint', inverse_kinematics.in_bound('right_wrist_3_joint', out_angle['right_wrist_3_joint']))
        manipulator_ctrl.move_relative([0, 0, 0], [0, 0, 0])
        self.pub_right_gripper.publish(0.1)
        raw_input()


if __name__ == '__main__':
    try:
        PickTextile()
    except rospy.ROSInterruptException:
        pass
