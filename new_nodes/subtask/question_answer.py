import rospy
from include import answers_the_questions
from include.abstract_subtask import AbstractSubtask

__author__ = 'ms.antonio'


class QuestionAnswer(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.counter = 1
        self.limit = 5

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill(self, 'TurnNeck')
            self.skill.turn(0, 0)
            self.counter = 1
            self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            if self.skill.state == 'succeeded':
                self.change_state('prepare_to_answer')

        elif self.state is 'prepare_to_answer':
            if self.skill.state is 'succeeded':
                if self.counter > self.limit:
                    self.change_state('finish')
                else:
                    self.skill = self.skillBook.get_skill(self, 'Say')
                    self.skill.say('Please ask the question')
                    self.change_state('answering')

        elif self.state is 'answering':
            if self.skill.state is 'succeeded':
                if perception_data.device is 'VOICE':
                    rospy.loginfo(perception_data.input)
                    if perception_data.input is 'robot stop':
                        self.change_state('finish')
                    elif perception_data.input is not None:
                        self.skill.say('The answer of the question ' + str(perception_data.input) + ' is ' +
                                       answers_the_questions.answers(perception_data.input))
                        self.counter += 1
                        self.change_state('prepare_to_answer')
