#!/usr/bin/env python
"""
Class for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""

import roslib

roslib.load_manifest('main_state')

class Action:
    def __init__(self):
        self.action = ''
        self.object = ''
        self.data = ''

def readFileToList(filename):
    output = []
    file = open(filename)
    for line in file:
        output.append(line.strip().lower())
    return output


class CommandExtractor(object):
    def isVerb(self, word):
        if word in self.verbs:
            return True
        else:
            return False

    def isObject(self, word):
        if word in self.objects:
            return True
        elif word in self.locations:
            return True
        elif word in self.names:
            return True
        elif word in self.object_categories:
            return True
        elif word in self.location_categories:
            return True
        return False

    def __init__(self):
        # Read config file
        self.object_categories = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/object_categories.txt')
        self.objects = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/objects.txt')
        self.locations = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/locations.txt')
        self.names = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/names.txt')
        self.location_categories = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/location_categories.txt')
        self.verbs = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/verbs.txt')
        self.intransitive_verbs = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/intransitive_verbs.txt')

    # Extract action from command and return as tuple(s) of (verb,object,data)
    def extractActions(self, command):
        output = []
        commands = command.split()
        for i in xrange(0, len(commands)):
            # If commands[i] is verb, then looking for object and data
            if self.isVerb(commands[i].lower()):
                action = Action()
                action.action = commands[i].lower()
                for j in xrange(i + 1, len(commands)):
                    if self.isObject(commands[j].lower()):
                        if action.object == '':  # If object is null assign it to obj
                            action.object = commands[j].lower()
                        else:  # If object is not null, then assume it is a data
                            action.data = commands[j].lower()
                    if self.isVerb(commands[j].lower()):
                        break
                # Append an action to output list
                output.append(action)
        #rospy.loginfo(output)
        return output

    #Check whether command is valid or not
    def isValidCommand(self, command):
        words = command.split()
        isVerbFound = False
        isObjectFound = isObjectCategoryFound = False
        isLocationFound = isLocationCategoryFound = False
        for word in words:
            if word in self.verbs or word in self.intransitive_verbs:
                isVerbFound = True
            elif word in self.objects:
                isObjectFound = True
            elif word in self.locations:
                isLocationFound = True
            elif word in self.object_categories:
                isObjectCategoryFound = True
            elif word in self.location_categories:
                isLocationCategoryFound = True
        return isVerbFound and ((isObjectFound or isObjectCategoryFound) or (isLocationFound or isLocationCategoryFound))
