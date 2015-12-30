__author__ = 'krit'
import roslib
import random
from include.abstract_subtask import AbstractSubtask
import subprocess
from include.delay import Delay


class ScissorRockPaper(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.speak = self.skillBook.get_skill(self, 'Say')
        self.action = ['paper', 'rock', 'scissor']
        self.selected_action = None
        self.timer = Delay()
        self.process = None
        self.image = {'paper': roslib.packages.get_pkg_dir('main_state') + '/picture/paper.jpg',
                      'rock': roslib.packages.get_pkg_dir('main_state') + '/picture/rock.jpg',
                      'scissor': roslib.packages.get_pkg_dir('main_state') + '/picture/scissor.jpg',
                      'rps': roslib.packages.get_pkg_dir('main_state') + '/picture/RPS.png',
                      'lose': roslib.packages.get_pkg_dir('main_state') + '/picture/Lose.png',
                      'win': roslib.packages.get_pkg_dir('main_state') + '/picture/Win.png'}

    def perform(self, perception_data):
        if self.state is 'init':
            self.show_image(self.image['rps'])
            self.speak.say("Let's play rock paper scissor.")
            self.change_state('counting')
        elif self.state is 'counting':
            if self.speak.state is 'succeeded':
                self.show_image(self.image['rps'])
                self.speak = self.skillBook.get_skill(self, 'Count')
                self.speak.count_down(3)
                self.change_state('play')
        elif self.state is 'play':
            if self.speak.state is 'succeeded':
                self.speak = self.skillBook.get_skill(self, 'Say')
                self.selected_action = random.choice(self.action)
                self.show_image(self.image[self.selected_action])
                self.timer.wait(10)
                self.change_state('color_detect')
        elif self.state is 'color_detect':
            # red : rock, yellow : scissor, green : paper
            if self.timer.get_dif() >= 1 and perception_data.device is self.Devices.CIRCLE_DETECT:
                if len(perception_data.input) > 1:
                    self.speak.say("I can't understand it. Let's play again.")
                    self.change_state('counting')
                elif len(perception_data.input) == 1:
                    if self.compare_action(self.selected_action, perception_data.input[0]) == 1:
                        self.speak.say("You lose.")
                        self.show_image(self.image['lose'])
                        self.change_state('finish')
                    elif self.compare_action(self.selected_action, perception_data.input[0]) == 0:
                        self.speak.say("Draw. Let's play again.")
                        self.change_state('counting')
                    elif self.compare_action(self.selected_action, perception_data.input[0]) == -1:
                        self.speak.say("You win.")
                        self.show_image(self.image['win'])
                        self.change_state('finish')

            if not self.timer.is_waiting():
                self.speak.say("I can't understand it. Let's play again.")
                self.change_state('counting')

    def get_action_from_color(self, color):
        action_dict = {'red': 'rock', 'green': 'paper', 'yellow': 'scissor'}
        return action_dict[color]

    def compare_action(self, robot, human):
        reward = {'paper': {'paper': 0, 'rock': 1, 'scissor': -1},
                  'rock': {'paper': -1, 'rock': 0, 'scissor': 1},
                  'scissor': {'paper': 1, 'rock': -1, 'scissor': 0}}
        return reward[robot][self.get_action_from_color(human)]

    def show_image(self, picture):
        if not self.process is None:
            self.process.kill()
        self.process = subprocess.Popen(["eog", picture])