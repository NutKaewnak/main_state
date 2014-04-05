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
        rospy.spin()

    def startAction(self, action):
        if action[0] in self.verb_categories['go']:
            if action[1] in self.location_categories.values():
                self.move_robot(action[1])
                self.state = 'move'
            elif action[1] in self.location_categories.keys():
                Publish.speak("Please tell me where is the " + action[1])
                self.state = 'ask'
        if action[0] in self.verb_categories['bring']:
            location = ''
            if action[1] in self.object_categories.values():
                object_category = [c for c in self.object_categories.keys() if action[1] in self.object_categories[c]][0]
                location = self.object_locations[object_category]
                self.move_robot(location)
                self.state = 'move'

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
                    self.actions = command_extractor.extractActionTuples(self.command)
                    self.current_action = self.actions[self.current_action_index]
                    Publish.speak('I will ' + self.command)
                    self.startAction(self.current_action)
                else:
                    Publish.speak('Please repeat your command.')
                    self.state = 'init'
        elif self.state == 'ask':
            if device == Devices.voice:
                if data in self.location_categories.values():
                    Publish.speak(self.current_action[1] + ' is at ' + data)
                    self.state = 'ask_confirm'
                elif data in self.object_categories.values():
                    Publish.speak(self.current_action[1] + ' is ' + data)
                    self.state = 'ask_confirm'
        elif self.state == 'ask_confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    Publish.speak('I will ' + self.ac)
        rospy.loginfo('state out:' + self.state + ' from:' + device + ' data:' + str(data))

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        GPSR()
    except Exception as error:
        rospy.loginfo(error)
