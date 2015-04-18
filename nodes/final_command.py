#!/usr/bin/env python
import rospy
import roslib
import math
from include.function import *
from include.publish import *
from include.base_state import *
from include.command_extractor import *
from include.location_information import *
from include.object_information import *
from include.people_information import *
from geometry_msgs.msg import Vector3, Pose2D
from lumyai_navigation_msgs.msg import NavGoalMsg

def readFileToDic(filename):
    file = open(filename)
    dic = {}
    key = None
    for line in file:
        if line.startswith('#'):
            continue
        if line.startswith('-'):
            dic[key].append(line.replace('-', '').strip())
        else:
            key = line.strip()
            dic[key] = []
    return dic

class Final(BaseState):

    def __init__(self):
        BaseState.__init__(self)
        rospy.loginfo('Start Final State')
        self.command = ''
        self.command_extractor = CommandExtractor()
        self.actions = []
        self.current_action = None
        self.action_index = 0
        self.timer = Delay()
        vc_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/verb_categories.txt'
        location_info = read_location_category()
        object_info = read_object_info()
        self.verb_categories = readFileToDic(vc_filename)
        self.location_categories = location_info.get_location_category_map()
        self.object_categories = object_info.get_object_category_map()
        rospy.spin()

    def main(self, device, data):
        rospy.loginfo('state in:' + self.state + ' from:' + device + ' data:' + str(data))
        if self.state == 'init':
            if device == Devices.voice:
                if self.command_extractor.isValidCommand(data):
                    self.timer.wait(3)
                    self.command = self.command + data
                    action = self.command_extractor.getActions(data)
                    new_action = Action(action[0], action[1], action[2])
                    self.actions.append(action)
            if not self.timer.is_waiting():
                self.state = 'confirm'
                text = ''
                for action in self.actions:
                    text = text + '%s %s %s' % (action.action, action.object, action.data)
                self.speak(text)

        elif self.state == 'confirm':
            if device == Devices.voice and 'yes' in data:
                self.speak('I will dy your command')
                self.current_action = self.actions[self.action_index]

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        Final()
    except Exception as error:
        rospy.loginfo(error)