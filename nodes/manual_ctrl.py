#!/usr/bin/env python
#__author__ = fptrainnie
#__scripts__ = manual_control


from sensor_msgs.msg import Joy
import rospy
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import Bool,Float64,Header
import shape_msgs.msg
import geometry_msgs.msg
from trajectory_msgs.msg import *
from control_msgs.msg import FollowJointTrajectoryFeedback
import object_detection.msg
import tf
from dynamixel_controllers.srv import SetTorqueLimit
from controller.manipulator_controller import ManipulateController
from tabletop.srv import TabletopObjectDetection
import numpy

isFirst = True
#global INIT_HAND
#INIT_HAND = 0.0
#global RISE_HAND_RIGHT 
#RISE_HAND_RIGHT = -1.82
#global RISE_HAND_LEFT
#RISE_HAND_LEFT = 2.7

##-------------------------------------------------------##

def callback(data):
    print 'c_1'
    global isFirst
    global pub_right_hand
    global pub_left_hand
    global pub_torso
    global arm
    arm = 'right_arm'
    #global INIT_HAND, RISE_HAND_RIGHT, RISE_HAND_LEFT
    global mnplctrl    
    global torso_h
    global pub_torso
    if data.axes[2]<1 or data.axes[5]<1: #choose_hand
        if data.axes[2]<1: #LT #left_hand
            arm = 'left_arm'
            print 'Use left arm'

        elif data.axes[5]<1: #RT #right_hand
            arm = 'right_arm'
            print 'Use right arm'

    elif data.buttons[2]==1 or data.buttons[3]==1:
        if isFirst:
            mnplctrl = ManipulateController()
            mnplctrl.init_controller()
            isFirst = False
        #rospy.init_node('hand_controller')

        if data.buttons[3]==1: #Y #rise_hand_up
            if arm == 'right_arm':
                print 'Right arm up'
                mnplctrl.static_pose('right_arm',"right_respect")
                #jointstatus = mnplctrl.getjointstatus(hand)
                #mnplctrl.setjoint("right_shoulder_1_joint" ,mnplctrl.getjointstatus["right_shoulder_1_joint"]+mnplctrl.RISE_HAND_RIGHT)
                #mnplctrl.setjoint("right_shoulder_2_joint" ,jointstatus)
                #mnplctrl.setjoint("right_elbow_joint",0.0)
                #if jointstatus["right_elbow_joint"] >= 0.00:
                #   mnplctrl.setjoint('right_elbow_joint',mnplctrl.URDF_ELBOW_LIMIT)
                #else:
                #    mnplctrl.setjoint("right_elbow_joint",jointstatus["right_elbow_joint"] + 0.1 )
                #mnplctrl.setjoint('right_wrist_1_joint',0.00)
                #mnplctrl.setjoint('right_wrist_2_joint',0.00)
                #mnplctrl.setjoint('right_wrist_3_joint',0.00)
                
                #pub_right_hand.publish(Float64(mnplctrl.RISE_HAND_RIGHT))
            elif arm == 'left_arm':
                print 'Left arm up'
                mnplctrl.static_pose('left_arm',"left_rise_up")
            #    pub_left_hand.publish(Float64(mnplctrl.RISE_HAND_LEFT))
        elif data.buttons[2]==1: #X #normal_hand
            if arm == 'right_arm':
                print 'Right arm normal'
                mnplctrl.static_pose('right_arm',"right_normal")
            if arm == 'left_arm':
                print 'Left arm normal'
                mnplctrl.static_pose('left_arm',"left_normal")

##-------------------------------------------------------##

def start_joy():
    global pub_right_hand
    global pub_left_hand
    print 'b_1'
    global mnplctrl

    rospy.init_node('start_joy',anonymous=True)
    print 'b_2' 
    rospy.Subscriber('joy',Joy,callback)
    rospy.spin()
    print 'b_3'

##-------------------------------------------------------##

if __name__ == '__main__':
    print 'a_1'
    try:
        start_joy()
    except rospy.ROSInterruptException:
        pass
    print 'a_2'
