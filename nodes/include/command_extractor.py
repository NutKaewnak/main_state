#!/usr/bin/env python
"""
Class for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""

import roslib

roslib.load_manifest('main_state')

class Action:
    def __init__(self, action, object, data):
        self.action = action
        self.object = object
        self.data = data

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

    def getObject(self, sentence):
        for obj in self.objects:
            if obj in sentence:
                return obj
        for category in self.object_categories:
            if category in sentence:
                return category
        for name in self.names:
            if name in sentence:
                return name
        return None

    def getData(self, sentence):
        for location in self.locations:
            if location in sentence:
                return location
        for category in self.location_categories:
            if category in sentence:
                return category
        return None

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

    # Get actions from command
    def getActions(selfs, command):
        """
        >>> CommandExtractor().getActions('')
        []
        >>> CommandExtractor().getActions('move to bar go to bed and leave apartment')
        [('move', None, 'bar'), ('go', None, 'bed'), ('leave', None, None)]
        >>> CommandExtractor().getActions('navigate to kitchen table bring coke and exit apartment')
        [('navigate', None, 'kitchen table'), ('bring', 'coke', None), ('exit', None, None)]
        >>> CommandExtractor().getActions('go to bar find milk and take it')
        [('go', None, 'bar'), ('find', 'milk', None), ('take', None, None)]
        >>> CommandExtractor().getActions('go to stove identify peanut butter and take it')
        [('go', None, 'stove'), ('identify', 'peanut butter', None), ('take', None, None)]
        >>> CommandExtractor().getActions('go to kitchen find amanda and exit')
        [('go', None, 'kitchen'), ('find', 'amanda', None), ('exit', None, None)]
        >>> CommandExtractor().getActions('bring me a drink')
        [('bring', 'drink', None)]
        >>> CommandExtractor().getActions('carry a drink to table')
        [('carry', 'drink', 'table')]
        >>> CommandExtractor().getActions('navigate to shelf')
        [('navigate', None, 'shelf')]
        >>> CommandExtractor().getActions('carry a cleaning stuff to table')
        [('carry', 'cleaning stuff', 'table')]
        >>> CommandExtractor().getActions('bring snacks to seat')
        [('bring', 'snacks', 'seat')]
        """
        output = []
        words = command.split()
        for i in xrange(0,len(words)):
            if selfs.isVerb(words[i].lower()):
                startSentence = command.find(words[i])
                endSentence = -1
                for j in xrange(i+1,len(words)):
                    if selfs.isVerb(words[j]):
                        endSentence = command.find(words[j],command.find(words[j]))
                        break
                if endSentence == -1:
                    endSentence = len(command)
                sentence = command[startSentence:endSentence]
                output.append((words[i],selfs.getObject(sentence),selfs.getData(sentence)))
        return output

    #Check whether command is valid or not
    def isValidCommand(self, command):
        """
        >>> CommandExtractor().isValidCommand('')
        False
        >>> CommandExtractor().isValidCommand('snacks')
        False
        >>> CommandExtractor().isValidCommand('bench')
        False
        >>> CommandExtractor().isValidCommand('cleaning stuff')
        False
        >>> CommandExtractor().isValidCommand('seat')
        False
        >>> CommandExtractor().isValidCommand('robot yes')
        False
        >>> CommandExtractor().isValidCommand('robot no')
        False
        >>> CommandExtractor().isValidCommand('move to bench go to kitchen table and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('go to sidetable get milk and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('bring peanut butter go to bench and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('navigate to bench introduce yourself and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('bring me a food')
        True
        >>> CommandExtractor().isValidCommand('bring a cleaning stuff')
        True
        >>> CommandExtractor().isValidCommand('move to table')
        True
        >>> CommandExtractor().isValidCommand('bring cleaning stuff to seat')
        True
        """
        isVerbFound = isIntransitiveVerbFound = False
        isObjectFound = isObjectCategoryFound = False
        isLocationFound = isLocationCategoryFound = False
        for verb in self.verbs:
            if verb in command:
                isVerbFound = True
        for verb in self.intransitive_verbs:
            if verb in command:
                isIntransitiveVerbFound = True
        for object in self.objects:
            if object in command:
                isObjectFound = True
        for category in self.object_categories:
            if category in command:
                isObjectCategoryFound = True
        for location in self.locations:
            if location in command:
                isLocationFound = True
        for category in self.location_categories:
            if category in command:
                isLocationCategoryFound = True
        return (isVerbFound and ((isObjectFound or isObjectCategoryFound) or (isLocationFound or isLocationCategoryFound))) or isIntransitiveVerbFound

if __name__ == '__main__':
    import doctest
    doctest.testmod()
