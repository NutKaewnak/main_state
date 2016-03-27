#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from controller.manipulator_controller import ManipulateController
from skill.include import inverse_kinematics
from task.include.delay import Delay
from geometry_msgs.msg import Point
from dynamixel_controllers.srv import SetTorqueLimit


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
        self.obj_pos.x = 0.68
        self.obj_pos.y = -0.189
        self.obj_pos.z = 0.58

        # rospy.loginfo("-----ARM NORMAL-----")
        # manipulator_ctrl.static_pose('right_normal')
        # rospy.sleep(3)

        rospy.loginfo("-----ARM Before PREPARE 1-----")
        self.pub_right_gripper.publish(0.0)
        manipulator_ctrl.static_pose('right_picking_before_prepare_1')
        rospy.sleep(4)

        rospy.loginfo("-----ARM Before PREPARE 2-----")
        manipulator_ctrl.static_pose('right_picking_before_prepare_2')
        rospy.sleep(4)

        # rospy.loginfo("-----ARM PREPARE-----")
        # manipulator_ctrl.static_pose('right_picking_prepare')
        # rospy.sleep(4)

        rospy.loginfo("-----INIT POSITION-----")
        manipulator_ctrl.init_position(self.obj_pos)
        rospy.sleep(3)



        rospy.loginfo("-----OPEN GRIPPER-----")
        self.pub_right_gripper.publish(1.0)
        # raw_input()
        rospy.sleep(2)

        # rospy.loginfo("-----First step go to object position-----")
        # manipulator_ctrl.move_arm_pick_object_first()
        # rospy.sleep(3)

        # rospy.loginfo("-----Second step go to object position-----")
        # manipulator_ctrl.move_arm_pick_object_second()
        # rospy.sleep(5)

        rospy.loginfo("-----Before pick cloth-----")
        manipulator_ctrl.move_arm_before_pick_cloth()
        # raw_input()
        rospy.sleep(5)

        rospy.loginfo("-----CLOSE GRIPPER + Move relative-----")
        # manipulator_ctrl.move_relative([0, 0, 0], [0, 0, 0])
        # self.set_torque_limit()
        self.pub_right_gripper.publish(0.0)
        rospy.sleep(10)
        #
        manipulator_ctrl.move_arm_after_pick_cloth()
        raw_input()
        rospy.sleep(3)

        manipulator_ctrl.move_arm_turn_left()
        raw_input()
        rospy.sleep(3)

        manipulator_ctrl.move_arm_turn_right()
        raw_input()
        rospy.sleep(3)

        rospy.loginfo("-----OPEN GRIPPER-----")
        self.pub_right_gripper.publish(0.8)
        # raw_input()
        rospy.sleep(2)

        # rospy.loginfo("-----AFTER GRASP-----")
        # manipulator_ctrl.static_pose('right_picking_prepare')
        # # raw_input()

if __name__ == '__main__':
    try:
        TestInvKine()
    except rospy.ROSInterruptException:
        pass
