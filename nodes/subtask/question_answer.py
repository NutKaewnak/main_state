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
        self.debug_state = None

    def perform(self, perception_data):
        if self.debug_state != self.state:
            self.debug_state = self.state
            print self.debug_state

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
                self.say.say('Please ask the direct question ' + str(self.counter))
                self.timer.wait(15)
                self.change_state('answering')

        elif self.state is 'answering':
            if perception_data.device == 'VOICE':
                print self.timer.is_waiting()
                if self.timer.is_waiting():
                    # print "-----------"
                    if perception_data.device is 'VOICE':
                        rospy.loginfo(perception_data.input)
                        if perception_data.input is 'robot stop':
                            self.change_state('finish')
                        elif perception_data.input is not None:
                            self.say.say('The answer of the question ' + str(perception_data.input) + ' is ' +
                                         answers_the_questions.answers(perception_data.input))
                            self.timer.wait(10)
                            self.change_state("speak_answer")

                else:
                    self.counter += 1
                    self.change_state('prepare_to_answer')

        elif self.state is 'speak_answer':
            if not self.timer.is_waiting():
                self.counter += 1
                self.change_state('prepare_to_answer')
