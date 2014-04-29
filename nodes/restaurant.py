#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *

roslib.load_manifest('main_state')

from include.function import *
from include.publish import *
from include.reconfig_kinect import *
from std_msgs.msg import String, Bool
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D, Vector3
from math import pi

# predefine
#object_list = ['green cup','blue cup' ,'pink cup' ,'blue mug' ,'ping mug' ,'cock' ,'frog' ,'owl' ,'green tea' ,'energy drink' ,'banana juice' ,'sprite' ,'coffee' ,'cappucino' ,'max coffee' ,'blue chips' ,'orange chips' ,'pringles' ,'black light' ,'blue light' ,'bottle' ,'blue brush' ,'red brush' ,'pen holder'] 
#location_list = [ 'drink shelf' ,'snack shelf' ,'food shelf' ,'location one' ,'location two' ,'location three']
location_list = {}
#object_location = {'green cup':'cup shelf','blue cup':'cup shelf','pink cup':'cup shelf','blue mug':'cup shelf','pink mug':'cup shelf','cock':'toy shelf','frog':'toy shelf','owl':'toy shelf','green tea':'drink shelf','energy drink':'drink shelf','banana juice':'drink shelf','sprite':'drink shelf','coffee':'drink shelf','cappucino':'drink shelf','max coffee':'drink shelf','blue chips':'snack shelf','orange chips':'snack shelf','pringles':'snack shelf','black light':'tool shelf','blue light':'tool shelf','bottle':'tool shelf','blue brush':'tool shelf','red brush':'tool shelf','pen holder':'tool shelf'}
catagory_list = {'snacks': 'snack shelf', 'food': 'food shelf', 'drink': 'drink shelf'}
object_list = {}
# for robot memorize
location_pos = {}
robot_pos = None
command_list = []
current_location = 0
current_command = 0
location_count = 0


class Command:
    def __init__(self, locationName, objectName):
        self.locationName = locationName
        self.objectName = objectName

def main_state(device, data):
    global state, location_list, temp, command_list, location_count, current_command

    if (state == 'waitForLocationName'):
        publish.robot_stop()
        if (device == 'voice'):
            for i in location_list.keys():
                if (i in data):
                    temp = i
                    call(["espeak", "-ven+f4", "this is " + i + " yes or no ", "-s 110"])
                    state = 'confirmLocationName'
        elif (device == 'voice' and ('follow me' in data)):
            call(["espeak", "-ven+f4", "i will follow you", "-s 110"])
            state = 'follow_phase_1'
    elif (state == 'confirmLocationName'):
        publish.robot_stop()
        if (device == 'voice' and ('robot yes' in data)):
            location_list[temp] = NavGoalMsg('clear', 'absolute', robot_pos)
            call(["espeak", "-ven+f4", "i remember " + temp, "-s 110"])
            location_count += 1
            state = 'follow_phase_1'
        elif (device == 'voice' and ('robot no' in data)):
            call(["espeak", "-ven+f4", "where are we", "-s 110"])
            state = 'waitForLocationName'
    elif (state == 'waitForCommand'):
        publish.robot_stop()
        if (len(command_list) == 3):
            current_command = 0
            publish.base.publish(
                location_list[catagory_list[object_list[command_list[current_command].objectName].catagory]])
            delay.delay(3)
            state = 'gotoObjectLocation'
        elif (device == 'voice'):
            for i in location_list.keys():
                if (i in data):
                    for j in object_list.keys():
                        if (j in data):
                            temp = Command(i, j)
                            call(["espeak", "-ven+f4", "bring " + j + " to " + i + " yes or no ", "-s 110"])
                            state = 'confirmCommand'
                            return None
    elif (state == 'confirmCommand'):
        publish.robot_stop()
        if (device == 'voice' and ('robot yes' in data)):
            command_list.append(temp)
            call(["espeak", "-ven+f4", "i will bring " + temp.objectName + " to " + temp.locationName, "-s 110"])
            state = 'waitForCommand'
        elif (device == 'voice' and ('robot no' in data)):
            call(["espeak", "-ven+f4", "please say again", "-s 110"])
            state = 'waitForCommand'
    elif (state == 'gotoObjectLocation'):
        if (device == 'base' and data == 'SUCCEEDED'):
            call(["espeak", "-ven+f4",
                  "i am at " + catagory_list[object_list[command_list[current_command].objectName].catagory], "-s 110"])
            publish.object_search.publish(command_list[current_command].objectName)
            reconfig.changeDepthResolution(2)
            state = 'searchObject'
    elif (state == 'searchObject'):
        reconfig.changeDepthResolution(2)
        if (device == 'object'):
            if (data == 'no'):
                publish.object_search.publish(command_list[current_command].objectName)
            else:
                objectName, x, y, z = data.split(',')
                call(['espeak', 'i found' + command_list[current_command].objectName, '-ven+f4', '-s 120'])
                publish.manipulator_point.publish(Vector3(float(x), float(y), float(z)))
                delay.delay(3)
                state = 'getObject'
    elif (state == 'getObject'):
        if (device == 'manipulator' and data == 'finish'):
            reconfig.changeDepthResolution(8)
    elif (state == 'finishGrasp'):
        stopTime = time.localtime()
        if (time.mktime(stopTime) - time.mktime(startTime) >= 10.0):
            current_location = command_list[current_command][0]
            pub['base'].publish(location_pos[current_location])
            state = 'gotoTable'
    elif (state == 'gotoTable'):
        if (device == 'base' and data == 'SUCCEEDED'):
            call(["espeak", "-ven+f4", "i am at " + current_location, "-s 110"])
            # grasp
            current_command += 1
            current_location = object_location[command_list[current_command][1]]
            pub['base'].publish(location_pos[current_location])
            state = 'gotoLocation'

def restaurant(BaseState):
    def __init__(self):
        BaseState.__init__(self)

        Publish.set_height(1.27)
        self.reconfig.changeDepthResolution(8)
        Publish.set_manipulator_action('walking')

        rospy.loginfo('Start restaurant State')
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if self.state == 'init':
            if device == Devices.voice and 'follow me' in data:
                Publish.speak("I will follow you.")
                self.state = 'follow'
        elif self.state == 'follow':
            if device == Devices.follow:
                Publish.move_robot(data)
            elif device == Devices.voice and ('robot stop' in data or 'robot halt' in data):
                Publish.stop_robot()
                Publish.speak("What is this place?")
                self.state = 'waitForLocationName'
            elif device == Devices.voice and 'robot wait' in data:
                Publish.stop_robot()
                Publish.speak("Waiting for command.")
                self.state = 'waitForCommand'


if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        restaurant()
    except rospy.ROSInterruptException:
        pass
