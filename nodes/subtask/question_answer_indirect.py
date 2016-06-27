import rospy
from include import answers_the_questions
from include.abstract_subtask import AbstractSubtask
from math import hypot, radians
from include.delay import Delay
import threading

__author__ = 'ms.antonio'


class QuestionAnswerIndirect(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.move_base = None
        self.counter = 1
        self.limit = 5
        # self.has_direction = False
        self.question = None
        self.timer = Delay()
        self.is_performing = False

    def perform(self, perception_data):
        if self.is_performing:
            return
        self.is_performing = True

        if self.state is 'init':
            self.move_base = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.say = self.skillBook.get_skill(self, 'Say')
            self.skill.turn(0, 0)
            self.counter = 1
            self.question = None
            self.choosen_degree = None
            self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            self.say.say('Please ask the indirect question ' + str(self.counter))
            self.timer.wait(5)
            self.change_state('speak_ready')
            # print self.skill.state
            # if self.skill.state == 'succeeded':
            #     self.change_state('prepare_to_answer')

        elif self.state is 'speak_ready':
            if not self.timer.is_waiting():
                self.change_state('prepare_to_answer')

        elif self.state is 'prepare_to_answer':
            # print 'prepare-----------------------------------------'
            # if perception_data.device is self.Devices.HARK_SOURCE_FRONT and self.has_direction is False:
            if perception_data.device is self.Devices.HARK_SOURCE_FRONT and self.question is None:
                if perception_data.input.src:
                    temp = 99
                    checker = 0
                    # self.choosen_degree = 0
                    for i in xrange(len(perception_data.input.src)):
                        x = perception_data.input.src[i].x
                        y = perception_data.input.src[i].y
                        z = perception_data.input.src[i].z
                        degree = perception_data.input.src[i].azimuth
                        distance = hypot(x, y)

                        print 'Degree', degree
                        print 'Distance', distance

                        if distance < 1.50 and degree <= 90 or degree >= -90:
                            if temp > distance:
                                temp = distance
                                self.choosen_degree = degree
                                checker = 1

                    if checker == 1:
                        print 'get direction-------------------------------'
                        print self.choosen_degree
                        # if self.question != None:
                        #     self.has_direction = True

            if perception_data.device is self.Devices.HARK_SOURCE_BACK and self.question is None:
            # if perception_data.device is self.Devices.HARK_SOURCE_BACK and self.has_direction is False:
                if perception_data.input.src:
                    temp = 99
                    checker = 0
                    # self.choosen_degree = 0
                    for i in xrange(len(perception_data.input.src)):
                        x = perception_data.input.src[i].x
                        y = perception_data.input.src[i].y
                        z = perception_data.input.src[i].z
                        degree = perception_data.input.src[i].azimuth
                        distance = hypot(x, y)

                        print 'Degree ', degree
                        print 'Distance ', distance

                        if distance < 1.50 and degree <= 90 or degree >= -90 and checker == 0:
                            if temp > distance:
                                temp = distance
                                if degree > 0:
                                    degree = -180 + degree

                                elif degree <= 0:
                                    degree = 180 + degree

                                self.choosen_degree = degree
                                checker = 1

                    if checker == 1:
                        print 'get direction-------------------------------'
                        print self.choosen_degree
                        # if self.question != None:
                        #     self.has_direction = True

            if perception_data.device is 'VOICE':
                print perception_data.device, "----------", perception_data.input
                if perception_data.input is 'robot stop':
                    self.change_state('finish')
                elif perception_data.input is not None:
                    self.question = perception_data.input
                # elif perception_data.input == 'what color is cobalt':
                #     self.question = perception_data.input

                    print 'get input voice---------------------------------------'

            # if self.has_direction is True and self.question != None:
            # if self.question is not None and self.has_direction is True:
            if self.question is not None and self.choosen_degree is not None:
                print 'change to turn----------------------------------------'
                self.change_state('turning')

        elif self.state is 'turning':
            self.move_base = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.move_base.set_position_without_clear_costmap(0, 0, radians(self.choosen_degree))
            self.timer.wait(5)
            self.change_state('finished_turning')

        elif self.state is 'finished_turning':
            if not self.timer.is_waiting():
                self.say.say('finish turning')
                self.change_state('answering')

        elif self.state is 'answering':
            print 'state', self.state
            print self.move_base.state
            # if self.say.state == 'succeeded':
            print 'Say Set========================================'
            # self.say.say('the answer of the question what color is cobalt is blue.')
            self.say = self.skillBook.get_skill(self, 'Say')
            self.say.say('The answer of the question ' + str(self.question) + ' is ' +
                         str(answers_the_questions.answers(self.question)))
            self.counter += 1
            # self.has_direction = False
            self.question = None
            self.choosen_degree = None
            self.change_state('speaking')

        elif self.state is 'speaking':
            print 'Speak========================================'
            if self.say.state == 'succeeded':
                print 'next----------------------------------'
                if self.counter < 5:
                    self.change_state('turn_neck')
                else:
                    self.change_state('finish')

        # elif self.state is 'prepare_to_answer':
        #     if self.skill.state is 'succeeded':
        #         if self.counter > self.limit:
        #             self.change_state('finish')
        #         else:
        #             self.skill = self.skillBook.get_skill(self, 'Say')
        #             self.skill.say('Please ask the question')
        #             self.change_state('answering')
        #
        # elif self.state is 'answering':
        #     if self.skill.state is 'succeeded':
        #         if perception_data.device is 'VOICE':
        #             rospy.loginfo(perception_data.input)
        #             if perception_data.input is 'robot stop':
        #                 self.change_state('finish')
        #             elif perception_data.input is not None:
        #                 self.skill.say('The answer of the question ' + str(perception_data.input) + ' is ' +
        #                                answers_the_questions.answers(perception_data.input))
        #                 self.counter += 1
        #                 self.change_state('prepare_to_answer')
        self.is_performing = False
