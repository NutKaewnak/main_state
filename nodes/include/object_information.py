#!/usr/bin/env python
import rospy
import roslib
import xml.etree.ElementTree as ET

roslib.load_manifest('main_state')

class Object:
    def __init__(self, object_node, category):
        self.name = object_node.attrib['name']
        self.category = category.name
        self.location = category.location
        self.action_place = category.action_place
        if 'isManipulate' in object_node.attrib:
            self.isManipulate = bool(object_node.attrib['isManipulate'])
        else:
            self.isManipulate = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n(Object name: ' + self.name + \
               ', category: ' + self.category + \
               ', location: ' + self.location + \
               ', action_place: ' + self.action_place + \
               ', isManipulate: ' + str(self.isManipulate) + ')'

class Category:
    def __init__(self, category_node):
        self.name = category_node.attrib['name']
        self.location = category_node.attrib['location']
        if 'action_place' in category_node.attrib:
            self.action_place = category_node.attrib['action_place']
        else:
            self.action_place = 'place_object'
        self.objects = []
        for object_node in category_node:
            object_instance = Object(object_node, self)
            self.objects.append(object_instance)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '\n(Category name: ' + self.name + \
               ', location: ' + self.location + \
               ', action_place:' + self.action_place + \
               ', objects: [' + str(self.objects) + '])'

class ObjectInfo:
    def __init__(self, object_info_node):
        self.category_data = {}
        self.object_data = {}
        for category in object_info_node:
            category_instance = Category(category)
            self.category_data[category_instance.name] = category_instance
            for object_instance in category_instance.objects:
                self.object_data[object_instance.name] = object_instance
        object_name = [(len(key),key) for key in self.object_data]
        object_name = sorted(object_name, reverse=True)
        self.object_list = [key for tmp,key in object_name]

    def get_category(self, category_name):
        return self.category_data[category_name]

    def get_object(self, object_name):
        return self.object_data[object_name]

    def get_object_from_str(self, sentence):
        result = []
        for object_name in self.object_list:
            if object_name in sentence:
                result.append(object_name)
                sentence = sentence.replace(object_name, "")
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'ObjectInfo : [' + str(self.category_data) + "]\n"

def read_object_info():
    return read_object_info_file(roslib.packages.get_pkg_dir('main_state') + '/config/object_information.xml')

def read_object_info_file(filename):
    rospy.loginfo('object_information.py : Read Object Information XML')
    object_info_file = ET.parse(filename)
    return ObjectInfo(object_info_file.getroot())

if __name__ == "__main__":
    object_info = read_object_info()
    print object_info

    print object_info.get_object_from_str("i want chocolate milk, tooth paste")
    print object_info.get_object_from_str("i want milk")
    print object_info.get_object_from_str("i want milk, chocolate milk")
