#!/usr/bin/env python
"""
Class for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""

import roslib

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
        if word in self.other_objects:
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

    def getVerb(self, sentence):
        if sentence == None:
            return None
        sentence = sentence.strip()
        sentence = " %s "%sentence
        for verb in self.verbs:
            verb = " %s "%verb
            if verb in sentence:
                return verb.strip()
        return None

    def has_verb(self, sentence):
        if self.getVerb(sentence) != None:
            return True
        return False

    def getObject(self, sentence):
        sentence = sentence.strip()
        sentence = " %s "%sentence
        for obj in self.objects:
            obj = " %s "%obj
            if obj in sentence:
                return obj.strip()
        for obj in self.other_objects:
            obj = " %s "%obj
            if obj in sentence:
                return obj.strip()
        for category in self.object_categories:
            category = " %s "%category
            if category in sentence:
                return category.strip()
        for name in self.names:
            name = " %s "%name
            if name in sentence:
                return name.strip()
        return None

    def has_object(self, sentence):
        if self.getObject(sentence) != None:
            return True
        return False

    def getData(self, sentence):
        sentence = sentence.strip()
        sentence = " %s "%sentence
        for place in self.places:
            place = " %s "%place
            if place in sentence:
                return place.strip()
        for room in self.rooms:
            room = " %s "%room
            if room in sentence:
                return room.strip()
        for category in self.location_categories:
            category = " %s "%category
            if category in sentence:
                return category.strip()
        return None

    def has_data(self, sentence):
        if self.getData(sentence) != None:
            return True
        return False


    def getName(self, sentence):
        sentence = sentence.strip()
        sentence = " %s "%sentence
        for name in self.names:
            name = " %s "%name
            if name in sentence:
                return name.strip()
        return None

    def getPronoun(self, sentence):
        if sentence == None:
            return None
        # sentence = sentence.strip()
        # sentence += " "
        for word in ['me', 'him', 'her', 'it', 'them']:
            # word = " %s "%word
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
        if " %s "%word in [' from ', ' in ', ' at ', ' to ', ' on ']:
            return True
        return False

    def getVerb(self, sentence):
        for verb in self.verbs:
            verb = ' %s '%verb
            if verb in ' %s '%sentence:
                return verb.strip()
        return None

    def replace_verb(self, sentence):
        sentence = " %s "%sentence
        # print sentence
        for verb in	[' bring ', ' carry ', ' deliver ', ' take ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' bring ')
                # sentence = sentence.strip()
        for verb in	[' find ', ' look for ', ' locate ', ' meet ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' find ')
                # return sentence.strip()
        for verb in	[' go to ', ' navigate to ', ' reach ', ' get into ', ' navigate ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' go to ')
                # return sentence.strip()
        for verb in	[' take ', ' grasp ', ' get ', ' pick up ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' grasp ')
                # return sentence.strip()
        for verb in	[' tell ', ' say ', ' speak ']:
            # print sentence
            if verb in sentence:
                # print verb
                sentence = sentence.replace(verb, ' tell ')
                # return sentence.strip()
        for verb in [' guide ', ' escort ', ' take ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' guide ')
                # return sentence.strip()
        return sentence.strip()

    def changeVerb(self, word):
        if word in ['approach', 'drive', 'enter', 'go', 'head', 'move', 'navigate', 'point', 'get into']:
            return 'go'
        elif word in ['bring', 'carry', 'deliver', 'get', 'give', 'grab', 'grasp', 'hand', 'hold', 'pick', 'pick up', 'take', 'offer','retrieve']:
            return 'take'
        elif word in ['guide', 'escort', 'take']:
            return 'guide'
        elif word in ['announce', 'notify', 'remind', 'speak', 'tell']:
            return 'tell'
        elif word in ['leave', 'exit']:
            return 'exit'
        elif word in ['ask']:
            return 'ask'
        elif word in ['answer']:
            return 'answer'
        elif word in ['follow']:
            return 'follow'
        elif word in ['detect', 'find', 'identify', 'look for', 'meet']:
            return 'find'
        elif word in ['introduce']:
            return 'introduce'
        elif word in ['make']:
            return 'make'
        elif word in ['to']:
            return 'to'
        elif word in ['from', 'in', 'at', 'on']:
            return 'go'
        return None

    def get_object_categories(self, sentence):
        sentence = sentence.strip()
        sentence = " %s "%sentence
        for category in self.object_categories:
            category = " %s "%category
            if category in sentence:
                return category.strip()
        return None

    def get_location_categories(self, sentence):
        sentence = sentence.strip()
        sentence = " %s "%sentence
        for category in self.location_categories:
            category = " %s "%category
            if category in sentence:
                return category.strip()
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

        self.questions = readFileToList(
            roslib.packages.get_pkg_dir('speech_processing') + '/command_config/questions.txt')

        self.intransitive_verbs = readFileToList(
            roslib.packages.get_pkg_dir('main_state') + '/config/command_config/intransitive_verbs.txt')

    # Get actions from command
    def getActions(self, command):
        """
        >>> CommandExtractor().make_question(CommandExtractor().getActions("Please find the woman dressed with orange t-shirt in the office and follow them"))
        []
        """
        output = []
        for sentence in self.cut_sentence(command):
            self.extract_sentence(sentence,output)

        # print output
        self.replace_unknown_noun(output)
        # print output
        return output

    def replace_question(self, command):
        sentence = " %s " % command
        # print sentence
        for question in self.questions:
            if question in command:
                question = question
                sentence = sentence.replace(" "+ question + " ", ' <Q> ')

        return sentence.strip(), question

    def replace_question_beck(self, commands, question):

        for i in range(len(commands)):
            sentence = " %s " % commands[i]
            if ' <Q> ' in sentence:
                sentence = sentence.replace(' <Q> ', " " + question + " ")
            commands[i] = sentence.strip()
        return commands


    def cut_sentence(self, command):
        commands = []
        command = self.replace_verb(command)
        command, question = self.replace_question(command)
        # print question
        words = command.split()
        for i in xrange(0,len(words)):
            word = words[i].lower()
            if self.isVerb(word) or self.isPreposition(word):
                # print word
                startSentence = command.find(words[i])
                endSentence = -1
                for j in xrange(i+1,len(words)):
                    if self.isVerb(words[j]) or self.isPreposition(words[j].lower()):
                        endSentence = (" %s "%command).find(" %s "%words[j],startSentence + len(words[i]) - 1)
                        break
                if endSentence == -1:
                    endSentence = len(command)
                sentence = command[startSentence:endSentence]
                command = command[endSentence:]
                commands.append(sentence)
        # print commands,'=========================================='
        self.replace_question_beck(commands, question)
        return commands

    def extract_sentence(self, sentence ,output):
        # print sentence
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
        if word == 'from' or word == 'on':
            output.insert(-1,Action(self.changeVerb(word), object, data))
        elif word == 'to':
            if data != None:
                output[-1].data = data
            elif object != None:
                output[-1].data = object
        elif word == 'in' or word == 'at':
            old_data = output[-1].data
            if old_data != None and self.changeVerb(output[-1].action) == 'grasp':
                output[-1].data = None
                output.append(Action(self.changeVerb(word), object, data))
                output.append(Action('give', None, old_data))
            else:
            	# if data == None:
            		# output.insert(-1,Action('go', None, data))
                output.insert(-1,Action('go', None, data))
        else:
            output.append(Action(self.changeVerb(word), object, data))

        # print output, '7777777777777777777777777777'

    def replace_unknown_noun(self, output):
        action_with_pronoun = None
        action_with_object = None
        # print output , "000000000000000"
        for action in reversed(output):
            if self.isPronoun(action.object) and action.data != None:
                # print 111111
                action_with_pronoun = action
            elif action_with_object != None:
                # print 222222
                break
            elif self.isObject(action.object) and action.data == None:
                # print 333333
                action_with_object = action
        # print action_with_object, action_with_pronoun
        # if action_with_object != None and action_with_pronoun != None:
        #     action_with_pronoun.object = action_with_object.object
        #     output.remove(action_with_object)
        # print output, '--------=++++s'
        temp = None
        for action in output:
            if temp != None:
                if action.action == 'grasp':
                    temp.data = action.data
                    output.remove(action)
            if action.action == 'grasp':
                temp = action

        # print output, '------'

    # def count_command(self, list_action):
    #     """
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("bring a coke from bathroom to the desk"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the bedroom find a person and tell the time"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the dinner-table grasp the crackers and take them to the side-table"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("bring a coke to the person in the living room and answer him a question"))
    #     4
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the door ask the person there for her name and tell it to me"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the bedroom find the waving person and tell the time"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the kitchen find a person and follow her"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the side-table grasp the coke and take it to the dinner table"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the dinner-table grasp the banana and take it to the side-table"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("take the coke from the sink and carry it to me"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the kitchen grasp the coke and take it to the side-table"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the bathroom grasp the soap and take it to the side-table"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("grasp the coke from the small table and carry it to me"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("deliver a coke to frank in the kitchen"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("offer a coke to frank in the kitchen"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("offer a coke to the person at the door"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions("take me a coke on the desk"))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('move to show case go to desk and leave apartment'))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('navigate to kitchen table bring soda and exit apartment'))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('go to bar find coffee and take it'))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('go to reception table identify green cup and take it'))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('go to reception table go to bar and introduce yourself'))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('go to desk find frank and exit'))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('bring me a coke'))
    #     2
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('carry a cake to small table'))
    #     2
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('navigate to door'))
    #     1
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('carry a toy to small table'))
    #     2
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('go to desk find a person and exit'))
    #     3
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('bring cake to desk'))
    #     2
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('detect a person in bathroom'))
    #     2
    #     >>> CommandExtractor().count_command(CommandExtractor().getActions('find a waving person in bathroom'))
    #     2
    #     """

    #     count = 0
    #     for action in list_action:
    #         count += 1
    #         if action.action == 'grasp' and action.data != None and action.object != None:
    #             count += 1
    #     return count

    def make_question(self, list_action):
        """
        >>> CommandExtractor().make_question(CommandExtractor().getActions("pick up the pringles from the drawer deliver it to jacob in the cabinet and find mason in the tv stand"))
        [(go, bedroom, None), (grasp, None, coke), (go, bathroom, None), (give, frank, None)]
        """

        sentence = ""
        for action in list_action:
            if list_action.index(action) == len(list_action)-1 and len(list_action) > 1:
                sentence += 'and '
            if action.action == 'go':
                sentence += 'go to '
                sentence += '%s '%action.data
                sentence = sentence.strip() + ', '
            elif action.action == 'take':
                sentence += 'take '
                sentence += '%s '%action.object
                if action.data != None:
                    sentence += 'to %s '%action.data
                sentence = sentence.strip() + ', '
            elif action.action == 'find':
                sentence += 'find '
                print action
                if action.object != None and action.data != None:
                    sentence += '%s ' % action.data
                    sentence += 'in %s ' % action.object
                else:
                    sentence += '%s '%action.object
                    if action.data != None:
                        sentence += 'in %s '%action.data
                sentence = sentence.strip() + ', '
            elif action.action == 'follow':
                sentence += 'follow '
                sentence += '%s '%action.object
                if action.data != None:
                    sentence += 'to the %s '%action.data
                sentence = sentence.strip() + ', '
            elif action.action == 'tell':
                sentence += 'tell '
                sentence += '%s '%action.object
                sentence = sentence.strip() + ', '
            elif action.action == 'give':
                sentence += 'give it to %s '%action.data
                sentence = sentence.strip() + ', '
            elif action.action == 'answer':
                sentence += 'answer '
                sentence += '%s '%action.object
            elif action.action == 'guide':
                sentence += 'guide '
                sentence += "" + str(action.object) + " to " + str(action.data)
                sentence = sentence.strip() + ', '
        sentence = ' %s '%sentence[:-2]
        if sentence.count(' me ') > 0:
            sentence = sentence.replace(' me ',' you ')
        if sentence.count(' your ') > 0:
            sentence = sentence.replace(' your ',' my ')
        return "Do you want me " + sentence.strip()  + '.'

    # #Check whether command is valid or not
    # def isValidCommand(self, command):
    #     """
    #     >>> CommandExtractor().isValidCommand('')
    #     False
    #     >>> CommandExtractor().isValidCommand('snack')
    #     False
    #     >>> CommandExtractor().isValidCommand('robot yes')
    #     False
    #     >>> CommandExtractor().isValidCommand('robot no')
    #     False
    #     >>> CommandExtractor().isValidCommand('move to bar go to kitchen table and exit apartment')
    #     True
    #     >>> CommandExtractor().isValidCommand('go to fridge get soda and exit apartment')
    #     True
    #     >>> CommandExtractor().isValidCommand('bring cake go to desk and exit apartment')
    #     True
    #     >>> CommandExtractor().isValidCommand('navigate to bar introduce yourself and exit apartment')
    #     True
    #     >>> CommandExtractor().isValidCommand('bring me a cake')
    #     True
    #     >>> CommandExtractor().isValidCommand('bring a coke')
    #     True
    #     >>> CommandExtractor().isValidCommand('move to bar')
    #     True
    #     >>> CommandExtractor().isValidCommand('bring toy to desk')
    #     True
    #     >>> CommandExtractor().isValidCommand("bring a coke from bathroom to the desk")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the bedroom find a person and tell the time")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the dinner-table grasp the crackers and take them to the side-table")
    #     True
    #     >>> CommandExtractor().isValidCommand("bring a coke to the person in the living room and answer him a question")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the door ask the person there for her name and tell it to me")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the bedroom find the waving person and tell the time")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the kitchen find a person and follow her")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the side-table grasp the coke and take it to the dinner table")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the dinner-table grasp the banana and take it to the side-table")
    #     True
    #     >>> CommandExtractor().isValidCommand("take the coke from the sink and carry it to me")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the kitchen grasp the coke and take it to the side-table")
    #     True
    #     >>> CommandExtractor().isValidCommand("go to the bathroom grasp the soap and take it to the side-table")
    #     True
    #     >>> CommandExtractor().isValidCommand("grasp the coke from the small table and carry it to me")
    #     True
    #     >>> CommandExtractor().isValidCommand("deliver a coke to frank in the kitchen")
    #     True
    #     >>> CommandExtractor().isValidCommand("offer a coke to frank in the kitchen")
    #     True
    #     >>> CommandExtractor().isValidCommand("offer a coke to the person at the door")
    #     True
    #     >>> CommandExtractor().isValidCommand("take me a coke on the desk")
    #     True
    #     >>> CommandExtractor().isValidCommand('move to show case go to desk and leave apartment')
    #     True
    #     >>> CommandExtractor().isValidCommand('navigate to kitchen table bring soda and exit apartment')
    #     True
    #     >>> CommandExtractor().isValidCommand('go to bar find coffee and take it')
    #     True
    #     >>> CommandExtractor().isValidCommand('go to reception table identify green cup and take it')
    #     True
    #     >>> CommandExtractor().isValidCommand('go to reception table go to bar and introduce yourself')
    #     True
    #     >>> CommandExtractor().isValidCommand('go to desk find frank and exit')
    #     True
    #     >>> CommandExtractor().isValidCommand('bring me a coke')
    #     True
    #     >>> CommandExtractor().isValidCommand('carry a cake to small table')
    #     True
    #     >>> CommandExtractor().isValidCommand('navigate to door')
    #     True
    #     >>> CommandExtractor().isValidCommand('carry a toy to small table')
    #     True
    #     >>> CommandExtractor().isValidCommand('go to desk find a person and exit')
    #     True
    #     >>> CommandExtractor().isValidCommand('bring cake to desk')
    #     True
    #     >>> CommandExtractor().isValidCommand('detect a person in bathroom')
    #     True
    #     >>> CommandExtractor().isValidCommand('find a waving person in bathroom')
    #     True
    #     >>> CommandExtractor().isValidCommand('leave')
    #     False
    #     >>> CommandExtractor().isValidCommand('cake to desk')
    #     False
    #     >>> CommandExtractor().isValidCommand('desk')
    #     False
    #     >>> CommandExtractor().isValidCommand('to desk')
    #     False
    #     >>> CommandExtractor().isValidCommand('cake to')
    #     False
    #     """
    #     # isVerbFound = isIntransitiveVerbFound = False
    #     # isObjectFound = isObjectCategoryFound = False
    #     # isLocationFound = isLocationCategoryFound = False
    #     isVerbFound = self.has_verb(command)
    #     isObjectFound = self.has_object(command)
    #     isLocationFound = self.has_data(command)

    #     return  (isVerbFound and (isObjectFound or isLocationFound))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # a = 'take the coke from bathroom and carry it to me'
    # print CommandExtractor().getActions(a)
    # print CommandExtractor().count_command(CommandExtractor().getActions(a))
    # print CommandExtractor().isValidCommand(a)
    # print CommandExtractor().make_question(CommandExtractor().getActions(a))
    # print CommandExtractor().getActions('find a coke and take it')
    # print CommandExtractor().getActions("find a person in the bathroom and tell what time is it")
    # print CommandExtractor().getActions("go to bathroom")
    # print CommandExtractor().getActions("find a person in the bathroom and tell the name of your team")
    # print CommandExtractor().get_object_categories("bring me a fruit")
    # print CommandExtractor().getVerb("gett into bathroom")

