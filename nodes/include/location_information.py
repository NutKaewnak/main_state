#!/usr/bin/env python
import rospy
import roslib
import xml.etree.ElementTree as ET

roslib.load_manifest('main_state')

from geometry_msgs.msg import Pose2D


class LocationInfo:
    def __init__(self, name=None, position=None, height=0.0):
        self.name = name
        self.position = position
        self.height = float(height)

    def init_from_node(self, location_node):
        self.name = location_node.attrib['name']
        location_pos = map(float, location_node.attrib['position'].split(','))
        self.position = Pose2D(location_pos[0], location_pos[1], float(location_node.attrib['rotation']))
        self.height = float(location_node.attrib['height'])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(name: ' + self.name + \
               ', Pose: [' + str(self.position) + \
               '], Height: ' + str(self.height) + ')'


class RoomInfo(LocationInfo):
    def __init__(self, name=None, position=None, height=0.0):
        LocationInfo.__init__(self, name, position, height)
        self.locations = []

    def init_from_node(self, room_node):
        LocationInfo.init_from_node(self, room_node)
        for location in room_node:
            self.locations.append(location.attrib['name'])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(name: ' + self.name + \
               ', Pose: [' + str(self.position) + \
               '], Height: ' + str(self.height) + \
               ', locations: [' + str(self.locations) + '])'

class LocationCategory():
    def __init__(self,location_info_node):
        self.location_categories = {}
        for category in location_info_node:
            self.location_categories[category.attrib['name']] = []
            for location in category:
                self.location_categories[category.attrib['name']].append(location.attrib['name'])

    def get_all_category_names(self):
        return self.location_categories.keys()

    def get_all_location_names(self):
        return [location for c in self.get_all_category_names() for location in self.location_categories[c]]

    def get_location_in_category(self, category_name):
        return self.location_categories[category_name]

def read_location_information(location_list):
    read_location_information_file(location_list, roslib.packages.get_pkg_dir('main_state') + '/config/location_information.xml')

def read_location_category():
    return read_location_category_file(roslib.packages.get_pkg_dir('main_state') + '/config/location_category.xml')

def read_location_category_file(filename):
    rospy.loginfo('location_information.py : Read Location Category XML')
    location_category_file = ET.parse(filename)
    return LocationCategory(location_category_file.getroot())

def read_location_information_file(location_list, filename):
    rospy.loginfo('location_information.py : Read Location Information XML')
    location_information_file = ET.parse(filename)
    for location in location_information_file.getroot():
        if location.tag == 'room':
            room_info = RoomInfo()
            room_info.init_from_node(location)
            location_list[location.attrib['name']] = room_info
            for sub_location in location:
                location_info = LocationInfo()
                location_info.init_from_node(sub_location)
                location_list[sub_location.attrib['name']] = location_info
        elif location.tag == 'location':
            location_info = LocationInfo()
            location_info.init_from_node(location)
            location_list[location.attrib['name']] = location_info

if __name__ == "__main__":
    location_list = {}
    read_location_information(location_list)
    #print location_list
