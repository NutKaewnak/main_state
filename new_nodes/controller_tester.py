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
from dynamixel_controllers.srv import SetTorqueLimit
from controller.manipulator_controller import ManipulateController
from tabletop.srv import TabletopObjectDetection
import numpy

framecount = 0

mnplctrl = None
pos = []
pub = None
enable = False

finish = False

# def callback(data):
#     global framecount,enable,pos
#     position = geometry_msgs.msg.Point()
#     position = data.centriod
#     framecount += 1
#     if framecount < 5:
#         #print "msg counting " + str(framecount)
#         return
#     if framecount is 5:
#         enable = True
#         rospy.loginfo('------------start  picking----------')
#         print "location : x = " + str(position.x) + "  y= " + str(position.y) + " z= " + str(position.z) 
#         pos.append(position.x)
#         pos.append(position.y)
#         pos.append(position.z)
#     #mnplctrl.pick("right_arm",[position.x-0.2,position.y,position.z+0.05],[0.0,0.0,0.0],"object","table","base_link")
#     #mnplctrl.robot.right_arm.set_support_surface_name("table")
#     #mnplctrl.robot.right_arm.pick("object")
#     #moveit_commander.


def adding_fake_object():
    global mnplctrl,pub
    ##publishing object
    mnplctrl.scene.remove_world_object("pole")
    mnplctrl.scene.remove_world_object("table")
    mnplctrl.scene.remove_world_object("object")

    # publish a demo scene
    p = geometry_msgs.msg.PoseStamped()
    p.header.frame_id = 'base_link'
    p.pose.position.x = 0.7
    p.pose.position.y = 1
    p.pose.position.z = 0.85
    p.pose.orientation.w = 1.0
    mnplctrl.scene.add_box("pole", p, (0.3, 0.1, 1.0))
    p.pose.position.x = 0.725
    p.pose.position.y = -0.2
    p.pose.position.z = 0.175
    mnplctrl.scene.add_box("table", p, (0.5, 1.5, 0.35))

    p.pose.position.x = 0.7
    p.pose.position.y = 0
    p.pose.position.z = 0.5
    mnplctrl.scene.add_box("object", p, (0.15, 0.06, 0.3))
    
##---------------------------------------------------------------##
def set_torque_limit(limit = 0.5):
    rospy.wait_for_service('/dynamixel/right_gripper_joint_controller/set_torque_limit')
    try:
        rospy.loginfo('settorque')
        setTorque = rospy.ServiceProxy('/dynamixel/right_gripper_joint_controller/set_torque_limit', SetTorqueLimit)
        respTorque = setTorque(limit)
    except rospy.ServiceException, e:
        rospy.logwarn("Service Torque call failed " + str(e))


def pick_tester():
    global mnplctrl,pub,pos
    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('controller_tester')

    pub = rospy.Publisher('/dynamixel/right_gripper_joint_controller/command', Float64)

    rospy.loginfo("---BUILDING SCENE----")
    rospy.sleep(3.0)

    rospy.loginfo("--INIT--")
    mnplctrl.pickobject_init("right_arm", "object", [0.70, -0.22 + 0.10, 0.95])
    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("---pregrasp---")
    mnplctrl.pickobject_pregrasp()
    rospy.loginfo("Press any key to Continue")
    raw_input()
    

    # rospy.loginfo("go to in front of object")
    # mnplctrl.pickobject_movetoobjectfront()
    # rospy.loginfo("--complete--")
    # raw_input()

    rospy.loginfo("---Opening Gripper---")
    #mnplctrl.pickobject_opengripper()

    pub.publish(Float64(mnplctrl.GRIPPER_OPENED))

    rospy.loginfo("---Complete Opening Gripper----")


    rospy.loginfo("Press any key to Continue")
    raw_input()
    
    rospy.loginfo("----movetoobjectfront----")
    mnplctrl.pickobject_movetoobjectfront()
    rospy.loginfo("movetoobjectfront Complete")

    rospy.loginfo("Press any key to Continue")
    raw_input()




    rospy.loginfo("----Reaching to Object----")
    mnplctrl.pickobject_reach()
    rospy.loginfo("Reaching Complete")

    rospy.loginfo("Press any key to Continue")
    raw_input()
    
    rospy.loginfo("---GRASPING---")
    #mnplctrl.pickobject_grasp()
    
    set_torque_limit()
    pub.publish(Float64(mnplctrl.GRIPPER_CLOSED))

    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("---After Grasp---")
    mnplctrl.pickobject_after_grasp()

    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("---pregrasp---")
    mnplctrl.pickobject_pregrasp()
    rospy.loginfo("Press any key to Continue")
    raw_input()

    rospy.loginfo("----Return To Normal-----")
    mnplctrl.static_pose("right_arm","right_init_picking")
    rospy.loginfo("---FINISH----")
    

    raw_input()

    rospy.loginfo("---Opening Gripper---")
    #mnplctrl.pickobject_opengripper()

    pub.publish(Float64(mnplctrl.GRIPPER_OPENED))

    rospy.loginfo("---Complete Opening Gripper----")

    rospy.spin()
    mnplctrl.__del__()

