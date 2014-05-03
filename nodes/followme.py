#!/usr/bin/env python
import rospy
import roslib
import time
import math
from subprocess import call
roslib.load_manifest('main_state')

from include.function import *
from include.publish import *
from include.base_state import *

from std_msgs.msg import String,Bool
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D


class followme(BaseState):
    
    def __init__(self):
        BaseState.__init__(self)
        self.robot_pos = []
        #self.robot_pos.append(0)
        #self.state = 'init'
        rospy.loginfo('Start Follow Me State')
        rospy.Subscriber("/base/base_pos", Pose2D, self.cb_base_pos)
        rospy.Subscriber("/scan/wall_people", Pose2D, self.cb_wall_people)
        self.robot_pos_wall = None
        rospy.Subscriber("/gesture/point", PointStamped, self.cb_gesture)
        rospy.Subscriber("pan_tilt_main_state",Quaternion, self.cb_pan_tilt_main)
        self.publish = Publish()
        self.currentAngle = -90*math.pi/180
        rospy.spin()

    def cb_pan_tilt_main(self, data):
        self.perform_state('pan_tilt', data)

    def cb_base_pos(self,data):
        pos = data
        if len(self.robot_pos) == 0:
            self.robot_pos.append(pos)
        else:
            last_pos = self.robot_pos[-1]
        dif = math.sqrt((last_pos.x-pos.x)**2 + (last_pos.y-pos.y)**2)
        if dif >= 0.15:
            self.robot_pos.append(pos)
        temp = self.robot_pos
        for _pos in self.robot_pos:
            dif = math.sqrt((_pos.x-pos.x)**2 + (_pos.y-pos.y)**2)
            if dif >= 2.3:
                temp = temp[1:]
        self.robot_pos = temp

    def cb_wall_people(self,data):
        pos_ = Pose2D()
        pos_.x = data.x + 2.0
        pos_.y = data.y - 1.0
        pos_.theta = data.theta + 3.14/2
        self.robot_pos_wall = pos_
        self.main(Devices.foot_detect,pos_)

    def cb_gesture(self,data):
        print "in cb_gesture cb"
        self.main('gesture',"%f,%f,%f" % (data.point.x,data.point.y,data.point.z))

    def main(self,device,data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:")
        if self.state == 'init':
            if device == Devices.voice and ('follow me' in data):
                Publish.speak("I will follow you.")
                self.state = 'follow_phase_2'
        elif self.state == 'follow_phase_1':
            if device == Devices.follow:
                if data.text_msg == 'lost':
                    self.speak("lost master")
                    data.text_msg = 'stop'
                Publish.move_robot(data)
            if device == 'pan_tilt':
                Publish.pan_tilt_cmd.publish(data)
            elif device == Devices.voice and ('leave the elevator' in data):
                self.speak("i will get out elevator")
                self.state = 'get_out_lift'
                Publish.move_absolute(self.robot_pos[0])
        elif self.state == 'get_out_lift':
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 're_calibrate'
                self.speak("please come in front of me.")
        elif self.state == 're_calibrate':
            self.publish.follow_init.publish(Bool(True))
            self.state = 'follow_phase_2'
        elif self.state == 'follow_phase_2':
            if device == Devices.follow:
                if data.text_msg == 'lost':
                     data.text_msg = 'stop'
                Publish.move_robot(data)
            elif device == 'pan_tilt':
                Publish.pan_tilt_cmd.publish(data)
            elif device == Devices.foot_detect:
                rospy.loginfo(type(data))
                rospy.loginfo(str(data))
                #Publish.move_relative(data)
                Publish.move_absolute(data)
                Publish.set_neck(0.0, 0.0, 0.0)
                self.currentAngle = -90*math.pi/180
                self.timer = Delay()
                self.state = 'Seachgesture'
                self.speak("Please wave your hand.")
                self.wait(6)
        elif self.state == 'Seachgesture':
            if device == 'gesture':
                self.speak("I see you.")
                x,y,z = data.split(',')
                x = float(z) * math.cos(self.currentAngle)
                y = float(z) * math.sin(self.currentAngle)
                Publish.move_relative(float(x),float(y), 0)
                self.state = 're_calibrate_2'
            if not self.timer.is_waiting():
                self.currentAngle += 0.3
                print self.currentAngle
                self.timer.wait(3)
                if self.currentAngle >= 90*math.pi/180:
                    self.speak("I did not found .")
                    self.state = 'error'
                else:
                    Publish.set_neck(0, 0, self.currentAngle)
        elif self.state == 're_calibrate_2':
            if device == Devices.base and data == 'SUCCEEDED':
                #self.speak("please come in front of me.")
                self.wait(2)
                self.publish.follow_init.publish(Bool(True))
                self.state = 'follow_phase_3'
        elif self.state == 'follow_phase_3':
            if device == Devices.follow:
                Publish.move_robot(data)
            elif device == 'pan_tilt':
                Publish.pan_tilt_cmd.publish(data)

#state = 'init'
#self.robot_pos = []
#startTime = 0

#def cb_voice(data):
#    main_state('voice',data.data)

#def cb_base(data):
#    main_state('base',data.data)

#def cb_follow(data):
#    main_state('follow',data)


#def main():
#    rospy.init_node('main_state')
#    rospy.Subscriber("/base/is_fin", String, cb_base)
#    rospy.Subscriber("/follow/point", NavGoalMsg, cb_follow)
#    rospy.Subscriber("/base/base_pos", Pose2D, cb_base_pos)
#    rospy.Subscriber("/voice/output", String, cb_voice)
#    rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        followme()
    except rospy.ROSInterruptException:
        pass
