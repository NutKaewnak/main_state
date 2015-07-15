__author__ = 'Frank'

from include.command_extractor import CommandExtractor
from include.abstract_subtask import AbstractSubtask


class ExtractLongCommand(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.data = []
        self.num_actions = 0
        self.command_extractor = CommandExtractor()

    def perform(self, perception_data):
        if self.state is 'init':
            self.data = []
            self.num_actions = 0
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('Please say command.')
            self.change_state('wait_for_command')

        elif self.state is 'wait_for_command':
            if self.skill.state is 'succeeded':
                if perception_data.device is 'VOICE':
                    sentence = perception_data.input
                    if self.command_extractor.isValidCommand(sentence):
                        self.data.append(self.command_extractor.getActions(sentence))
                        self.num_actions = self.command_extractor.count_command(self.data)
                        if self.num_actions >= 3:
                            self.change_state('confirm')

        elif self.state is 'confirm':
            self.skill.say

        elif self.state is 'wait_for_confirm':
            if perception_data.device is 'VOICE':
                if perception_data.input is 'robot yes':
                    self.change_state('finish')
                elif perception_data.input is 'robot no':
                    self.skill.say('Your is canceled.')
                    self.change_state('init')

    def confirm_command(self, data):
