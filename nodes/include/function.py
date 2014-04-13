#!/usr/bin/env python
import rospy
import roslib

roslib.load_manifest('main_state')

import tf
from lumyai_navigation_msgs.msg import NavGoalMsg
from geometry_msgs.msg import Quaternion

class a_object:
    def __init__(self, name, category, place):
        self.name = name
        self.category = category
        self.place = place

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'name: ' + self.name + "\ncategory: " + self.catagory + "\nplace: " + self.place

def get_quaternion(roll, pitch, yaw):
    temp = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
    return Quaternion(temp[0], temp[1], temp[2], temp[3])


def read_object(object_list):
    rospy.loginfo('Main : Read Object')
    temp = open(roslib.packages.get_pkg_dir('main_state') + '/config/object_catagory.txt')
    catagory, place = '', ''
    for line in temp:
        line = line.strip().split('-')
        if (len(line) == 1):
            line = line[0].split(',')
            catagory, place = line[0], line[1]
        else:
            object_list[line[1]] = a_object(line[1], catagory, place)


def readLocationSequenceEmer(location_list):
    rospy.loginfo('Main : Read Location Sequence')
    temp = open(roslib.packages.get_pkg_dir('main_state') + '/config/search_sequence_emer.txt')
    for line in temp:
        if (line.strip() == ''): continue
        location_list.append(line.strip())


def readLocationSequence(location_list):
    rospy.loginfo('Main : Read Location Sequence')
    temp = open(roslib.packages.get_pkg_dir('main_state') + '/config/search_sequence.txt')
    for line in temp:
        if (line.strip() == ''): continue
        location_list.append(line.strip())


if __name__ == "__main__":
    object_list = {}
    read_object(object_list)
    print object_list
	
