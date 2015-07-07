#!/usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
import std_msgs.msg
import shape_msgs.msg
import geometry_msgs.msg
import trajectory_msgs.msg
import object_detection.msg
import tf
from controller.manipulator_controller import ManipulateController

framecount = 0

mnplctrl = None
pos = []
pub = None
enable = False

def callback(data):
    global framecount,enable,pos
    position = geometry_msgs.msg.Point()
    position = data.centriod
    framecount += 1
    if framecount < 5:
        #print "msg counting " + str(framecount)
        return
    if framecount is 5:
        enable = True
        rospy.loginfo('------------start  picking----------')
        print "location : x = " + str(position.x) + "  y= " + str(position.y) + " z= " + str(position.z) 
        pos.append(position.x)
        pos.append(position.y)
        pos.append(position.z)
    #mnplctrl.pick("right_arm",[position.x-0.2,position.y,position.z+0.05],[0.0,0.0,0.0],"object","table","base_link")
    #mnplctrl.robot.right_arm.set_support_surface_name("table")
    #mnplctrl.robot.right_arm.pick("object")
    #moveit_commander.


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
    


def tester():
    global mnplctrl,pub,pos
    mnplctrl = ManipulateController()
    rospy.init_node('controller_tester')
    #pub = rospy.Publisher('collision_object', moveit_msgs.msg.CollisionObject, queue_size=10)
    rospy.loginfo("---BUILDING SCENE----")
    # rospy.sleep(5)
    # mnplctrl.scene.remove_world_object("pole")
    # mnplctrl.scene.remove_world_object("table")
    # mnplctrl.scene.remove_world_object("object")
   
    # adding_fake_object()
    #rospy.sleep(2)
    rospy.loginfo("--Normal--")
    mnplctrl.static_pose("right_arm","right_normal")
    #mnplctrl.static_pose("left_arm","left_normal")
    rospy.sleep(10)

    rospy.loginfo("Complete Normal")
    #rospy.Subscriber("/object_shape", object_detection.msg.ObjectDetection, callback)
    #while enable is False:
    #    pass
        
    # rospy.loginfo("Starting manipulation")
    # #mnplctrl.pickobject_pregrasp("right_arm","object",[pos[0],pos[1],pos[2]])
    # mnplctrl.pickobject_pregrasp("right_arm","object",[0.62,0.0,0.95])
    
    # rospy.sleep(15)
    
    # rospy.loginfo("Opening Gripper")
    # mnplctrl.pickobject_opengripper()

    # rospy.sleep(15)
    # rospy.loginfo("Reaching to Object")
    # mnplctrl.pickobject_reach([0.02,0.05])
    

    # rospy.sleep(15)
    # rospy.loginfo("---GRASPING---")
    # mnplctrl.pickobject_grasp()

    
   # rospy.sleep(2.0)
    # print "-----start----"
    # Manually pick in simulation
    # mnplctrl.pick("right_arm",[0.50,-0.15,0.55],[0.0,0.0,0.0],"object","table","base_link")

    # print "-----------finish pick----------"
    rospy.spin()
    mnplctrl.__del__()

if __name__=='__main__':
    try:
        tester()
    except rospy.ROSInterruptException:
        pass