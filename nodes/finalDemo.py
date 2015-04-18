#!/usr/bin/env python
# TODO reproduce state
from subprocess import call

import rospy
import roslib


roslib.load_manifest('main_state')
roslib.load_manifest('manipulator')
from include.function import *
#from include.publish import *
from std_msgs.msg import String
from geometry_msgs.msg import Vector3

state = 'init'
startTime = 0
count = 0
points = []
value = ''


def cb_voice(data):
    main_state('voice', data.data)


def cb_color_track(data):
    main_state('color_track', data)


def cb_mani(data):
    main_state('manipulate', data.data)


def cb_object_point(data):
    main_state('object', data.data)


def main_state(device, data):
    global state, startTime, count, points, value
    rospy.loginfo("state:" + state + " from:" + device + " " + str(data))
    print state	
    if (state == 'init'):
        if (device == 'voice' and ('breakfast' in data)):
            call(["espeak", "-ven+f4", "i will make you a breakfast", "-s 150"])
	    findObjectPointPublisher.publish('start')  #start searching object
            state = 'searchingCornflake'

    elif (state == 'searchingCornflake'):
        if (device == 'recognition'):
            call(["espeak", "-ven+f4", "Searching cornflake", "-s 150"])  #milk + cornflake
            object = []
	    if(data.isMove):
	    	#to go closer
	    	pass
	    else:
	    	objects = data.objects
		for obj in objects:
			if obj.catagory == desiredObject_1:
				centroidVector = Vector3()
				centroidVector.x = obj.point.x
				centroidVector.y = obj.point.y
				centroidVector.z = obj.point.z
	    			#pickObjectPublisher.publish(centroidVector)
            			state = 'graspingCornflake'

    elif (state == 'graspingCornflake'):
        #if (device == 'manipulate' and data == 'finish'): #finish grasping Cornflake
            state = 'trackingBowl'

    elif (state == 'trackingBowl'):
        call(["espeak", "-ven+f4", "searching a bowl", "-s 150"])
        if (device == 'color_track'):
            #TODO use hough for more precise point?
            #Hind send_object_point.publish(data)  #send point above a bowl to pour
            call(["espeak", "-ven+f4", "pouring", "-s 150"])
            state = 'discardCornflake'

    elif (state == 'discardCornflake'):
        if (device == 'manipulate' and data == 'finish'): #after pouring
            call(["espeak", "-ven+f4", "discard cornflake", "-s 150"])  #discard cornflake in hand for grasp milk
            act.publish('walking_for_drop')  #<<- drop command
            state = 'searchingMilk'

    elif (state == 'searchingMilk'):
        if (device == 'manipulate' and data == 'finish'): #finish discard
        	if (device == 'recognition'):
            		call(["espeak", "-ven+f4", "Searching cornflake", "-s 150"])  #milk + cornflake
            		object = []
			if(data.isMove):
	    			#to go closer
	    			pass
			else:
				objects = data.objects
				for obj in objects:
					if obj.catagory == desiredObject_2:
						centroidVector = Vector3()
						centroidVector.x = obj.point.x
						centroidVector.y = obj.point.y
						centroidVector.z = obj.point.z
	   					#pickObjectPublisher.publish(centroidVector)
	    					state = 'graspingMilk'

    elif (state == 'graspingMilk'):
        if (device == 'manipulate' and data == 'finish'):
            state = 'trackingBowl_2'

    elif (state == 'trackingBowl_2'):
        call(["espeak", "-ven+f4", "searching a bowl", "-s 150"])
        if (device == 'color_track'):
            #TODO use hough for more precise point?
            #TODO 2? Could we use the first point? and shall we?
            #Hind send_object_point.publish(data) #send point above a bowl to pour
            call(["espeak", "-ven+f4", "pouring", "-s 150"])
            state = 'discardMilk'

    elif (state =='discardMilk'):
        if (device == 'manipulate' and data == 'finish'):
            state = 'serve'

    elif (state == 'serve'):
            call(["espeak", "-ven+f4", "the breakfast is served", "-s 150"])
            act.publish('walking_for_drop')
            state = 'drop'

    elif (state == 'drop'):  #send normal action and release grasping
        if (device == 'manipulate' and data == 'finish'):
            state = 'finish'

    elif (state == 'finish'):
        pass


def main():
    global findObjectPointPublisher, send_object_point, point_pub_vec, point_pub_vec_split, act
    rospy.init_node('finalDemo')
    rospy.Subscriber("/Tracking", Vector3, cb_color_track)  #Tracking (point x,y,z)
    rospy.Subscriber("/manipulator/is_fin", String, cb_mani)  #manipulate (string 'isfin' ?)
    rospy.Subscriber("/voice/output", String, cb_voice)  #voice
    rospy.Subscriber("/center_pcl_object", String, cb_object_point)  #Recieve object point (String x,y,z,x,y,z)

    act = rospy.Publisher('/manipulator/action', String)
    send_object_point = rospy.Publisher('/manipulator/object_point', Vector3)  #transform
    findObjectPointPublisher = rospy.Publisher('/localization', String)  #trigger to start track object
    point_pub_vec = rospy.Publisher('/manipulator/object_point', Vector3)
    point_pub_vec_split = rospy.Publisher('/manipulator/object_point_split', String)

    rospy.spin()


if __name__ == '__main__':
    try:
        delay = Delay()
        #publish = Publish()
        main()
    except rospy.ROSInterruptException:
        pass
