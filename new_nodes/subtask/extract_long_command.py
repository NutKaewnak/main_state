__author__ = 'ms.antonio'

import roslib
from include.command_extractor import CommandExtractor
from include.abstract_subtask import AbstractSubtask


def read_file_to_list(filename):
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
        self.object = None
        self.location = None
        self.verb = None
        self.object_category = None
        self.location_category = None
        self.data = None
        self.object_category_array = read_file_to_list(roslib.packages.get_pkg_dir('main_state') +
                                                       '/config/object_category.txt')
        self.object_array = read_file_to_list(roslib.packages.get_pkg_dir('main_state') + '/config/objects.txt')
        self.location_category_array = read_file_to_list(roslib.packages.get_pkg_dir('main_state') +
                                                         '/config/location_categories.txt')
        self.location_array = read_file_to_list(roslib.packages.get_pkg_dir('main_state') + '/config/locations.txt')
        self.verb_array = read_file_to_list(roslib.packages.get_pkg_dir('main_state') + '/config/verbs.txt')
        self.command_extractor = CommandExtractor()

    def perform(self, perception_data):
        if self.state is 'init':
            self.object = None
            self.location = None
            self.verb = None
            self.object_category = None
            self.location_category = None
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('Please say command')
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            if perception_data.device is 'VOICE':
                self.data = perception_data.input
                if self.command_extractor.isValidCommand(self.data):
                    self.change_state('wait_for_confirm')

        elif self.state is 'wait_for_confirm':
            if perception_data.device is 'VOICE':
                if perception_data.input is 'robot yes':
                    self.extract_command(self.data)
                    if self.location_category is not None and self.object_category is not None:
                        self.skill.say('What' + self.object_category + 'do you want')
                        self.change_state('AskForFindObject')

                    elif self.location_category is not None and self.object_category is None:
                        self.skill.say('What' + self.location_category + 'do you want')
                        self.change_state('AskForFindLocation')

                    elif self.location_category is None and self.object_category is not None:
                        self.skill.say('What' + self.object_category + 'do you want')
                        self.change_state('AskForFindObject')

                    elif self.location_category is None and self.object_category is None:
                        if self.object is not None and self.location is None:
                            self.change_state('AskForFindLocation')

                        elif self.object is None and self.location is not None:
                            self.change_state('finish')

                elif perception_data.input is 'robot no':
                    self.skill.say('Canceled. Please say command again.')
                    self.change_state('wait_for_command')

        elif self.state is 'AskForFindObject':
            if perception_data.device == 'VOICE':
                self.data = perception_data.input
                for i in self.object_array:
                    if i in self.data:
                        self.object = i
                        self.skill.say('So where'+self.object+'it is')
                        self.change_state('AskForFindLocation')
                        break

        elif self.state is 'AskForFindLocation':
            if perception_data.device == 'VOICE':
                self.data = perception_data.input
                for i in self.location_array:
                    if i in self.data:
                        self.location = i
                        if self.location is not None:
                            self.skill.say('Wait a minute , I will' + self.verb + 'to' + self.location)
                        elif self.object is not None and self.location is not None:
                            print self.object
                            self.skill.say('I will' + self.verb + self.object + 'from' + self.location + 'to you')
                        self.change_state('finish')

                        self.skill.say('object is'+self.object)
                        self.skill.say('location is'+self.location)
                        break

    def extract_command(self, data):
        for i in self.location_category_array:
            if i in data:
                self.location_category = i
                break
        print 'loc_cat :' + self.location_category
        for i in self.object_category_array:
            if i in data:
                self.object_category = i
                break
        print 'obj_cat :' + self.object_category
        for i in self.object_array:
            if i in data:
                self.object = i
                break
        print 'obj :' + self.object
        for i in self.location_array:
            if i in data:
                self.location = i
                break
        print 'loc :' + self.location
        for i in self.verb_array:
            if i in data:
                self.verb = i
                break
        print 'loc :' + self.location

    def get_object(self):
        return self.object

    def get_location(self):
        return self.location