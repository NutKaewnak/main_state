#!/usr/bin/env python
"""
Class for segment a command and generate action tuples.
Action tuples : (verb,<object>,<data>)
"""


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
        for obj in self.other_object:
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
        for verb in	[' find ', ' look for ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' find ')
                # return sentence.strip()
        for verb in	[' go to ', ' navigate to ', ' reach ', ' get into ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' go to ')
                # return sentence.strip()
        for verb in	[' take ', ' grasp ', ' get ']:
            if verb in sentence:
                sentence = sentence.replace(verb, ' take ')
                # return sentence.strip()
        for verb in	[' tell ', ' say ', ' speak ']:
            # print sentence
            if verb in sentence:
                # print verb
                sentence = sentence.replace(verb, ' tell ')
                # return sentence.strip()
        return sentence.strip()

    def changeVerb(self, word):
        if word in ['approach', 'drive', 'enter', 'go', 'head', 'move', 'navigate', 'point', 'get into']:
            return 'go'
        elif word in ['bring', 'carry', 'deliver', 'get', 'give', 'grab', 'grasp', 'hand', 'hold', 'pick', 'pick up', 'take', 'offer','retrieve']:
            return 'grasp'
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
        elif word in ['detect', 'find', 'identify', 'look for']:
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

        self.intransitive_verbs = readFileToList(
            roslib.packages.get_pkg_dir('main_state') + '/command_config/intransitive_verbs.txt')

    # Get actions from command
    def getActions(self, command):
        """
        >>> CommandExtractor().getActions("bring a coke from bathroom to the desk")
        [(go, bathroom, None), (grasp, desk, coke)]
        >>> CommandExtractor().getActions("go to the bedroom find a person and tell the time")
        [(go, bedroom, None), (find, None, person), (tell, None, time)]
        >>> CommandExtractor().getActions("go to the dinner-table grasp the crackers and take them to the side-table")
        [(go, dinner-table, None), (grasp, side-table, crackers)]
        >>> CommandExtractor().getActions("bring a coke to the person in the living room and answer him a question")
        [(grasp, None, coke), (go, living room, None), (give, person, None), (answer, him, question)]
        >>> CommandExtractor().getActions("go to the door ask the person there for her name and tell it to me")
        [(go, door, None), (ask, person, her name), (tell, me, it)]
        >>> CommandExtractor().getActions("go to the bedroom find the waving person and tell the time")
        [(go, bedroom, None), (find, None, waving person), (tell, None, time)]
        >>> CommandExtractor().getActions("go to the kitchen find a person and follow her")
        [(go, kitchen, None), (find, None, person), (follow, None, her)]
        >>> CommandExtractor().getActions("go to the side-table grasp the coke and take it to the dinner table")
        [(go, side-table, None), (grasp, dinner table, coke)]
        >>> CommandExtractor().getActions("go to the dinner-table grasp the banana and take it to the side-table")
        [(go, dinner-table, None), (grasp, side-table, banana)]
        >>> CommandExtractor().getActions("take the coke from the sink and carry it to me")
        [(go, sink, None), (grasp, me, coke)]
        >>> CommandExtractor().getActions("go to the kitchen grasp the coke and take it to the side-table")
        [(go, kitchen, None), (grasp, side-table, coke)]
        >>> CommandExtractor().getActions("go to the bathroom grasp the soap and take it to the side-table")
        [(go, bathroom, None), (grasp, side-table, soap)]
        >>> CommandExtractor().getActions("grasp the coke from the small table and carry it to me")
        [(go, small table, None), (grasp, me, coke)]
        >>> CommandExtractor().getActions("deliver a coke to frank in the kitchen")
        [(grasp, None, coke), (go, kitchen, None), (give, frank, None)]
        >>> CommandExtractor().getActions("offer a coke to frank in the kitchen")
        [(grasp, None, coke), (go, kitchen, None), (give, frank, None)]
        >>> CommandExtractor().getActions("offer a coke to the person at the door")
        [(grasp, None, coke), (go, door, None), (give, person, None)]
        >>> CommandExtractor().getActions("take me a coke on the desk")
        [(go, desk, None), (grasp, me, coke)]
        >>> CommandExtractor().getActions('move to show case go to desk and leave apartment')
        [(go, show case, None), (go, desk, None), (exit, apartment, None)]
        >>> CommandExtractor().getActions('navigate to kitchen table bring soda and exit apartment')
        [(go, kitchen table, None), (grasp, None, soda), (exit, apartment, None)]
        >>> CommandExtractor().getActions('go to bar find coffee and take it')
        [(go, bar, None), (find, None, coffee), (grasp, None, it)]
        >>> CommandExtractor().getActions('go to reception table identify green cup and take it')
        [(go, reception table, None), (find, None, green cup), (grasp, None, it)]
        >>> CommandExtractor().getActions('go to reception table go to bar and introduce yourself')
        [(go, reception table, None), (go, bar, None), (introduce, None, yourself)]
        >>> CommandExtractor().getActions('go to desk find frank and exit')
        [(go, desk, None), (find, None, frank), (exit, None, None)]
        >>> CommandExtractor().getActions('bring me a coke')
        [(grasp, me, coke)]
        >>> CommandExtractor().getActions('carry a cake to small table')
        [(grasp, small table, cake)]
        >>> CommandExtractor().getActions('navigate to door')
        [(go, door, None)]
        >>> CommandExtractor().getActions('carry a toy to small table')
        [(grasp, small table, toy)]
        >>> CommandExtractor().getActions('go to desk find a person and exit')
        [(go, desk, None), (find, None, person), (exit, None, None)]
        >>> CommandExtractor().getActions('bring cake to desk')
        [(grasp, desk, cake)]
        >>> CommandExtractor().getActions('detect a person in bathroom')
        [(go, bathroom, None), (find, None, person)]
        >>> CommandExtractor().getActions('find a waving person in bathroom')
        [(go, bathroom, None), (find, None, waving person)]
        >>> CommandExtractor().getActions('bring a coke on small table')
        [(go, small table, None), (grasp, None, coke)]
        >>> CommandExtractor().getActions('take me a coke on small table')
        [(go, small table, None), (grasp, me, coke)]
        >>> CommandExtractor().getActions("find a person in the bathroom and answer a question")
        [(go, bathroom, None), (find, None, person), (answer, None, question)]
        >>> CommandExtractor().getActions("find a person in the bathroom and tell what day is tomorrow")
        [(go, bathroom, None), (find, None, person), (tell, None, what day is tomorrow)]
        >>> CommandExtractor().getActions("find a person in the bathroom and tell the day of the week")
        [(go, bathroom, None), (find, None, person), (tell, None, the day of the week)]
        >>> CommandExtractor().getActions("find a person in the bathroom and tell your name")
        [(go, bathroom, None), (find, None, person), (tell, None, your name)]
        >>> CommandExtractor().getActions("find a person in the bathroom and tell the name of your team")
        [(go, bathroom, None), (find, None, person), (tell, None, the name of your team)]
        >>> CommandExtractor().getActions("find a person in the bathroom and tell the name of your team")
        [(go, bathroom, None), (find, None, person), (tell, None, the name of your team)]
        >>> CommandExtractor().getActions("take a coke from bedroom and deliver it to frank in bathroom")
        [(go, bedroom, None), (grasp, None, coke), (go, bathroom, None), (give, frank, None)]
        """
        output = []
        for sentence in self.cut_sentence(command):
            self.extract_sentence(sentence,output)

        # print output
        self.replace_unknown_noun(output)
        # print output
        return output

    def cut_sentence(self, command):
        commands = []
        command = self.replace_verb(command)
        words = command.split()
        for i in xrange(0,len(words)):
            word = words[i].lower()
            if self.isVerb(word) or self.isPreposition(word):
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
                output.insert(-1,Action('go', None, data))
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
        # print action_with_object, action_with_pronoun
        if action_with_object != None and action_with_pronoun != None:
            action_with_pronoun.object = action_with_object.object
            output.remove(action_with_object)

        temp = None
        for action in output:
            if temp != None:
                if action.action == 'grasp':
                    output.remove(action)
            if action.action == 'grasp':
                temp = action

    def count_command(self, list_action):
        """
        >>> CommandExtractor().count_command(CommandExtractor().getActions("bring a coke from bathroom to the desk"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the bedroom find a person and tell the time"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the dinner-table grasp the crackers and take them to the side-table"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("bring a coke to the person in the living room and answer him a question"))
        4
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the door ask the person there for her name and tell it to me"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the bedroom find the waving person and tell the time"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the kitchen find a person and follow her"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the side-table grasp the coke and take it to the dinner table"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the dinner-table grasp the banana and take it to the side-table"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("take the coke from the sink and carry it to me"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the kitchen grasp the coke and take it to the side-table"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("go to the bathroom grasp the soap and take it to the side-table"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("grasp the coke from the small table and carry it to me"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("deliver a coke to frank in the kitchen"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("offer a coke to frank in the kitchen"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("offer a coke to the person at the door"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions("take me a coke on the desk"))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('move to show case go to desk and leave apartment'))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('navigate to kitchen table bring soda and exit apartment'))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('go to bar find coffee and take it'))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('go to reception table identify green cup and take it'))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('go to reception table go to bar and introduce yourself'))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('go to desk find frank and exit'))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('bring me a coke'))
        2
        >>> CommandExtractor().count_command(CommandExtractor().getActions('carry a cake to small table'))
        2
        >>> CommandExtractor().count_command(CommandExtractor().getActions('navigate to door'))
        1
        >>> CommandExtractor().count_command(CommandExtractor().getActions('carry a toy to small table'))
        2
        >>> CommandExtractor().count_command(CommandExtractor().getActions('go to desk find a person and exit'))
        3
        >>> CommandExtractor().count_command(CommandExtractor().getActions('bring cake to desk'))
        2
        >>> CommandExtractor().count_command(CommandExtractor().getActions('detect a person in bathroom'))
        2
        >>> CommandExtractor().count_command(CommandExtractor().getActions('find a waving person in bathroom'))
        2
        """

        count = 0
        for action in list_action:
            count += 1
            if action.action == 'grasp' and action.data != None and action.object != None:
                count += 1
        return count

    def make_question(self, list_action):
        """
        >>> CommandExtractor().make_question(CommandExtractor().getActions('find a waving person in bathroom'))
        'Do you want me go to bathroom, and find waving person.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('look for a person and follow her to bathroom'))
        'Do you want me follow person to the bathroom.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('look for a person and answer a question'))
        'Do you want me find person, and answer question.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('look for a person and say what day is today'))
        'Do you want me find person, and tell what day is today.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('take the coke from bathroom and carry it to me'))
        'Do you want me go to bathroom, and grasp coke to you.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('take the coke from bathroom and carry it to frank which is in bedroom'))
        'Do you want me go to bathroom, grasp coke, go to bedroom, and give it to frank.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('take the coke from bathroom and carry it to frank at bedroom'))
        'Do you want me go to bathroom, grasp coke, go to bedroom, and give it to frank.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('take the coke from bathroom and carry it to frank in bedroom'))
        'Do you want me go to bathroom, grasp coke, go to bedroom, and give it to frank.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('take the coke from bathroom and carry it to bedroom'))
        'Do you want me go to bathroom, and grasp coke to bedroom.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('get into bedroom and look for a coke'))
        'Do you want me go to bedroom, and find coke.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('look for a person in bathroom and answer a question'))
        'Do you want me go to bathroom, find person, and answer question.'
        >>> CommandExtractor().make_question(CommandExtractor().getActions('look for a person in bathroom and say your name'))
        'Do you want me go to bathroom, find person, and tell my name.'
        """

        sentence = ""
        for action in list_action:
            if list_action.index(action) == len(list_action)-1 and len(list_action) > 1:
                sentence += 'and '
            if action.action == 'go':
                sentence += 'go to '
                sentence += '%s '%action.data
            elif action.action == 'grasp':
                sentence += 'grasp '
                sentence += '%s '%action.object
                if action.data != None:
                    sentence += 'to %s '%action.data
            elif action.action == 'find':
                sentence += 'find '
                sentence += '%s '%action.object
                if action.data != None:
                    sentence += 'in %s '%action.data
            elif action.action == 'follow':
                sentence += 'follow '
                sentence += '%s '%action.object
                sentence += 'to the %s '%action.data
            elif action.action == 'tell':
                sentence += 'tell '
                sentence += '%s '%action.object
            elif action.action == 'give':
                sentence += 'give it to %s '%action.data
            elif action.action == 'answer':
                sentence += 'answer '
                sentence += '%s '%action.object
            sentence = sentence.strip() + ', '
        sentence = ' %s '%sentence[:-2]
        if sentence.count(' me ') > 0:
            sentence = sentence.replace(' me ',' you ')
        if sentence.count(' your ') > 0:
            sentence = sentence.replace(' your ',' my ')
        print sentence
        return "Do you want me " + sentence.strip()  + '.'


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
        >>> CommandExtractor().isValidCommand('bring cake go to desk and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('navigate to bar introduce yourself and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('bring me a cake')
        True
        >>> CommandExtractor().isValidCommand('bring a coke')
        True
        >>> CommandExtractor().isValidCommand('move to bar')
        True
        >>> CommandExtractor().isValidCommand('bring toy to desk')
        True
        >>> CommandExtractor().isValidCommand("bring a coke from bathroom to the desk")
        True
        >>> CommandExtractor().isValidCommand("go to the bedroom find a person and tell the time")
        True
        >>> CommandExtractor().isValidCommand("go to the dinner-table grasp the crackers and take them to the side-table")
        True
        >>> CommandExtractor().isValidCommand("bring a coke to the person in the living room and answer him a question")
        True
        >>> CommandExtractor().isValidCommand("go to the door ask the person there for her name and tell it to me")
        True
        >>> CommandExtractor().isValidCommand("go to the bedroom find the waving person and tell the time")
        True
        >>> CommandExtractor().isValidCommand("go to the kitchen find a person and follow her")
        True
        >>> CommandExtractor().isValidCommand("go to the side-table grasp the coke and take it to the dinner table")
        True
        >>> CommandExtractor().isValidCommand("go to the dinner-table grasp the banana and take it to the side-table")
        True
        >>> CommandExtractor().isValidCommand("take the coke from the sink and carry it to me")
        True
        >>> CommandExtractor().isValidCommand("go to the kitchen grasp the coke and take it to the side-table")
        True
        >>> CommandExtractor().isValidCommand("go to the bathroom grasp the soap and take it to the side-table")
        True
        >>> CommandExtractor().isValidCommand("grasp the coke from the small table and carry it to me")
        True
        >>> CommandExtractor().isValidCommand("deliver a coke to frank in the kitchen")
        True
        >>> CommandExtractor().isValidCommand("offer a coke to frank in the kitchen")
        True
        >>> CommandExtractor().isValidCommand("offer a coke to the person at the door")
        True
        >>> CommandExtractor().isValidCommand("take me a coke on the desk")
        True
        >>> CommandExtractor().isValidCommand('move to show case go to desk and leave apartment')
        True
        >>> CommandExtractor().isValidCommand('navigate to kitchen table bring soda and exit apartment')
        True
        >>> CommandExtractor().isValidCommand('go to bar find coffee and take it')
        True
        >>> CommandExtractor().isValidCommand('go to reception table identify green cup and take it')
        True
        >>> CommandExtractor().isValidCommand('go to reception table go to bar and introduce yourself')
        True
        >>> CommandExtractor().isValidCommand('go to desk find frank and exit')
        True
        >>> CommandExtractor().isValidCommand('bring me a coke')
        True
        >>> CommandExtractor().isValidCommand('carry a cake to small table')
        True
        >>> CommandExtractor().isValidCommand('navigate to door')
        True
        >>> CommandExtractor().isValidCommand('carry a toy to small table')
        True
        >>> CommandExtractor().isValidCommand('go to desk find a person and exit')
        True
        >>> CommandExtractor().isValidCommand('bring cake to desk')
        True
        >>> CommandExtractor().isValidCommand('detect a person in bathroom')
        True
        >>> CommandExtractor().isValidCommand('find a waving person in bathroom')
        True
        >>> CommandExtractor().isValidCommand('leave')
        False
        >>> CommandExtractor().isValidCommand('cake to desk')
        False
        >>> CommandExtractor().isValidCommand('desk')
        False
        >>> CommandExtractor().isValidCommand('to desk')
        False
        >>> CommandExtractor().isValidCommand('cake to')
        False
        """
        # isVerbFound = isIntransitiveVerbFound = False
        # isObjectFound = isObjectCategoryFound = False
        # isLocationFound = isLocationCategoryFound = False
        isVerbFound = self.has_verb(command)
        isObjectFound = self.has_object(command)
        isLocationFound = self.has_data(command)

        return  (isVerbFound and (isObjectFound or isLocationFound))


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

