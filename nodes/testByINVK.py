#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from controller.manipulator_controller import ManipulateController
from skill.include import inverse_kinematics
from task.include.delay import Delay
from geometry_msgs.msg import Point
from dynamixel_controllers.srv import SetTorqueLimit
import math


__author__ = 'fptrainnie'


class TestInvKine:
    def __init__(self):
        global invK, manipulator_ctrl
        self.delay = Delay()
        rospy.init_node('TestInverseKinematic')
        invK = inverse_kinematics.InverseKinematics()
        manipulator_ctrl = ManipulateController()
        manipulator_ctrl.init_controller()
        self.pub_right_gripper = rospy.Publisher('dynamixel/right_gripper_joint_controller/command', Float64)
        self.pub_left_gripper = rospy.Publisher('dynamixel/left_gripper_joint_controller/command', Float64)
        self.set_torque_limit = rospy.ServiceProxy('/dynamixel/right_gripper/set_torque_limit', SetTorqueLimit)
        self.invKine()

    def set_torque_limit(self, limit = 0.3):
        rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
        try:
            rospy.loginfo('settorque')
            setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
            respTorque = setTorque(limit)
        except rospy.ServiceException, e:
            rospy.logwarn("Service Torque call failed " + str(e))

    def invKine(self):

        # FOR TEST RIGHT ARM
        # position y < 0

        GRIPPER_EFFORT = 0.4

        self.obj_pos = Point()
        self.obj_pos.x = 0.66-0.25
        self.obj_pos.y = -0.188 + 0.04
        self.obj_pos.z = 0.82

        # rospy.loginfo("-----ARM NORMAL-----")
        # manipulator_ctrl.static_pose('right_normal')
        # raw_input()

        rospy.loginfo("-----ARM PREPARE-----")
        manipulator_ctrl.static_pose('right_picking_prepare')
        raw_input()

        rospy.loginfo("-----INIT POSITION-----")
        invK.init_position(self.obj_pos)
        raw_input()

        rospy.loginfo("-----OPEN GRIPPER-----")
        self.pub_right_gripper.publish(0.8)
        raw_input()

        #out_angle = inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(invK.prepare_point_to_invert_kinematic(self.obj_pos)))
        # manipulator_ctrl.transform_point(self.obj_pos)
        out_angle = inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(self.obj_pos), 0)
        raw_input()
        print 'ANGLE = ' + str(out_angle['right_shoulder_1_joint'])
        manipulator_ctrl.move_joint('right_shoulder_1_joint', inverse_kinematics.in_bound('right_shoulder_1_joint', out_angle['right_shoulder_1_joint']))
        manipulator_ctrl.move_joint('right_shoulder_2_joint', inverse_kinematics.in_bound('right_shoulder_2_joint', out_angle['right_shoulder_2_joint']))
        manipulator_ctrl.move_joint('right_elbow_joint', inverse_kinematics.in_bound('right_elbow_joint', out_angle['right_elbow_joint']))
        manipulator_ctrl.move_joint('right_wrist_1_joint', inverse_kinematics.in_bound('right_wrist_1_joint', out_angle['right_wrist_1_joint']))
        manipulator_ctrl.move_joint('right_wrist_2_joint', inverse_kinematics.in_bound('right_wrist_2_joint', out_angle['right_wrist_2_joint']))
        manipulator_ctrl.move_joint('right_wrist_3_joint', inverse_kinematics.in_bound('right_wrist_3_joint', out_angle['right_wrist_3_joint']))
        raw_input()

        self.obj_pos.x += 0.1
        out_angle = inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(self.obj_pos), 0)
        raw_input()
        print 'ANGLE = ' + str(out_angle['right_shoulder_1_joint'])
        manipulator_ctrl.move_joint('right_shoulder_1_joint', inverse_kinematics.in_bound('right_shoulder_1_joint', out_angle['right_shoulder_1_joint']))
        manipulator_ctrl.move_joint('right_shoulder_2_joint', inverse_kinematics.in_bound('right_shoulder_2_joint', out_angle['right_shoulder_2_joint']))
        manipulator_ctrl.move_joint('right_elbow_joint', inverse_kinematics.in_bound('right_elbow_joint', out_angle['right_elbow_joint']))
        manipulator_ctrl.move_joint('right_wrist_1_joint', inverse_kinematics.in_bound('right_wrist_1_joint', out_angle['right_wrist_1_joint']))
        manipulator_ctrl.move_joint('right_wrist_2_joint', inverse_kinematics.in_bound('right_wrist_2_joint', out_angle['right_wrist_2_joint']))
        manipulator_ctrl.move_joint('right_wrist_3_joint', inverse_kinematics.in_bound('right_wrist_3_joint', out_angle['right_wrist_3_joint']))
        raw_input()

        self.obj_pos.x += 0.05
        out_angle = inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(self.obj_pos), 0)
        raw_input()
        print 'ANGLE = ' + str(out_angle['right_shoulder_1_joint'])
        manipulator_ctrl.move_joint('right_shoulder_1_joint', inverse_kinematics.in_bound('right_shoulder_1_joint', out_angle['right_shoulder_1_joint']))
        manipulator_ctrl.move_joint('right_shoulder_2_joint', inverse_kinematics.in_bound('right_shoulder_2_joint', out_angle['right_shoulder_2_joint']))
        manipulator_ctrl.move_joint('right_elbow_joint', inverse_kinematics.in_bound('right_elbow_joint', out_angle['right_elbow_joint']))
        manipulator_ctrl.move_joint('right_wrist_1_joint', inverse_kinematics.in_bound('right_wrist_1_joint', out_angle['right_wrist_1_joint']))
        manipulator_ctrl.move_joint('right_wrist_2_joint', inverse_kinematics.in_bound('right_wrist_2_joint', out_angle['right_wrist_2_joint']))
        manipulator_ctrl.move_joint('right_wrist_3_joint', inverse_kinematics.in_bound('right_wrist_3_joint', out_angle['right_wrist_3_joint']))
        raw_input()

        rospy.loginfo("-----CLOSE GRIPPER + Move relative-----")
        # manipulator_ctrl.move_relative([0, 0, 0], [0, 0, 0])
        # self.set_torque_limit()
        self.pub_right_gripper.publish(0.2)
        raw_input()

        rospy.loginfo("-----AFTER GRASP-----")
        manipulator_ctrl.static_pose('right_picking_prepare')
        # raw_input()


    # --------------------------------------------------------------------- #

        # # FOR TEST LEFT ARM
        # # position y > 0
        #
        # self.obj_pos = Point()
        # self.obj_pos.x = 0.6
        # self.obj_pos.y = 0.25
        # self.obj_pos.z = 0.8
        #
        # arm_group = 'left_arm'
        #
        # rospy.loginfo("-----LEFT ARM NORMAL-----")
        # manipulator_ctrl.static_pose('left_normal')
        # raw_input()
        #
        # rospy.loginfo("-----LEFT ARM PREPARE-----")
        # # manipulator_ctrl.static_pose('left_picking_prepare')
        # raw_input()
        #
        # rospy.loginfo("-----INIT POSITION-----")
        # invK.init_position(self.obj_pos)
        # raw_input()
        #
        # rospy.loginfo("-----OPEN GRIPPER-----")
        # self.pub_left_gripper.publish(0.8)
        # raw_input()
        #
        # #out_angle = inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(invK.prepare_point_to_invert_kinematic(self.obj_pos)))
        # # manipulator_ctrl.transform_point(self.obj_pos)
        # out_angle = inverse_kinematics.inverse_kinematic(manipulator_ctrl.transform_point(self.obj_pos), 0)
        # raw_input()
        # manipulator_ctrl.move_joint('left_shoulder_1_joint', inverse_kinematics.in_bound('left_shoulder_1_joint', out_angle['left_shoulder_1_joint']))
        # manipulator_ctrl.move_joint('left_shoulder_2_joint', inverse_kinematics.in_bound('left_shoulder_2_joint', out_angle['left_shoulder_2_joint']))
        # manipulator_ctrl.move_joint('left_elbow_joint', inverse_kinematics.in_bound('left_elbow_joint', out_angle['left_elbow_joint']))
        # manipulator_ctrl.move_joint('left_wrist_1_joint', inverse_kinematics.in_bound('left_wrist_1_joint', out_angle['left_wrist_1_joint']))
        # manipulator_ctrl.move_joint('left_wrist_2_joint', inverse_kinematics.in_bound('left_wrist_2_joint', out_angle['left_wrist_2_joint']))
        # manipulator_ctrl.move_joint('left_wrist_3_joint', inverse_kinematics.in_bound('left_wrist_3_joint', out_angle['left_wrist_3_joint']))
        # raw_input()
        # rospy.loginfo("-----CLOSE GRIPPER + Move relative-----")
        # manipulator_ctrl.move_relative([0, 0, 0], [0, 0, 0])
        # self.pub_left_gripper.publish(0.1)
        # raw_input()
        #
        # rospy.loginfo("-----AFTER GRASP-----")
        # manipulator_ctrl.static_pose('left_picking_prepare')
        # raw_input()
        #
        # rospy.spin()

if __name__ == '__main__':
    try:
        TestInvKine()
    except rospy.ROSInterruptException:
        pass
