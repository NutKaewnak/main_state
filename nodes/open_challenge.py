#!/usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import Bool,Float64
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import object_detection.msg
import tf
from controller.manipulator_controller import ManipulateController
from dynamixel_controllers.srv import SetTorqueLimit
from tabletop.srv import TabletopObjectDetection
import numpy

class OpenChallenge:
    def __init__(self):
        
        rospy.init_node('openchallenge')
        
        self.mnplctrl = ManipulateController()
        self.mnplctrl.init_controller()
        self.pub = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)

        #rospy.wait_for_service('tabletop_object_detection')
        # try:
        #     self.callback = rospy.ServiceProxy('tabletop_object_detection', TabletopObjectDetection)
        # except rospy.ServiceException, e:
        #     print "Service call failed: %s",e

        

    def set_torque_limit(self,limit = 0.5):
        rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
        try:
            rospy.loginfo('settorque')
            setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
            respTorque = setTorque(limit)
        except rospy.ServiceException, e:
            rospy.logwarn("Service Torque call failed " + str(e))

    def open_challange_state(self):
        #response = self.callback
        
        # obj_x = response.centriods[0].point.x
        # obj_y = response.centriods[0].point.y
        # obj_z = response.centriods[0].point.z
        obj_x = 0.6
        obj_y = -0.01
        obj_z = 0.85+0.15 + 0.05 +0.05 +0.02
        #rospy.loginfo('object point : x = ' + str(response.centriods[0].point.x) + ', y = ' + str(response.centriods[0].point.y) + ', z = ' + str(response.centriods[0].point.z)   )
        y_offset = -0.1
        z_offset = 0.20
        torque_limit = 0.5

        # rospy.loginfo('1st:right_init_picking')
        # self.mnplctrl.static_pose('right_arm',"right_init_picking")
        # rospy.loginfo('executing:right_init_picking')
        # raw_input()


        rospy.loginfo('1st:right_pregrasp')
        self.mnplctrl.static_pose('right_arm',"right_pregrasp")
        rospy.loginfo('executing:right_pregrasp')
        #raw_input()
        rospy.sleep(7.00)
        
        rospy.loginfo('2rd: open gripper')
        #self.mnplctrl.movejoint("right_gripper_joint",self.mnplctrl.GRIPPER_OPENED)
        self.pub.publish( Float64(self.mnplctrl.GRIPPER_OPENED) ) 
        rospy.loginfo('executing: open gripper')
        #raw_input()
        rospy.sleep(7.00)
        
        rospy.loginfo('3rd:reach to the top of object')
        self.mnplctrl.manipulate('right_arm',[obj_x,obj_y + y_offset, obj_z  + z_offset],[-1.57,0,0],[0.05,0.1])
        rospy.loginfo('executing:reach to the top of object')
        #raw_input()
        rospy.sleep(7.00)

        # rospy.loginfo('4th movedownward')
        # self.mnplctrl.move_relative('right_arm',[0,0,-0.05],[0,0,0])
        # rospy.loginfo('executing: movedownward')
        #raw_input()

        self.set_torque_limit(torque_limit)
        rospy.loginfo('settorque limit to gripper : ' + str(torque_limit))

        rospy.loginfo('5' + ' Crack')
        #self.mnplctrl.movejoint("right_gripper_joint",self.mnplctrl.GRIPPER_CLOSED)
        self.pub.publish(Float64(self.mnplctrl.GRIPPER_CLOSED) )
        rospy.loginfo('executing: Crack')
        #raw_input()
        rospy.sleep(3.00)

        rospy.loginfo('6' + 'Release')
        #self.mnplctrl.movejoint("right_gripper_joint",self.mnplctrl.GRIPPER_OPENED)
        self.pub.publish( Float64(self.mnplctrl.GRIPPER_OPENED) )
        rospy.loginfo('executing: Release')
        #raw_input()
        rospy.sleep(5.00)

        # rospy.loginfo('7th going_up')
        # self.mnplctrl.move_relative('right_arm',[0,0,+0.05],[0,0,0])
        # rospy.loginfo('executing: going_up')
        # raw_input()


        rospy.loginfo('8th:right_pregrasp')
        self.mnplctrl.static_pose('right_arm',"right_pregrasp")
        rospy.loginfo('executing:right_pregrasp')
        #raw_input()
        rospy.sleep(7.00)

        rospy.loginfo('9th:END')
        self.mnplctrl.static_pose('right_arm',"right_normal")
        rospy.loginfo('executing:END')
        #raw_input()

        rospy.spin()


if __name__=='__main__':
    try:
        state = OpenChallenge()
        state.open_challange_state()

    except rospy.ROSInterruptException:
        pass
