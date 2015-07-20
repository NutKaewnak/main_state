__author__ = 'nicole'
import rospy
from include.abstract_task import AbstractTask
from include.command_extractor import CommandExtractor


class GPSR(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.command_extractor = CommandExtractor()
        self.command = None
        self.say = self.subtaskBook.get_subtask(self, 'Say')

    def perform(self, perception_data):
        rospy.loginfo('state in: ' + self.state + ' from: ' + str(perception_data.device) +
                      ' data: ' + str(perception_data.input))
        if self.state is 'init':
            self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('move_pass_door')

        elif self.state is 'move_pass_door':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('gpsr_start')  # not have yet
                self.change_state('move_to_start')

        elif self.state is 'move_to_start':
            if self.subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'Introduce')
                self.change_state('introduce')

        elif self.state is 'introduce':
            if self.subtask.state is 'finish':
                self.say.state = 'finish'
                self.change_state('wait_for_command')

        elif self.state == 'wait_for_command':
            # self.subtask = self.subtaskBook.get_subtask(self, 'ExtractCommand')  # wait for frank
            if self.say.state == 'finish' and perception_data.device is 'VOICE':
                self.command = self.command_extractor.getActions(perception_data.input)
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say(self.command_extractor.make_question(self.command) + ' Please say robot yes or robot no.')
                rospy.loginfo(perception_data.input)
                self.change_state('confirm')

        elif self.state == 'confirm':
            if self.say.state == 'finish' and perception_data.device is 'VOICE':
                if 'robot yes' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('OK, I will do it.')
                    self.change_state('action_1')
                elif 'robot no' in perception_data.input:
                    self.say = self.subtaskBook.get_subtask(self, 'Say')
                    self.say.say('Sorry, Please say again.')
                    self.change_state('wait_for_command')

        elif self.state == 'action_1':
            if self.say.state == 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                if self.command[0].object is not None:
                    self.subtask.to_location(self.command[0].data)
                    self.change_state('finish')
                elif self.command[1].object is not None:
                    self.subtask.to_location(self.command[1].data)
                    self.change_state('finish')