def module_tester():

    global mnplctrl
    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('controller_tester')
    rospy.sleep(3.0)
    mnplctrl.move_relative('right_arm',[0,0,0],numpy.radians([24.255,0,0]))
    rospy.spin()

##---------------------------------------------------------------##

def boolcallback(data):
    global finish
    if data.data == True:
        rospy.loginfo('---ENDING WIP---')
        finish = True
    else:
        rospy.loginfo('Wrong input')


def robozoo_tester():
    global mnplctrl,finish

    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('robozoo')
    rospy.Subscriber("wip_done", Bool, boolcallback)

    rospy.loginfo('1st:right_init_picking')
    mnplctrl.static_pose('right_arm',"right_init_picking")
    rospy.loginfo('executing:right_init_picking')
    #raw_input()
    rospy.sleep(4.00)

    rospy.loginfo('2nd:right_pregrasp')
    mnplctrl.static_pose('right_arm',"right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    #raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('3rd:right_wip_prepare')
    mnplctrl.static_pose('right_arm',"right_wip_prepare")
    rospy.loginfo('executing:right_wip_prepare')
    #raw_input()
    rospy.sleep(4.00)
    
    #while not rospy.is_shutdown():
    while (not finish) and (not rospy.is_shutdown()):
        rospy.loginfo('wip1')
        mnplctrl.static_pose('right_arm',"right_wip_1")
        #raw_input()
        rospy.sleep(1.50)
        rospy.loginfo('wip2')
        mnplctrl.static_pose('right_arm',"right_wip_2")
        #raw_input()
        rospy.sleep(1.50)

    rospy.loginfo('4th : right_wip_retreat')
    mnplctrl.static_pose('right_arm',"right_wip_retreat")
    rospy.loginfo('executing:right_wip_retreat')
    #raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('5th : right_pregrasp')
    mnplctrl.static_pose('right_arm',"right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    #raw_input()
    rospy.sleep(4.00)
    rospy.loginfo('6th : right_init_picking')
    mnplctrl.static_pose('right_arm',"right_init_picking")
    rospy.loginfo('--Finish--')
   
callback = None



def open_challenge_tester():
    global mnplctrl,callback
    y_offset = -0.1
    z_offset = 0.15

    obj_x = 0.6
    obj_y = 0.0
    obj_z = 0.7

    mnplctrl = ManipulateController()
    mnplctrl.init_controller()
    rospy.init_node('openchallenge')
    
    response = callback


    rospy.loginfo('1st:right_init_picking')
    mnplctrl.static_pose('right_arm',"right_init_picking")
    rospy.loginfo('executing:right_init_picking')
    raw_input()

    rospy.loginfo('2nd:right_pregrasp')
    mnplctrl.static_pose('right_arm',"right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    raw_input()
    
    rospy.loginfo('3rd:reach to the top of object')
    mnplctrl.manipulate('right_arm',[obj_x,obj_y + y_offset, obj_z  + z_offset],[-1.57,0,0],[0.05,0.1])
    rospy.loginfo('executing:reach to the top of object')
    raw_input()

    rospy.loginfo('4th movedownward')
    mnplctrl.move_relative('right_arm',[0,0,-z_offset],[0,0,0])
    rospy.loginfo('executing: movedownward')
    raw_input()

    rospy.loginfo('5th Crack')
    mnplctrl.movejoint("right_gripper_joint",mnplctrl.GRIPPER_CLOSED)
    rospy.loginfo('executing: Crack')
    raw_input()

    rospy.loginfo('6th Release')
    mnplctrl.movejoint("right_gripper_joint",mnplctrl.GRIPPER_OPENED)
    rospy.loginfo('executing: Release')
    raw_input()

    rospy.loginfo('7th going_up')
    mnplctrl.move_relative('right_arm',[0,0,z_offset],[0,0,0])
    rospy.loginfo('executing: going_up')
    raw_input()


    rospy.loginfo('8th:right_pregrasp')
    mnplctrl.static_pose('right_arm',"right_pregrasp")
    rospy.loginfo('executing:right_pregrasp')
    raw_input()

    rospy.loginfo('9th:END')
    mnplctrl.static_pose('right_arm',"right_normal")
    rospy.loginfo('executing:END')
    raw_input()






if __name__=='__main__':
    global callback
    try:
        pick_tester()
        #module_tester()
        #robozoo_tester()
        #rospy.wait_for_service('tabletop_object_detection')
        # try:
        #     callback = rospy.ServiceProxy('tabletop_object_detection', TabletopObjectDetection)
        # except rospy.ServiceException, e:
        #     print "Service call failed: %s",e
        # pick_tester()

    except rospy.ROSInterruptException:
        pass