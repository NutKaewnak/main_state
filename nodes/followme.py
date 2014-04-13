#!/usr/bin/env python
import rospy
import roslib
import time
import math
from subprocess import call
roslib.load_manifest('main_state')

from include.function import *
from include.publish import *

from std_msgs.msg import String,Bool
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D

state = 'init'
robot_pos = []
startTime = 0

def cb_voice(data):
    main_state('voice',data.data)

def cb_base(data):
    main_state('base',data.data)

def cb_base_pos(data):
    global robot_pos
    pos = data
    if(len(robot_pos) == 0):
	robot_pos.append(pos)
    else:
        last_pos = robot_pos[-1]
	dif = math.sqrt((last_pos.x-pos.x)**2 + (last_pos.y-pos.y)**2)
	if(dif >= 0.15):
		robot_pos.append(pos)
    temp = robot_pos
    for _pos in robot_pos:
	dif = math.sqrt((_pos.x-pos.x)**2 + (_pos.y-pos.y)**2)
	if(dif >= 2.0):
		temp = temp[1:]
    robot_pos = temp
    
def cb_follow(data):
    main_state('follow',data)

def main_state(device,data):
	global state,startTime
        if(device == 'follow'):
		pass
	else:
		rospy.loginfo("state:"+state+" from:"+device+" "+data)
	if(state == 'init'):
		if(device == 'voice' and ('follow me' in data)):
                        call(["espeak","-ven+f4","i will follow you","-s 150"])
			state = 'follow_phase_1'
	elif(state == 'follow_phase_1'):
		if(device == 'follow'):
			if(data.text_msg == 'lost'):
				data.text_msg = 'stop'
                        publish.base.publish(data)
			#if(data.text_msg == 'stop'):
			#	data.text_msg = 'clear'
                        #	pub['base'].publish(data)
		elif(device == 'voice' and ('get out' in data)):
			state = 'get_out_lift'
                        publish.base.publish(NavGoalMsg('clear','absolute',robot_pos[0]))
	elif(state == 'get_out_lift'):
		if(device == 'base' and data == 'SUCCEEDED'):
			state = 're_calibrate'
                        call(["espeak","-ven+f4","please come in front of me","-s 150"])
			delay.waiting(5)
	elif(state == 're_calibrate'):
		if(delay.isWaitFinish()):
			state = 'follow_phase_2'
                        publish.follow_init.publish(Bool(True))
	elif(state == 'follow_phase_2'):
		if(device == 'follow'):
			if(data.text_msg == 'lost'):
				data.text_msg = 'stop'
                        #pub['base'].publish(data)
			publish.base.publish(data)

def main():
    rospy.init_node('main_state')

    rospy.Subscriber("/base/is_fin", String, cb_base)
    rospy.Subscriber("/follow/point", NavGoalMsg, cb_follow)
    rospy.Subscriber("/base/base_pos", Pose2D, cb_base_pos)
    rospy.Subscriber("/voice/output", String, cb_voice)
    rospy.spin()

if __name__ == '__main__':
    try:
	delay = Delay()
	publish = Publish()
        main()
    except rospy.ROSInterruptException:
        pass
