#!/usr/bin/env python
import rospy
import roslib
import xml.etree.ElementTree as ET


class People:
    def __init__(self, people_node):
        self.people = []
        for person in people_node:
            self.people.append(person.attrib['name'])

    def get_people_names(self):
        return self.people


def read_people_information():
    return read_people_information_file(roslib.packages.get_pkg_dir('main_state') + '/config/people_information.xml')


def read_people_information_file(filename):
    rospy.loginfo('people_information.py : Read People Information XML')
    people_information_file = ET.parse(filename)
    return People(people_information_file.getroot())