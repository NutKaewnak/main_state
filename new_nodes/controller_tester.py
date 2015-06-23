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

pub = None

def callback(data):
    global framecount
    position = geometry_msgs.msg.Point()
    position = data.centriod
    framecount += 1
    if framecount is not 3:
        print "msg counting " + str(framecount)
        return
    rospy.loginfo('------------start  picking----------')
    print "location : x = " + str(position.x) + "  y= " + str(position.y) + " z= " + str(position.z) 
    mnplctrl.pick("right_arm",[position.x-0.2,position.y,position.z+0.05],[0.0,0.0,0.0],"object","table","base_link")
    #mnplctrl.robot.right_arm.set_support_surface_name("table")
    #mnplctrl.robot.right_arm.pick("object")



def adding_fake_object():
    global mnplctrl,pub

    co = moveit_msgs.msg.CollisionObject()
    co.header.stamp = rospy.Time.now()
    co.header.frame_id = "base_link"

    #remove pole
    co.id = "table"
    co.operation = moveit_msgs.msg.CollisionObject.REMOVE
    pub.publish(co)

    co.operation = moveit_msgs.msg.CollisionObject.ADD
    solidprim = shape_msgs.msg.SolidPrimitive()
    solidprim.type = shape_msgs.msg.SolidPrimitive.BOX
    solidprim.dimensions.append(std_msgs.msg.Float64(0.3))
    solidprim.dimensions.append(std_msgs.msg.Float64(0.1))
    solidprim.dimensions.append(std_msgs.msg.Float64(1.0))
    co.primitives.append(solidprim)
    prim_pose = geometry_msgs.msg.Pose()
    prim_pose.position.x = 0.7
    prim_pose.position.y = 0.1
    prim_pose.position.z = 0.85
    prim_pose.orientation.w = 1.0
    co.primitive_poses.append(prim_pose)
    pub.publish(co)
    rospy.loginfo("ADDING TABLE")

    co = moveit_msgs.msg.CollisionObject()
    co.header.stamp = rospy.Time.now()
    co.header.frame_id = "base_link"

    co.id = "object"
    co.operation = moveit_msgs.msg.CollisionObject.REMOVE
    pub.publish(co)




    ##publishing object
    # mnplctrl.scene.remove_world_object("pole")
    # mnplctrl.scene.remove_world_object("table")
    # mnplctrl.scene.remove_world_object("object")

    # # publish a demo scene
    # p = geometry_msgs.msg.PoseStamped()
    # p.header.frame_id = 'base_link'
    # p.pose.position.x = 0.7
    # p.pose.position.y = 1
    # p.pose.position.z = 0.85
    # p.pose.orientation.w = 1.0
    # mnplctrl.scene.add_box("pole", p, (0.3, 0.1, 1.0))
    # p.pose.position.x = 0.725
    # p.pose.position.y = -0.2
    # p.pose.position.z = 0.175
    # mnplctrl.scene.add_box("table", p, (0.5, 1.5, 0.35))

    # p.pose.position.x = 0.7
    # p.pose.position.y = 0
    # p.pose.position.z = 0.5
    # mnplctrl.scene.add_box("object", p, (0.15, 0.06, 0.3))
    


def tester():
    global mnplctrl,pub
    
    
    mnplctrl = ManipulateController()

    rospy.init_node('controller_tester')

    #rospy.Subscriber("/object_shape", object_detection.msg.ObjectDetection, callback)
    pub = rospy.Publisher('collision_object', moveit_msgs.msg.CollisionObject, queue_size=10)
    rospy.loginfo("BUILDING SCENE")

    #adding_fake_object()
    #mnplctrl.scene.remove_world_object("pole")
    #mnplctrl.scene.remove_world_object("table")
    #mnplctrl.scene.remove_world_object("object")
   
    # publish a demo scene



    # rospy.sleep(5)
    mnplctrl.static_pose("right_arm","right_normal")
    #mnplctrl.static_pose("left_arm","left_normal")
    
    
    rospy.sleep(5)
    
    rospy.loginfo("Starting manipulation")
    mnplctrl.pickobject_pregrasp("right_arm","object",[0.7,0,0.5])
    
    rospy.sleep(5)
    rospy.loginfo("Opening Gripper")
    mnplctrl.pickobject_opengripper()

    rospy.sleep(5)
    rospy.loginfo("Reaching to Object")
    mnplctrl.pickobject_reach()
    rospy.sleep(5)
    rospy.loginfo("---GRASPING---")
    mnplctrl.pickobject_grasp()

    
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