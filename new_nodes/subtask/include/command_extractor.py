#!/usr/bin/env python
"""
Class for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""

import roslib
from location_information import *
from object_information import *
from people_information import *

roslib.load_manifest('main_state')

class Action:
    def __init__(self, action=None, object=None, data=None):
        self.action = action
        self.object = object
        self.data = data

    def __repr__(self):
        return "(%s, %s, %s)"%(self.action, self.data, self.object)

def readFileToList(filename):
    output = []
    file = open(filename)
    for line in file:
        if line.startswith('#'):
            continue
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
        if word in self.other_object:
            return True
        elif word in self.names:
            return True
        elif word in self.object_categories:
            return True
        elif word in self.location_categories:
            return True
        return False

    def isLocation(self, word):
        if word in self.rooms:
            return True
        elif word in self.places:
            return True
        return False

    def getObject(self, sentence):
        for obj in self.objects:
            if obj in sentence:
                return obj
        for obj in self.other_object:
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
        for location in self.rooms:
            if location in sentence:
                return location
        for location in self.places:
            if location in sentence:
                return location
        for category in self.location_categories:
            if category in sentence:
                return category
        return None

    def getName(self, sentence):
        for name in self.names:
            if name in sentence:
                return name
        return None

    def getPronoun(self, sentence):
        if sentence == None:
            return None
        for word in ['me', 'him', 'her', 'it', 'them']:
            words = sentence.split()
            if word in words: #and self.getObject(" ".join(words[words.index(word):])) == None:
                return  word
        return None

    def hasPronoun(self, sentence):
        if self.getPronoun(sentence) == None:
            return False
        return True

    def isPronoun(self, word):
        if self.getPronoun(word) == None:
            return False
        return True

    def isPreposition(self, word):
        if word in ['from', 'in', 'at', 'to']:
            return True
        return False

    def changeVerb(self, word):
        if word in ['approach', 'drive', 'enter', 'go', 'head', 'move', 'navigate', 'point']:
            return 'go'
        elif word in ['bring', 'carry', 'deliver', 'get', 'give', 'grab', 'grasp', 'hand', 'hold', 'pick', 'pick up', 'take', 'offer']:
            return 'grasp'
        elif word in ['announce', 'notify', 'remind', 'speak', 'tell']:
            return 'tell'
        elif word in ['ask']:
            return 'ask'
        elif word in ['answer']:
            return 'answer'
        elif word in ['follow']:
            return 'follow'
        elif word in ['detect', 'find', 'identify', 'look for']:
            return 'find'
        elif word in ['introduce']:
            return 'introduce';
        elif word in ['to']:
            return 'to'
        elif word in ['from', 'in', 'at']:
            return 'go'
        return None


    def __init__(self):
        # Read config file
        self.objects = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/objects.txt')

        self.other_objects = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/other_objects.txt')

        self.object_categories = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/object_categories.txt')

        self.rooms = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/rooms.txt')

        self.places = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/places.txt')

        self.location_categories = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/location_categories.txt')

        self.names = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/names.txt')

        self.verbs = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/verbs.txt')

        self.intransitive_verbs = readFileToList(
            roslib.packages.get_pkg_dir('main_state') + '/command_config/intransitive_verbs.txt')
    # Get actions from command
    def getActions(self, command):
        """
        >>> CommandExtractor().getActions("bring a coke from bathroom to the desk")
        [(go, bathroom, None), (grasp, desk, coke)]
        >>> CommandExtractor().getActions("go to the bedroom, find a person and tell the time")
        [(go, bedroom, None), (find, None, person), (tell, None, time)]
        >>> CommandExtractor().getActions("go to the dinner-table, grasp the crackers, and take them to the side-table")
        [(go, dinner-table, None), (grasp, side-table, crackers)]
        >>> CommandExtractor().getActions("bring a coke to the person in the living room and answer him a question")
        [(grasp, None, coke), (go, living room, None), (give, person, None), (answer, him, question)]
        >>> CommandExtractor().getActions("go to the door, ask the person there for her name and tell it to me")
        [(go, door, None), (ask, person, her name), (tell, me, it)]
        >>> CommandExtractor().getActions("go to the bedroom, find the waving person and tell the time")
        [(go, bedroom, None), (find, None, person), (tell, None, time)]
        >>> CommandExtractor().getActions("go to the kitchen, find a person and follow her")
        [(go, kitchen, None), (find, None, person), (follow, None, her)]
        >>> CommandExtractor().getActions("go to the side-table, grasp the coke, and take it to the dinner table")
        [(go, side-table, None), (grasp, dinner table, coke)]
        >>> CommandExtractor().getActions("go to the dinner-table, grasp the banana, and take it to the side-table")
        [(go, dinner-table, None), (grasp, side-table, banana)]
        >>> CommandExtractor().getActions("take the coke from the sink and carry it to me")
        [(go, sink, None), (grasp, me, coke)]
        >>> CommandExtractor().getActions("go to the kitchen, grasp the coke, and take it to the side-table")
        [(go, kitchen, None), (grasp, side-table, coke)]
        >>> CommandExtractor().getActions("go to the bathroom, grasp the soap, and take it to the side-table")
        [(go, bathroom, None), (grasp, side-table, soap)]
        >>> CommandExtractor().getActions("grasp the coke from the small table and carry it to me")
        [(go, small table, None), (grasp, me, coke)]
        >>> CommandExtractor().getActions("deliver a coke to frank in the kitchen")
        [(grasp, None, coke), (go, kitchen, None), (give, frank, None)]
        >>> CommandExtractor().getActions("offer a coke to frank in the kitchen")
        [(grasp, None, coke), (go, kitchen, None), (give, frank, None)]
        >>> CommandExtractor().getActions("offer a coke to the person at the door")
        [(grasp, None, coke), (go, door, None), (give, person, None)]
        """
        output = []
        for sentence in self.cut_sentence(command):
            self.extract_sentence(sentence,output)

        self.replace_unknown_noun(output)
        return output

    def cut_sentence(self, command):
        commands = []
        words = command.split()
        for i in xrange(0,len(words)):
            word = words[i].lower()
            if self.isVerb(word) or self.isPreposition(word):
                startSentence = command.find(words[i])
                endSentence = -1
                for j in xrange(i+1,len(words)):
                    if self.isVerb(words[j]) or self.isPreposition(words[j].lower()):
                        endSentence = command.find(words[j],startSentence + len(words[i]) - 1)
                        break
                if endSentence == -1:
                    endSentence = len(command)
                sentence = command[startSentence:endSentence]
                command = command[endSentence:]
                commands.append(sentence)
        return commands

    def extract_sentence(self, sentence ,output):
        words = sentence.split()
        word = words[0]
        object = self.getObject(sentence)
        data = self.getData(sentence)
        pronoun = None
        if object != None:
            pronoun = self.getPronoun(sentence.replace(object,''))
            object2 = self.getObject(sentence.replace(object,''))
            if object2!=None:
                pronoun = self.getPronoun(sentence.replace(object2,''))
                if sentence.index("%s"%object) > sentence.index("%s"%object2):
                    output.append(Action(self.changeVerb(word), object, object2))
                else:
                    output.append(Action(self.changeVerb(word), object2, object))
                return
        else:
            pronoun = self.getPronoun(sentence)


        if pronoun != None and object == None:
            object = pronoun
        elif pronoun != None and data == None:
            data = pronoun
        if word == 'from':
            output.insert(-1,Action(self.changeVerb(word), object, data))
        elif word == 'to':
            if data != None:
                output[-1].data = data
            elif object != None:
                output[-1].data = object
        elif word == 'in' or word == 'at':
            old_data = output[-1].data
            output[-1].data = None
            output.append(Action(self.changeVerb(word), object, data))
            output.append(Action('give', None, old_data))
        else:
            output.append(Action(self.changeVerb(word), object, data))

    def replace_unknown_noun(self, output):
        action_with_pronoun = None
        action_with_object = None
        for action in reversed(output):
            if self.isPronoun(action.object) and action.data != None:
                action_with_pronoun = action
            elif action_with_object != None:
                break
            elif self.isObject(action.object) and action.data == None:
                action_with_object = action
        if action_with_object != None and action_with_pronoun != None:
            action_with_pronoun.object = action_with_object.object
            output.remove(action_with_object)

    #Check whether command is valid or not
    def isValidCommand(self, command):
        """
        >>> CommandExtractor().isValidCommand('')
        False
        >>> CommandExtractor().isValidCommand('snack')
        False
        >>> CommandExtractor().isValidCommand('robot yes')
        False
        >>> CommandExtractor().isValidCommand('robot no')
        False
        >>> CommandExtractor().isValidCommand('move to bar go to kitchen table and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('go to fridge get soda and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('bring red chips go to bench and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('navigate to white shelf introduce yourself and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('bring me a cup')
        True
        >>> CommandExtractor().isValidCommand('bring a tool')
        True
        >>> CommandExtractor().isValidCommand('move to table')
        True
        >>> CommandExtractor().isValidCommand('bring toy to seat')
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
        for object in self.other_object:
            if object in command:
                isObjectFound = True
        for category in self.object_categories:
            if category in command:
                isObjectCategoryFound = True
        for location in self.rooms:
            if location in command:
                isLocationFound = True
        for location in self.places:
            if location in command:
                isLocationFound = True
        for category in self.location_categories:
            if category in command:
                isLocationCategoryFound = True
        return (isVerbFound and ((isObjectFound or isObjectCategoryFound) or (isLocationFound or isLocationCategoryFound))) or isIntransitiveVerbFound

if __name__ == '__main__':
    import doctest
    doctest.testmod()
