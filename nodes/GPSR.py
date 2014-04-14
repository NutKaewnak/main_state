#!/usr/bin/env python
import rospy
import roslib
from include.function import *
from include.publish import *
from include.base_state import *
from include.command_extractor import *
from geometry_msgs.msg import Vector3

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
        self.command_extractor = CommandExtractor()
        self.current_action_index = 0
        self.current_action = None
        self.actions = []
        self.verb_categories = readFileToDic(vc_filename)
        self.location_categories = readFileToDic(lc_filename)
        self.object_categories = readFileToDic(oc_filename)
        self.object_locations = readFileToDic(ol_filename)
        self.ask_data = ''
        rospy.spin()

    def findObjectCategory(self, object):
        for c in self.object_categories.keys():
            if object in self.object_categories[c]:
                return c

    def findObjectLocation(self, object):
        category = self.findObjectCategory(object)
        return self.object_locations[category][0]

    def startMoving(self, action):
        if action.data in self.verb_categories['go']:
            self.move_robot(action.data)
        elif action.action in self.verb_categories['bring']:
            self.move_robot(self.findObjectLocation(action.object))

    def startAction(self, action):
        if action.action in self.verb_categories['go']:
            if action.data in [loc for k in self.location_categories.keys() for loc in self.location_categories[k]]:
                self.move_robot(action.data)
                self.state = 'move'
                rospy.loginfo('%s,%s,%s'%(action.action,action.object if action.object else 'None',action.data if action.data else 'None'))
            elif action.data in self.location_categories.keys():
                Publish.speak("Please tell me where %s is." % action.data)
                self.state = 'ask_data'
        if action.action in self.verb_categories['bring']:
            if action.object in [obj for k in self.object_categories.keys() for obj in self.object_categories[k]]:
                self.move_robot(self.findObjectLocation(self.current_action.object))
                self.state = 'move'
                rospy.loginfo('%s,%s,%s'%(action.action,action.object if action.object else 'None',action.data if action.data else 'None'))
            elif action.object in self.object_categories.keys():
                Publish.speak("Please tell me what %s to bring." % action.object)
                self.state = 'ask_object'

    def main(self, device, data):
        rospy.loginfo('state in:' + self.state + ' from:' + device + ' data:' + str(data))
        if self.state == 'init':
            if device == Devices.voice and self.command_extractor.isValidCommand(data):
                self.command = data
                Publish.speak('Do you want me to %s' % data)
                self.state = 'confirm'
        elif self.state == 'confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    actions = self.command_extractor.getActions(self.command)
                    rospy.loginfo('Num action : ' + str(len(actions)))
                    for i in xrange(0,len(actions)):
                        action = Action(actions[i][0], actions[i][1], actions[i][2])
                        rospy.loginfo(' - %s,%s,%s'%(action.action,action.object if action.object else 'None',action.data if action.data else 'None'))
                        self.actions.append(action)
                    self.current_action = self.actions[self.current_action_index]
                    Publish.speak('I will %s.' % self.command)
                    self.startAction(self.current_action)
                elif 'no' in data:
                    Publish.speak('Please repeat your command.')
                    self.state = 'init'
        elif self.state == 'ask_object':
            if device == Devices.voice and data in self.object_categories[self.current_action.object]:
                Publish.speak('%s you want is %s yes or no.' % (self.current_action.object,data))
                self.ask_data = data
                self.state = 'ask_object_confirm'
        elif self.state == 'ask_object_confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    self.current_action.object = self.ask_data
                    if self.current_action.data in self.location_categories.keys():
                        Publish.speak('Please tell me where %s is.' % self.current_action.data)
                        self.state = 'ask_data'
                    else:
                        rospy.loginfo('I will %s %s' % (self.current_action.action,self.current_action.object))
                        Publish.speak('I will %s %s' % (self.current_action.action,self.current_action.object))
                        self.startMoving(self.current_action)
                        self.state = 'move'
                        rospy.loginfo('%s,%s,%s'%(self.current_action.action,self.current_action.object if self.current_action.object else 'None', self.current_action.data if self.current_action.data else 'None'))
                elif 'no' in data:
                    if self.current_action.object in self.object_categories.keys():
                        Publish.speak('Please tell me what %s to bring.' % self.current_action.object)
                    self.state = 'ask_object'
        elif self.state == 'ask_data':
            if device == Devices.voice and data in self.location_categories[self.current_action.data]:
                Publish.speak('%s is at %s yes or no.' % (self.current_action.data,data))
                self.ask_data = data
                self.state = 'ask_data_confirm'
        elif self.state == 'ask_data_confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    self.current_action.data = self.ask_data
                    rospy.loginfo('I will %s %s to %s' % (self.current_action.action,self.current_action.object if self.current_action.object else '',self.current_action.data if self.current_action.data else ''))
                    Publish.speak('I will %s %s to %s' % (self.current_action.action,self.current_action.object if self.current_action.object else '',self.current_action.data if self.current_action.data else ''))
                    self.startMoving(self.current_action)
                    self.state = 'move'
                    rospy.loginfo('%s,%s,%s'%(self.current_action.action,self.current_action.object if self.current_action.object else 'None', self.current_action.data if self.current_action.data else 'None'))
                elif 'no' in data:
                    Publish.speak('Please tell me where %s is' % self.current_action.data)
                    self.state = 'ask_data'
        elif self.state == 'move':
            if device == Devices.base and data == 'SUCCEEDED':
                rospy.loginfo('Arrive location.')
                Publish.object_search.publish(self.current_action.object) # Search object
                self.state = 'object_search'
        elif self.state == 'object_search':
            if device == 'object':
                if data == 'yes':
                    name, x, y, z = data.split(',')
                    Publish.manipulator_point(Vector3(float(x), float(y), float(z)))
                elif data == 'no':
                    Publish.speak(self.current_action.object + ' not found.')

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        GPSR()
    except Exception as error:
        rospy.loginfo(error)
