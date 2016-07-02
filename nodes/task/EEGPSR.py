import rospy
from include.abstract_task import AbstractTask
from include.delay import Delay
from include.command_extractor import CommandExtractor
import tf

__author__ = 'Frank'

class EEGPSR(AbstractTask):

    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.start = False
        self.timer = Delay()
        self.sp = Delay()

    def perform(self, perception_data):
        # print self.state
        if self.state is 'init' and perception_data.device == self.Devices.DOOR:
            self.subtask = self.subtaskBook.get_subtask(self, 'TurnNeck')
            self.subtask.turn_absolute( 0, 0)
            self.subtask = self.subtaskBook.get_subtask(self, 'MovePassDoor')
            self.change_state('move_pass_door')

        elif self.state == 'move_pass_door' and perception_data.device == self.Devices.DOOR:
            self.subtask = self.subtaskBook.get_subtask(self, 'MoveToLocation')
            self.subtask.to_location('EEGPSR_start')
            self.change_state("moved_to_start_position")

        elif self.state == 'moved_to_start_position':
            if self.subtask.state == 'finish' and perception_data.device == self.Devices.DOOR:
                self.change_state("introduce")
            elif self.subtask.state == 'error' and perception_data.device == self.Devices.DOOR:
                self.change_state("move_pass_door")

        elif self.state == 'introduce':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say("My name is lumyai. I am ready for your command.")
                self.change_state("speak_wait_for_command")

        elif self.state == 'speak_wait_for_command' and perception_data.device == self.Devices.DOOR:
            if self.say.state == 'finish':
                self.change_state("wait_for_command")

        elif self.state == 'wait_for_command' and perception_data.device == self.Devices.VOICE:
            sentence = perception_data.input
            self.actions = CommandExtractor().getActions(sentence)
            self.say = self.subtaskBook.get_subtask(self, 'Say')
            self.say.say(CommandExtractor().make_question(self.actions).replace("-", " ") + '. Please say robot yes or robot no.')
            self.change_state("wait_for_comfirm")

        elif self.state == 'wait_for_comfirm':
            if perception_data.device == self.Devices.VOICE and perception_data.input == 'robot yes':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('My works are starting now.')
                self.change_state("check_command")

            elif perception_data.device == self.Devices.VOICE and perception_data.input == 'robot no':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say("Please say your command again.")
                self.change_state('speak_wait_for_command')

        elif self.state == 'check_command' and perception_data.device == self.Devices.DOOR:
            if self.say.state == 'finish':
                for action in self.actions:
                    if action.action == 'kill':
                        self.say = self.subtaskBook.get_subtask(self, 'Say')
                        self.say.say('Sorry, that is too cruel. I cannot kill them. I am service robot. Please say a new command.')
                        self.change_state("speak_wait_for_command")
                        return
                self.timer = Delay()
                self.timer.wait(250)
                self.start = True
                self.change_state("perform")

        elif self.state == 'perform' and perception_data.device == self.Devices.DOOR:
            if len(self.actions) == 0:
                self.change_state("finish")
            self.action = self.actions[0]
            if self.action.action == 'go':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I am going to ' + self.action.data)
                self.move_location = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location(self.action.data)
                self.actions.pop(0)
                self.change_state('perform_move')
            elif self.action.action == 'greet':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('Hello, my name is lumyai. I am belong to kasetsart university. nice to meet you.')
                self.actions.pop(0)
                self.sp.wait(3)
                self.change_state('perform_speak')
            elif self.action.action == 'tell':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say("I cannot do that. I got F in mathematics.")
                self.actions.pop(0)
                self.sp.wait(3)
                self.change_state('perform_speak')
            elif self.action.action == 'give':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say("I cannot give it to anyone. My hands are too weak.")
                self.actions.pop(0)
                self.sp.wait(3)
                self.change_state('perform_speak')
            elif self.action.action == 'find':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say("I cannot see anyone. My eyes are bind.")
                self.actions.pop(0)
                self.sp.wait(3)
                self.change_state("perform_speak")
            elif self.action.action == 'follow':
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say("I cannot follow anyone. Because I cannot found anyone.")
                self.actions.pop(0)
                self.sp.wait(3)
                self.change_state('perform_speak')

        elif self.state == 'perform_speak' and perception_data.device == self.Devices.DOOR:
            if self.say.state == 'finish' or not self.sp.is_waiting():
                self.change_state("wait_for_command")

        elif self.state == 'perform_move':
            if perception_data.device == self.Devices.DOOR:
                if self.move_location.state == 'finish':
                    self.change_state("perform")
                elif self.move_location.state == 'error':
                    self.move_location = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                    self.subtask.to_location(self.action.data)
                    self.change_state("perform")

        elif self.state == 'back_to_start' == perception_data.device == self.Devices.DOOR:
            if self.subtask.state == 'finish' and perception_data.Device == self.Devices.DOOR:
                self.change_state("perform")
            elif self.subtask.state == 'error' and perception_data.device == self.Devices.DOOR:
                self.move_location = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('EEGPSR_start')
                self.change_state('back_to_start')

        elif self.start:
            if not self.timer.is_waiting() and perception_data.device == self.Devices.DOOR:
                self.say = self.subtaskBook.get_subtask(self, 'Say')
                self.say.say('I am going back to my start position.')
                self.move_location = self.subtaskBook.get_subtask(self, 'MoveToLocation')
                self.subtask.to_location('EEGPSR_start')
                self.change_state('back_to_start')



