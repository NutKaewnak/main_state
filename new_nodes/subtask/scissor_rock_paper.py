__author__ = 'krit'
import roslib
import random
from include.abstract_subtask import AbstractSubtask


class ScissorRockPaper(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.speak = self.skillBook.get_skill(self, 'Say')
        self.action = ['paper', 'rock', 'scissor']
        self.selected_action = None
        self.image = {'paper': roslib.packages.get_pkg_dir('main_state') + '/picture/paper.png',
                      'rock': roslib.packages.get_pkg_dir('main_state') + '/picture/rock.png',
                      'scissor': roslib.packages.get_pkg_dir('main_state') + '/picture/scissor.png'}

    def perform(self, perception_data):
        if self.state is 'init':
            self.speak.speak("Let's play rock paper scissor.")
            self.change_state('counting')
        elif self.state is 'counting':
            if self.speak.state is 'succeeded':
                self.speak = self.skillBook.get_skill(self, 'Count')
                self.speak.count(3)
                self.change_state('play')
        elif self.state is 'play':
            if self.speak.state is 'succeeded':
                self.selected_action = random.choice(self.action)
                # show image
                self.change_state('color_detect')
        elif self.state is 'color_detect':
            # red : rock, yellow : scissor, green : paper
            if perception_data.device is self.Devices.CIRCLE_DETECT:
                if len(perception_data.input) > 1:
                    self.speak.speak("I can't understand it. Let's play again.")
                    self.change_state('counting')
                else:
                    if self.compare_action(self.selected_action, perception_data.input[0]) == 1:
                        self.speak.speak("You lose.")
                        self.change_state('finish')
                    elif self.compare_action(self.selected_action, perception_data.input[0]) == 0:
                        self.speak.speak("Draw. Let's play again.")
                        self.change_state('counting')
                    elif self.compare_action(self.selected_action, perception_data.input[0]) == -1:
                        self.speak.speak("You win.")
                        self.change_state('finish')

    def get_action_from_color(self, color):
        action_dict = {'red': 'rock', 'green': 'paper', 'yellow': 'scissor'}
        return action_dict[color]

    def compare_action(self, robot, human):
        reward = {'paper': {'paper': 0, 'rock': 1, 'scissor': -1},
                  'rock': {'paper': -1, 'rock': 0, 'scissor': 1},
                  'scissor': {'paper': 1, 'rock': -1, 'scissor': 0}}
        return reward[robot][self.get_action_from_color(human)]