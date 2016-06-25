import rospy
from include import answers_the_questions
from include.abstract_subtask import AbstractSubtask
from math import hypot, radians
from include.delay import Delay
import threading
import time

__author__ = 'ms.antonio'


class QuestionAnswer(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.counter = 1
        self.limit = 5
        self.question = None
        self.timer = Delay()
        self.countTime = 15

    def perform(self, perception_data):
        if self.state is 'init':
            # self.move_base = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.say = self.skillBook.get_skill(self, 'Say')
            self.skill.turn(0, 0)
            self.counter = 1
            self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            self.change_state('prepare_to_answer')

        elif self.state is 'prepare_to_answer':
            if self.counter > self.limit:
                self.change_state('finish')
            else:
                self.say.say('Please ask the question')
                self.startTime = time.time()
                self.elapsedTime = self.startTime - time.time()
                self.change_state('answering')

        elif self.state is 'answering':
            if self.say.state is 'succeeded':
                print self.elapsedTime
                while self.elapsedTime < 15:
                    self.elapsedTime = self.startTime - time.time()
                    if perception_data.device is 'VOICE':
                        rospy.loginfo(perception_data.input)
                        if perception_data.input is 'robot stop':
                            self.change_state('finish')
                        elif perception_data.input is not None:
                            self.skill.say('The answer of the question ' + str(perception_data.input) + ' is ' +
                                           answers_the_questions.answers(perception_data.input))
                            self.counter += 1
                            self.change_state('prepare_to_answer')
                if perception_data.input == None:
                    self.counter += 1
                    self.change_state('prepare_to_answer')
