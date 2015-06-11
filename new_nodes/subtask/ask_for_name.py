__author__ = 'nicole'

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

class AskForName(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.person = None
        self.data = None
        self.name = readFileToList(roslib.packages.get_pkg_dir('speech_processing') + '/command_config/COCKTAIL/persons.txt')


    def perform(self, perception_data):
        if self.state is 'init':
            self.person = None
            self.data = None
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('Good day sir. Please tell me your name.')
            self.change_state('waitingForName')

        elif self.state is 'waitingForName':
            if perception_data.device == 'VOICE':
                self.data = perception_data.input
                for i in self.name:
                    if i in self.data:
                        self.person = i
                        self.change_state('finish')
                        self.skill.say('Your name is'+self.person)


    def getPerson(self):
        return self.person