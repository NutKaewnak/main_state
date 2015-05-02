__author__ = 'ms.antonio'

import roslib
from include.abstract_subtask import AbstractSubtask


class QuestionAnswer(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.skillBook.get_skill(self, 'Say')
        self.subtask = self.current_subtask
        self.counter = 0
        self.skill.say('ready')

    def perform(self, perception_data):
        if self.state is 'init':
            # check if skill is succeed
            if self.counter < 3:
                self.change_state('finish')
            elif perception_data.device == 'VOICE':
                print perception_data.input
                if 'your name' in perception_data.input:
                    self.skill.say('My name is Lumyai')
                    self.counter += 1
                elif ' day' in perception_data.input:
                    self.counter += 1
                    self.skill.say('Today is 2015 may 2nd')
                elif 'today' in perception_data.input or 'weather' in perception_data.input:
                    self.counter += 1
                    self.skill.say('It is sunny day')
                elif 'capital' in perception_data.input:
                    self.counter += 1
                    self.skill.say('The capital of Japan is tokyo')
                elif 'mountain' in perception_data.input or 'fuji' in perception_data.input:
                    self.counter += 1
                    self.skill.say('The height of mountain Fuji is 3776.24 meters')
                elif 'longest' in perception_data.input or 'river' in perception_data.input:
                    self.counter += 1
                    self.skill.say('The longest river in the world is the Nile in Africa with 4180 miles')
                elif 'american' in perception_data.input or 'president' in perception_data.input:
                    self.counter += 1
                    self.skill.say('Nowadays The american president is Barack Obama')
                elif 'bigger' in perception_data.input:
                    self.counter += 1
                    self.skill.say('China is bigger than japan')
                elif 'animal' in perception_data.input or 'heaviest' in perception_data.input:
                    self.counter += 1
                    self.skill.say('The heaviest land animal , in the world is , the african bush elephant')
                elif 'legs' in perception_data.input:
                    self.counter += 1
                    self.skill.say('Normally, the cow has 4 legs')

# Don't forget to add this subtask to subtask book