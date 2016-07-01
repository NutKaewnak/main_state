import rospy
from include import answers_the_questions_Ger2016
from include.abstract_subtask import AbstractSubtask
from math import hypot, radians
from include.delay import Delay
import threading
import time
from std_srvs.srv import *

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

        if not perception_data.device in ["VOICE", "DOOR"]:
            return

        if self.debug_state != self.state:
            self.debug_state = self.state
            print self.debug_state, '======================'

        if self.state is 'init':
            print 'before service'
            rospy.wait_for_service('/recognizer_grammar/mic_control_open')
            rospy.wait_for_service('/recognizer_grammar/mic_control_close')
            print 'finish wait service'
            self.mic_control_open = rospy.ServiceProxy("/recognizer_grammar/mic_control_open", Empty)
            self.mic_control_close = rospy.ServiceProxy("/recognizer_grammar/mic_control_close", Empty)
            print 'ServiceProxy'
            # self.move_base = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.mic_control_close()
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.say = self.skillBook.get_skill(self, 'Say')
            self.skill.turn(-0.2, -0.1)
            self.counter = 1
            self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            self.change_state('prepare_to_answer')

        elif self.state is 'prepare_to_answer':
            print 'prepare ============================ ans'
            if self.counter > self.limit:
                self.change_state('finish')
            else:
                self.mic_control_close()
                self.say = self.skillBook.get_skill(self, 'Say')
                self.say.say('Please ask the direct question ' + str(self.counter))
                self.timer.wait(10)
                self.change_state('answering_open_mic')

        elif self.state is 'answering_open_mic':
            if self.say.state == 'succeeded':
                self.mic_control_open()
                self.change_state("answering")

        elif self.state is 'answering':
            if self.timer.is_waiting():
                # print "-----------"
                if perception_data.device is 'VOICE':
                    rospy.loginfo(perception_data.input)
                    if perception_data.input is not None:
                        self.mic_control_close()
                        self.say.say('The answer of the question ' + str(perception_data.input) + ' is ' +
                                     answers_the_questions_Ger2016.answers(perception_data.input))
                        self.timer.wait(10)
                        self.change_state("speak_answer")

            else:
                self.counter += 1
                self.change_state('prepare_to_answer')

        elif self.state is 'speak_answer':
            # if not self.timer.is_waiting():
            if self.say.state == 'succeeded':
                self.counter += 1
                self.change_state('prepare_to_answer')
