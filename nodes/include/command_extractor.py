#!/usr/bin/env python
"""
Class for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""

import roslib

roslib.load_manifest('main_state')


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
        self.object_categories = readFileToList(
            roslib.packages.get_pkg_dir('main_state') + '/config/command_config/object_categories.txt')
        self.objects = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/objects.txt')
        self.locations = readFileToList(
            roslib.packages.get_pkg_dir('main_state') + '/config/command_config/locations.txt')
        self.names = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/names.txt')
        self.location_categories = readFileToList(
            roslib.packages.get_pkg_dir('main_state') + '/config/command_config/location_categories.txt')
        self.verbs = readFileToList(roslib.packages.get_pkg_dir('main_state') + '/config/command_config/verbs.txt')

    # Extract action from command and return as tuple(s) of (verb,object,data)
    def extractActionTuples(self, command):
        output = []
        commands = command.split()
        for i in xrange(0, len(commands)):
            # If commands[i] is verb, then looking for object and data
            if self.isVerb(commands[i].lower()):
                obj = None
                data = None
                for j in xrange(i + 1, len(commands)):
                    if self.isObject(commands[j].lower()):
                        if obj == None:  # If object is null assign it to obj
                            obj = commands[j].lower()
                        else:  # If object is not null, then assume it is a data
                            data = commands[j].lower()
                    if self.isVerb(commands[j].lower()):
                        break
                # Append an action to output list
                if obj != None and data != None:
                    output.append((commands[i], obj, data))
                elif obj != None:
                    output.append((commands[i], obj))
                else:
                    output.append((commands[i],))
        #rospy.loginfo(output)
        return output
