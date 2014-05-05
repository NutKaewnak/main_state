#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from include.object_information import *
from include.location_information import *
from include.command_extractor import *

roslib.load_manifest('main_state')

from include.function import *
from include.publish import *
from include.reconfig_kinect import *
from std_msgs.msg import String, Bool
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Pose2D, Vector3
from math import pi, sqrt, sin, cos


def main_state(device, data):
    global state, location_list, temp, command_list, location_count, current_command

    if (state == 'gotoObjectLocation'):
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


class restaurant(BaseState):
    def __init__(self):
        BaseState.__init__(self)

        Publish.set_height(0.85)
        self.reconfig.changeDepthResolution(8)
        Publish.set_manipulator_action('walking')

        self.direction = ['left', 'right', 'back']
        self.command_extractor = CommandExtractor()
        self.command_list = []

        read_location_information_file(self.location_list, roslib.packages.get_pkg_dir(
            'main_state') + '/config/restaurant_location_information.xml')

        self.object_info = read_object_info()
        self.not_found = False
        self.temp = []
        self.current_command = 0

        rospy.loginfo('Start restaurant State')
        rospy.spin()

    def remember_master(self, data):
        if self.robot_position == None:
            print "No robot_position"
            return
        theta = self.robot_position.theta + data.pose2d.theta
        dist = sqrt(data.pose2d.x ** 2 + data.pose2d.y ** 2)
        extend_x = dist * cos(theta)
        extend_y = dist * sin(theta)
        self.master_position = Pose2D(self.robot_position.x + extend_x, self.robot_position.y + extend_y, theta)
        #print self.master_position

    def get_object_location_from_current_command(self):
        return self.get_location_for_object(self.get_object_name_from_current_command())

    def get_object_name_from_current_command(self):
        return self.command_list[self.current_command][1]

    def get_location_for_object(self, object_name):
        return str(self.object_info.get_object(object_name).category) + ' shelf'

    def get_location_height(self, location):
        return self.location_list[location].height

    def get_serve_location_from_current_command(self):
        return self.command_list[self.current_command][2]

    def main(self, device, data):
        rospy.loginfo("state:" + self.state + " from:" + device + " data:" + str(data))
        if device == Devices.follow:
            self.remember_master(data)

        if self.state == 'init':
            if device == Devices.voice and 'follow me' in data:
                self.speak("I will follow you.")
                self.state = 'follow'
        elif self.state == 'follow':
            if device == Devices.follow:
                Publish.move_robot(data)
            elif device == Devices.voice and any(s in data for s in ['robot stop', 'robot halt', 'robot halting']):
                self.stop_robot()
                self.speak("What is this place?")
                self.state = 'waitForLocationName'
            elif device == Devices.voice and 'robot waiting' in data:
                self.stop_robot()
                self.speak("Waiting for command.")
                self.state = 'waitForCommand'
        elif self.state == 'waitForLocationName':
            self.stop_robot()
            if device == Devices.voice:
                if 'follow me' in data:
                    self.speak("I will follow you.")
                    self.state = 'follow'
                else:
                    for location in self.location_list.keys():
                        if location in data:
                            for orient in self.direction:
                                if orient in data:
                                    self.temp = (location, orient)
                                    self.speak(location + " on your " + orient + ",yes or no?")
                                    self.state = 'confirmLocationName'
                                    return None
        elif self.state == 'confirmLocationName':
            self.stop_robot()
            if device == Devices.voice and 'robot yes' in data:
                if self.temp[1] in 'left':
                    self.master_position.theta -= pi / 2.0
                elif self.temp[1] in 'right':
                    self.master_position.theta += pi / 2.0
                self.location_list[self.temp[0]] = LocationInfo(self.temp[0], self.master_position, 1.05)
                self.speak("I remember " + self.temp[0])
                self.state = 'waitForLocationName'
            elif device == Devices.voice and 'robot no' in data:
                self.speak("What is this place?")
                self.state = 'waitForLocationName'
        elif self.state == 'waitForCommand':
            self.stop_robot()
            if device == Devices.voice:
                actions = self.command_extractor.getActions(data)[0]
                self.speak("You want me to " + actions[0] + " " + actions[1] + " to " + actions[2] + ".")
                self.temp = actions
                self.state = "confirmOrder"
            if len(self.command_list) == 3:
                self.current_command = 0
                self.move_robot(self.get_object_location_from_current_command())
                self.wait(2)
                self.state = 'gotoObjectLocation'
        elif self.state == 'confirmOrder':
            self.stop_robot()
            if device == Devices.voice and 'robot yes' in data:
                self.command_list.append(self.temp)
                actions = self.temp
                print actions
                self.speak("I will " + actions[0] + " " + actions[1] + " to " + actions[2] + ".")
                self.state = 'waitForCommand'
            elif device == Devices.voice and 'robot no' in data:
                self.speak("Waiting for command.")
                self.state = 'waitForCommand'
        elif self.state == 'gotoObjectLocation':
            if device == Devices.base and 'SUCCEEDED' in data:
                self.speak('I am at ' + self.get_object_location_from_current_command() + '.')
                self.prepare_manipulate(self.get_location_height(self.get_object_location_from_current_command()))
                self.wait(1)
                self.state = 'searchObject'
        elif self.state == 'searchObject':
            if device == Devices.manipulator and data in 'finish':
                Publish.find_object(self.get_location_height(self.get_object_location_from_current_command()))
            elif device == Devices.recognition:
                found = False
                for object_instance in data.objects:
                    if object_instance.category in self.get_object_name_from_current_command():
                        found = True
                        if not object_instance.isManipulable:
                            # move
                            self.not_found = True
                            self.state = 'grasping'
                            self.wait(1)
                        else:
                            # grasp
                            self.not_found = False
                            Publish.set_manipulator_point(object_instance.point.x,
                                                          object_instance.point.y,
                                                          object_instance.point.z)
                            self.wait(1)
                            self.state = 'grasping'
                if not found:
                    self.not_found = True
                    self.state = 'grasping'
                    self.wait(1)
        elif self.state == 'grasping':
            if device == Devices.manipulator and data in 'finish':
                self.speak('I got ' + self.get_object_name_from_current_command() + '.')
                self.move_robot(self.get_serve_location_from_current_command())
                self.wait(1)
                self.state = 'gotoServeLocation'
            elif self.not_found:
                self.speak('I will go to ' + self.get_serve_location_from_current_command() + '.')
                self.move_robot(self.get_serve_location_from_current_command())
                self.wait(1)
                self.state = 'gotoServeLocation'
        elif self.state == 'gotoServeLocation':
            if device == Devices.base and 'SUCCEEDED' in data:
                if self.not_found:
                    self.speak('Sorry, I cannot get you ' + self.get_object_name_from_current_command() + '.')
                    self.current_command += 1
                    self.move_robot(self.get_object_location_from_current_command())
                    self.wait(2)
                    self.state = 'gotoObjectLocation'
                else:
                    self.speak('I am at ' + self.get_serve_location_from_current_command() + ' to serve you.')
                    Publish.set_manipulator_action('normal')
                    self.state = 'reachOut'
        elif self.state == 'reachOut':
            if device == Devices.manipulator and data in 'finish':
                Publish.set_manipulator_action('gripper_open')
                self.state = 'gripperOpen'
        elif self.state == 'gripperOpen':
            if device == Devices.manipulator and data in 'finish':
                self.current_command += 1
                self.move_robot(self.get_object_location_from_current_command())
                self.wait(2)
                self.state = 'gotoObjectLocation'

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        restaurant()
    except rospy.ROSInterruptException:
        pass
