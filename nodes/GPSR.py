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
from geometry_msgs.msg import Vector3, Pose2D
from lumyai_navigation_msgs.msg import NavGoalMsg

roslib.load_manifest('main_state')

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

class GPSR(BaseState):

    def __init__(self):
        BaseState.__init__(self)
        rospy.loginfo('Start GPSR State')
        vc_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/verb_categories.txt'
        lc_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/location_categories.txt'
        oc_filename = roslib.packages.get_pkg_dir('main_state') + '/config/command_config/object_categories.txt'
        self.location_info = read_location_category()
        self.object_info = read_object_info()
        self.state = 'wait'
        self.command = ''
        self.command_extractor = CommandExtractor()
        self.current_action_index = 0
        self.current_action = None
        self.actions = []
        self.verb_categories = readFileToDic(vc_filename)
        self.location_categories = self.location_info.location_categories
        self.object_categories = self.object_info.get_category_map()
        self.ask_data = None
        self.object_location = None
        self.starting_point = 'start1'
        self.exit_point = 'exit'
        self.current_angle = -60 * math.pi / 180
        self.max_pan_angle = 60 * math.pi / 180
        self.angle_step = 0.42
        self.neck_counter = 0
        self.height_offset = 0.3
        self.num_command = 0
        self.timer = Delay()
        self.LIMIT_MANIPULATED_DISTANCE = 0.78
        self.COOK_TABLE_HEIGTH          = 0.68
        self.ROBOT_HEIGHT               = 1.10
        self.desiredObject              = "kokokrunch"
        self.desiredObject_2            = "dutchmilk"
        Publish.set_height(1.0)
        Publish.set_neck(0.0, 0.0, 0.0)
        rospy.spin()

    def isCategoryOne(self, command):
        for object in self.object_info.get_all_object_names():
            if object in command:
                return True

        for location in self.location_info.get_all_location_names():
            if location in command:
                return True

        intransitive_verb = ['exit','leave','tell','introduce']
        for verb in intransitive_verb:
            if verb in command:
                return True

        return False

    def isCategoryTwo(self, command):
        if not self.isCategoryOne(command):
            for object_category in self.object_info.get_all_category_names():
                if object_category in command:
                    return True

            for location_category in self.location_info.get_all_category_names():
                if location_category in command:
                    return True
        return False

    def startMoving(self, action):
        if action.action in self.verb_categories['exit']:
            self.move_robot(self.exit_point)
        if action.action in self.verb_categories['go']:
            if action.data:
                self.move_robot(action.data)
            else:
                self.move_robot(self.exit_point)
        elif action.action in self.verb_categories['bring']:
            self.move_robot(self.current_action.data)
        self.wait(2)
        self.state = 'move'

    def prepareManipulate(self, height):
        Publish.set_height(height)
        Publish.set_manipulator_action('prepare')
        Publish.set_neck(0.0, -0.7, 0.0)

    def startAction(self, action): #category-one
        rospy.loginfo('%s %s %s'%(action.action, action.object, action.data))
        if action.action in self.verb_categories['go']:
            if action.data in [loc for k in self.location_categories.keys() for loc in self.location_categories[k]] or action.data is None:
                self.startMoving(action)
                #rospy.loginfo('%s,%s,%s'%(action.action,action.object if action.object else 'None',action.data if action.data else 'None'))
            elif action.data in self.location_categories.keys():
                self.speak("Please tell me where %s is." % action.data)
                self.state = 'ask_data'
        elif action.action in self.verb_categories['bring']:
            if action.object in [obj for k in self.object_categories.keys() for obj in self.object_categories[k]]:
                self.startMoving(action)
                #rospy.loginfo('%s,%s,%s'%(action.action,action.object if action.object else 'None',action.data if action.data else 'None'))
            elif action.object in self.object_categories.keys():
                self.speak("Please tell me what %s to %s." % (action.object,action.action))
                self.state = 'ask_object'
        elif action.action in self.verb_categories['exit']:
            self.startMoving(action)
        elif action.action in self.verb_categories['follow']:
            self.speak('I will follow you.')
            self.state = 'follow'
        elif action.action in self.verb_categories['introduce']:
            self.speak('Hello my name is lumyai. I am robot from Kasetsart University Thailand. Nice to meet you.')
            self.finishAction()
        elif action.action in self.verb_categories['make']:
            self.state = 'PREPARE_FOR_ACTION'
        elif action.action in self.verb_categories['notify']:
            self.move_robot(action.data)
            self.state = 'move'

    def finishAction(self):
        if self.current_action_index + 1 < len(self.actions):
            self.current_action_index += 1
            self.current_action = self.actions[self.current_action_index]
            #rospy.loginfo('Current action : %s,%s,%s'%(self.current_action.action,self.current_action if self.current_action.object else 'None',self.current_action.data if self.current_action.data else 'None'))
            self.startAction(self.current_action)
        else:
            self.move_robot(self.starting_point)
            self.wait(2)
            self.state = 'return'

    def main(self, device, data):
        rospy.loginfo('state in:' + self.state + ' from:' + device + ' data:' + str(data))
        if self.state == 'init':
            if device == Devices.door and data == 'open':
                Publish.move_relative(1.5,0)
                self.state = 'pass_door'
        elif self.state == 'pass_door':
            if device == Devices.base and data == 'SUCCEEDED':
                self.move_robot(self.starting_point)
                self.state = 'go_to_start'
        elif self.state == 'go_to_start':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak('hello, my name is lumyai please tell me what you want.')
                self.state = 'wait'
        elif self.state == 'wait':
            if device == Devices.voice and self.command_extractor.isValidCommand(data):
                self.state = 'confirm'
                self.command = data
                self.speak('did you say %s'%self.command)
            #    self.timer.wait(3)
            #    self.command = self.command + data
            #    action = self.command_extractor.getActions(data)
            #    print(action)
            #    new_action = Action(action[0][0], action[0][1], action[0][2])
            #    self.actions.append(new_action)
            #if not self.timer.is_waiting():
                #self.state = 'confirm'
                #self.speak('Did you say ' + self.command)
                #if self.isCategoryOne(data):
                #    self.state = 'wait_more_command'
                #    self.num_command += 1
                #elif self.isCategoryTwo(data):
                #    self.command = data
                #    self.speak('did you say %s.' % data)
                #    self.state = 'confirm'
                #self.command = data



        elif self.state == 'wait_more_command':
            if device == Devices.voice and self.command_extractor.isValidCommand(data):
                rospy.loginfo(self.command)
                if self.isCategoryOne(data):
                    self.num_command += 1
                    self.command += ' ' + data
                    if self.num_command == 3:
                        self.state = 'confirm'
                        self.speak('Did you say %s.'%self.command)
        elif self.state == 'confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    actions = self.command_extractor.getActions(self.command)
                    print(actions)
                    rospy.loginfo('Num action : ' + str(len(actions)))
                    for i in xrange(0,len(actions)):
                        action = Action(actions[i][0], actions[i][1], actions[i][2])
                        rospy.loginfo(' - %s,%s,%s'%(action.action,action.object if action.object else 'None',action.data if action.data else 'None'))
                        self.actions.append(action)
                    self.current_action = self.actions[self.current_action_index]
                    self.speak('I will %s.' % self.command)
                    self.startAction(self.current_action)
                    Publish.set_neck(0.0, -0.7, 0.0)
                    Publish.set_height(1.0)
                elif 'no' in data:
                    self.speak('Please repeat your command.')
                    self.state = 'wait'
        elif self.state == 'ask_object':
            if device == Devices.voice and data in self.object_categories[self.current_action.object]:
                self.speak('%s you want is %s yes or no.' % (self.current_action.object,data))
                self.ask_data = data
                self.state = 'ask_object_confirm'
        elif self.state == 'ask_object_confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    self.current_action.object = self.ask_data
                    self.speak('Please tell me where %s is.'%self.current_action.object)
                    self.state = 'ask_data'
                    #self.state = 'ask_object_location'
                elif 'no' in data:
                    self.speak('Please tell me what %s to bring.' % self.current_action.object)
                    self.state = 'ask_object'
        elif self.state == 'ask_object_location':
            if device == Devices.voice and data in [obj for key in self.location_categories.keys() for obj in self.location_categories[key]]:
                self.speak('%s is at %s yes or no.'%(self.current_action.object,data))
                self.ask_data = data
                self.state = 'ask_object_location_confirm'
        elif self.state == 'ask_object_location_confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    self.object_location = self.ask_data
                    if self.current_action.data:
                        self.speak('Please tell me where %s is.'%self.current_action.data)
                        self.state = 'ask_data'
                    else:
                        self.speak('I will %s %s'%(self.current_action.action,self.current_action.object))
                        rospy.loginfo('%s is at %s'%(self.current_action.object,self.object_location))
                        self.move_robot(self.object_location)
                        self.wait(2)
                        self.state = 'move'
                elif 'no' in data:
                    self.speak('Please tell me where %s is.'%self.current_action.object)
                    self.state = 'ask_object_location'
        elif self.state == 'ask_data':
            if device == Devices.voice and data in self.location_categories[self.current_action.data]:
                self.speak('%s is at %s yes or no.' % (self.current_action.data,data))
                self.ask_data = data
                self.state = 'ask_data_confirm'
        elif self.state == 'ask_data_confirm':
            if device == Devices.voice:
                if 'yes' in data:
                    self.current_action.data = self.ask_data
                    self.speak('I will %s %s from %s' % (self.current_action.action,self.current_action.object if self.current_action.object else '',self.current_action.data if self.current_action.data else ''))
                    rospy.loginfo('%s'%(self.current_action.data))
                    if self.current_action.action in self.verb_categories['go']:
                        self.move_robot(self.current_action.data)
                    elif self.current_action.action in self.verb_categories['bring']:
                        self.move_robot(self.current_action.data)
                    self.wait(2)
                    self.state = 'move'
                elif 'no' in data:
                    self.speak('Please tell me where %s is' % self.current_action.data)
                    self.state = 'ask_data'
        elif self.state == 'move':
            if device == Devices.base and data == 'SUCCEEDED':
                if self.current_action.action in self.verb_categories['bring']:
                    self.speak('I reach the %s'%self.current_action.data)
                    self.speak('I will get %s'%self.current_action.object)
                    rospy.loginfo(self.location_list[self.object_location].height + self.height_offset)
                    self.prepareManipulate(self.location_list[self.object_location].height + self.height_offset)
                    self.state = 'prepare'
                elif self.current_action.action in self.verb_categories['go']:
                    self.speak('I reach the %s'%self.current_action.data)
                    self.finishAction()
                elif self.current_action.action in self.verb_categories['exit']:
                    self.move_robot(self.exit_point)
                    self.state = 'return'
                elif self.current_action.action in self.verb_categories['notify']:
                    self.speak('your command is complete')
        elif self.state == 'prepare':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'object_search'
                rospy.loginfo(self.location_list[self.object_location].height)
                Publish.find_object(self.location_list[self.object_location].height)
        elif self.state == 'object_search':
            if device == Devices.recognition:
                found = False
                for object in data.objects:
                    if object.category == self.current_action.object:
                        found = True
                        if not object.isManipulable:
                            self.speak('Object not reachable')
                            self.move_robot(self.starting_point)
                            self.state = 'deliver'
                        else:
                            objCentroid = Vector3()
                            objCentroid.x = object.point.x
                            objCentroid.y = object.point.y
                            objCentroid.z = object.point.z
                            Publish.set_manipulator_point(objCentroid.x, objCentroid.y, objCentroid.z)
                            #rospy.loginfo('%s is at x:%f y:%f z:%f'%(self.current_action.object,objCentroid.x,objCentroid.y,objCentroid.z))
                            self.state = 'get_object'
                            self.speak('I found %s.'%self.current_action.object)
                if not found:
                    if self.current_angle >= self.max_pan_angle:
                        self.speak('%s not found'%self.current_action.object)
                        self.move_robot(self.starting_point)
                        self.wait(2)
                        self.state = 'deliver'
                        Publish.set_neck(0, -0.7, 0.0)
                    else:
                        self.current_angle += self.angle_step
                        Publish.set_neck(0, -0.7, self.current_angle)
                        Publish.find_object(self.location_list[self.object_location].height)
        elif self.state == 'get_object':
            if device == Devices.manipulator and data == 'finish':
                #if self.current_action.data:
                #    self.move_robot(self.current_action.data)
                #    self.wait(2)
                #else:
                self.move_robot(self.starting_point)
                self.wait(2)
                self.state = 'deliver'
                Publish.set_neck(0.0, 0.0, 0.0)
        elif self.state == 'deliver':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak('This is %s. Please take it.'%self.current_action.object)
                Publish.set_manipulator_action('normal_pullback')
                self.state = 'give'
        elif self.state == 'give':
            if device == Devices.manipulator and data == 'finish':
                Publish.set_manipulator_action('grip_open')
                self.state = 'grip_open'
        elif self.state == 'grip_open':
            if device == Devices.manipulator and data == 'finish':
                self.finishAction()
        elif self.state == 'introduce':
            self.finishAction()
        elif self.state == 'follow':
            if device == Devices.follow:
                if data.text_msg == 'lost':
                    data.text_msg = 'stop'
                Publish.move_robot(data)
            elif device == Devices.voice:
                self.stop_robot()
                self.finishAction()
        elif self.state == 'PREPARE_FOR_ACTION':
            Publish.set_manipulator_action('prepare')
            Publish.set_height(self.ROBOT_HEIGHT)
            Publish.set_neck(0,-0.7,0)
            Publish.move_relative(0,0,-0.5)
            self.state = 'READY_FOR_ACTION'
        elif self.state == 'READY_FOR_ACTION':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak("Searching breakfast ingredients.")
                Publish.find_object(self.COOK_TABLE_HEIGTH)
                self.state = 'SEARCHING_CORNFLAKE'
        elif(self.state == 'SEARCHING_CORNFLAKE'):
            if(device == Devices.recognition):
                objects = []
                print '--------len(data.objects) : ' +str(len(data.objects)) +  '-------'
                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    if  obj.category == "milo":#obj.category == self.desiredObject:
                        self.speak(obj.category)
                        centroidVector = Vector3()
                        centroidVector.x = obj.point.x
                        centroidVector.y = obj.point.y
                        centroidVector.z = obj.point.z
                        Publish.set_manipulator_action_grasp(centroidVector)
                        self.state = 'GRASPING_CORNFLAKE'
                        return None

        elif self.state == 'GRASPING_CORNFLAKE':
            if device == Devices.manipulator and data == 'finish':
                self.speak("I got it.")
                Publish.set_manipulator_action("prepare_pullback")
                self.state = 'SET_PREPARE'

        elif self.state == 'SET_PREPARE':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'SEARCHING_BOWL'
                #self.state = 'TURN_TO_CENTER_FROM_CORNFLAKE'
                #Publish.move_relative(0,0,0.5)

        elif self.state == 'TURN_TO_CENTER_FROM_CORNFLAKE':
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 'SEARCHING_BOWL'
                self.wait(2)
                #Publish.move_relative(0,0,0.5)

        elif self.state == 'SEARCHING_BOWL':
                if device == Devices.color_detector:
                    Publish.speak("searching a bowl.")
                    data.x -= 0.12
                    data.y -= 0.09
                    data.z += 0.30
                    Publish.set_manipulator_action_pour(data)
                    Publish.speak("pouring.")
                    self.state = 'DISCARD_CORNFLAKE'

        elif self.state == 'DISCARD_CORNFLAKE':
            if device == Devices.manipulator and data == 'finish':
                Publish.speak("discard cornflake.")
                self.wait(3)
                Publish.set_manipulator_action('cornflake_pullback')
                self.state = 'DISCARDING'

        elif self.state == 'DISCARDING':
            if device == Devices.manipulator and data == 'finish':
                #Publish.move_relative(0,0,0.5)
                Publish.find_object(self.COOK_TABLE_HEIGTH)
                self.state = 'SEARCHING_MILK'
                #self.state = 'TURN_TO_MILK'

        elif self.state == 'TURN_TO_MILK':
            if device == Devices.base and data == 'SUCCEEDED':
                Publish.find_object(self.COOK_TABLE_HEIGTH)
                self.state = 'SEARCHING_MILK'
                #self.state = 'TURN_TO_MILK'

        elif self.state == 'SEARCHING_MILK':
            if device == Devices.recognition:
                objects = []
                print '--------len(data.objects) : ' +str(len(data.objects)) + '-------'
                objects = data.objects
                for obj in objects:
                    print 'category : ' + obj.category + ' centroid : (' + str(obj.point.x) + "," + str(obj.point.y) + "," + str(obj.point.z) + ")"
                for obj in objects:
                    if obj.category == self.desiredObject_2:
                        self.speak(obj.category)
                        centroidVector = Vector3()
                        centroidVector.x = obj.point.x
                        centroidVector.y = obj.point.y
                        centroidVector.z = obj.point.z
                        Publish.set_manipulator_action_grasp(centroidVector)
                        self.state = 'GRASPING_MILK'
                        return None

        elif self.state == 'GRASPING_MILK':
            if device == Devices.manipulator and data == 'finish':
                self.speak("I got it.")
                Publish.set_manipulator_action("prepare_pullback")
                self.state = 'SET_PREPARE_MILK'

        elif self.state == 'SET_PREPARE_MILK':
            if device == Devices.manipulator and data == 'finish':
                self.state = 'SEARCHING_BOWL_2'
                #Publish.move_relative(0,0,-0.5)

        elif self.state == 'TURN_TO_CENTER_FROM_MILK':
            if device == Devices.base and data == 'SUCCEEDED':
                self.state = 'SEARCHING_BOWL_2'
                self.wait(2)
                #Publish.move_relative(0,0,0.5)

        elif self.state == 'SEARCHING_BOWL_2':
            if device == Devices.color_detector:
                Publish.speak("searching a bowl.")
                data.x -= 0.12
                data.y -= 0.09
                data.z += 0.30
                Publish.set_manipulator_action_pour(data)
                Publish.speak("pouring.")
                self.state = 'DISCARD_MILK'

        elif self.state == 'DISCARD_MILK':
            if device == Devices.manipulator and data == 'finish':
                self.wait(3)
                Publish.set_manipulator_action('cornflake_pullback')
                self.finishAction()
        elif self.state == 'return':
            if device == Devices.base and data == 'SUCCEEDED':
                self.speak('Return to starting point')
                self.actions = []
                self.current_action_index = 0
                self.current_action = None
                self.object_location = None
                self.state = 'wait'
                self.num_command = 0

if __name__ == '__main__':
    try:
        rospy.init_node('main_state')
        GPSR()
    except Exception as error:
        rospy.loginfo(error)