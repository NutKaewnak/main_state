__author__ = 'ms.antonio'

import roslib
from include.abstract_subtask import AbstractSubtask

def readFileToList(filename):
    output = []
    file = open(filename)
    for line in file:
        if line.startswith('#'):
            continue
        output.append(line.strip().lower())
    return output

class ExtractObjectLocation(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.object = 'None'
        self.location = 'None'
        self.verb = 'None'
        self.this_object_category = 'None'
        self.this_location_category = 'None'
        self.data = None
        self.object_category = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/object_category.txt')
        self.objects = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/objects.txt')
        self.location_category = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/location_category.txt')
        self.locations = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/GPSR/locations.txt')
        self.verbs = readFileToList(roslib.packages.get_pkg_dir('speech_processing')+'/command_config/GPSR/verbs.txt')
    def perform(self, perception_data):
        if self.state is 'init':
            self.object = 'None'
            self.location = 'None'
            self.verb = 'None'
            self.data = None
            self.this_object_category = 'None'
            self.this_location_category = 'None'
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('Good day sir, What would you want?')
            self.change_state('waitingForCommand')

        elif self.state is 'waitingForCommand':
            if perception_data.device == 'VOICE':
                self.data = perception_data.input
                for i in self.location_category:
                    if i in self.data:
                        self.this_location_category = i
                        break
                print  'loc_cat :' + self.this_location_category
                for i in self.object_category:
                    if i in self.data:
                        self.this_object_category = i
                        break
                print  'obj_cat :' + self.this_object_category
                for i in self.objects:
                    if i in self.data:
                        self.object = i
                        break
                print  'obj :' + self.object
                for i in self.locations:
                    if i in self.data:
                        self.location = i
                        break
                print  'loc :' + self.location
                for i in self.verbs:
                    if i in self.data:
                        self.verb = i
                        break
                print  'loc :' + self.location
                if self.this_location_category is not 'None' and self.this_object_category is not 'None':
                    self.skill.say('What'+self.this_object_category+'do you want')
                    self.change_state('AskForFindObject')
                elif self.this_location_category is not 'None' and self.this_object_category is 'None':
                    self.skill.say('What'+self.this_location_category+'do you want')
                    self.change_state('AskForFindLocation')
                elif self.this_location_category is 'None' and self.this_object_category is not 'None':
                    self.skill.say('What'+self.this_object_category+'do you want')
                    self.change_state('AskForFindObject')
                elif self.this_location_category is 'None' and self.this_object_category is 'None':
                    if self.object is not 'None' and self.location is 'None':
                        self.change_state('AskForFindLocation')
                    elif self.object is 'None' and self.location is not 'None':
                        self.change_state('finish')

        elif self.state is 'AskForFindObject':
            if perception_data.device == 'VOICE':
                self.data = perception_data.input
                for i in self.objects:
                    if i in self.data:
                        self.object = i
                        #self.skill.say('What'+i+' do you want')
                        #if self.type is '0':
                        #    self.change_state('FindLocation')
                        #elif self.type is '1':
                        self.skill.say('So where'+self.object+'it is')
                        self.change_state('AskForFindLocation')
                        break

        #elif self.state is 'FindLocation':
        #    self.location = FindLocation(self.object)
        #    self.skill.say('Wait a minute , I will bring' + self.object + 'from' + self.location +'to you' )
        #    self.change_state('finish')

        elif self.state is 'AskForFindLocation':
            if perception_data.device == 'VOICE':
                self.data = perception_data.input
                for i in self.locations:
                    if i in self.data:
                        self.location = i
                        if self.location is not 'None':
                             self.skill.say('Wait a minute , I will'+self.verb+'to'+self.location)
                        elif self.object is not 'None' and self.location is not 'None':
                            print  self.object
                            self.skill.say('Wait a minute , I will'+self.verb + self.object+'from'+self.location+'to you')
                        self.change_state('finish')
                        self.skill.say('object is'+self.object)
                        self.skill.say('location is'+self.location)
                        break

    def getObject(self):
        return self.object

    def getLocation(self):
        return self.location