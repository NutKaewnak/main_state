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

class AskForObject(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.object = None
        self.data = None
        self.name = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/COCKTAIL/objects.txt')


    def perform(self, perception_data):
        if self.state is 'init':
            self.object = None
            self.data = None
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('What would you like to drink?')
            self.change_state('waitingForName')

        elif self.state is 'waitingForName':
            if perception_data.device == 'VOICE':
                self.data = perception_data.input
                for i in self.name:
                    if i in self.data:
                        self.object = i
                        self.skill.say('You want to drink '+self.object+ 'right')

    def getObject(self):
        return self.object