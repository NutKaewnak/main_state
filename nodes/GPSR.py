#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from include.command_extractor import *
from math import pi

roslib.load_manifest('main_state')

def readFileToDic(filename):
    file = open(filename)
    dic = {}
    key = None
    for line in file:
        if line.startswith('-'):
            dic[key].append(line.replace('-', '').strip())
        else:
            key = line.strip()
            dic[key] = []
    return dic

class GPSR(BaseState):

    def __init__(self):
        BaseState.__init__(self)
        rospy.loginfo('Start GPSR State')
        vc_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/verb_categories.txt'
        lc_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/location_categories.txt'
        oc_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/object_categories.txt'
        ol_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/object_locations.txt'
        self.command = ''
        self.current_action_index = 0
        self.current_action = None
        self.actions = None
        self.verb_categories = readFileToDic(vc_filename)
        self.location_categories = readFileToDic(lc_filename)
        self.object_categories = readFileToDic(oc_filename)
        self.object_locations = readFileToDic(ol_filename)
        self.ask_data = ''
        rospy.spin()

    def startAction(self, action):
        if action.action in self.verb_categories['go']:
            if action.object in self.location_categories.values():
                self.move_robot(action.object)
                self.state = 'move'
            elif action.object in self.location_categories.keys():
                Publish.speak("Please tell me what " + action.object + " to go.")
                self.state = 'ask_object'
        if action.action in self.verb_categories['bring']:
            location = ''
            if action.object in self.object_categories.values():
                object_category = [c for c in self.object_categories.keys() if action.object in self.object_categories[c]]
                location = self.object_locations[object_category]
                self.move_robot(location)
                self.state = 'move'
            elif action.object in self.object_categories.keys():
                Publish.speak("Please tell me what " + action.object + " to bring.")
                self.state = 'ask_object'

    def main(self, device, data):
        rospy.loginfo('state in:' + self.state + ' from:' + device + ' data:' + str(data))
        if self.state == 'init':
            if device == Devices.voice:
                self.command = data
                Publish.speak('Do you want me to ' + data)
                self.state = 'confirm'
        elif self.state == 'confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    command_extractor = CommandExtractor()
                    self.actions = command_extractor.extractActions(self.command)
                    rospy.loginfo(len(self.actions))
                    self.current_action = self.actions[self.current_action_index]
                    Publish.speak('I will ' + self.current_action.action + ' ' + self.current_action.object)
                    self.startAction(self.current_action)
                else:
                    Publish.speak('Please repeat your command.')
                    self.state = 'init'
        elif self.state == 'ask_object':
            if device == Devices.voice:
                if data in [a for key in self.location_categories.keys() for a in self.location_categories[key]]:
                    Publish.speak(self.current_action.object + ' is at ' + data + ' yes or no.')
                    self.ask_data = data
                    self.state = 'ask_object_confirm'
                elif data in [a for key in self.object_categories.keys() for a in self.object_categories[key]]:
                    Publish.speak(self.current_action.object + ' you want' + ' is ' + data + ' yes or no.')
                    self.ask_data = data
                    self.state = 'ask_object_confirm'
        elif self.state == 'ask_object_confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    self.current_action.object = self.ask_data
                    Publish.speak('I will '+ self.current_action.action + " " + self.current_action.object)
                    self.state = 'move'
                else:
                    self.state = 'ask_object'
                    self.current_action = self.actions[self.current_action_index]
                    self.startAction(self.current_action)
        elif self.state == 'move':
            rospy.loginfo('move')

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        GPSR()
    except Exception as error:
        rospy.loginfo(error)
