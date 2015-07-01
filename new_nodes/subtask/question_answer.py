__author__ = 'ms.antonio'

import rospy
from include import answers_the_questions
from include.abstract_subtask import AbstractSubtask


class QuestionAnswer(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.counter = 1
        self.limit = 5

    def perform(self, perception_data):
        if self.state is 'init':
            # check if skill is succeed
            self.skill = self.skillBook.get_skill(self, 'Say')
            self.skill.say('ready')
            self.counter = 1
            self.change_state('answering')

        elif self.state is 'answering':
            if self.counter > self.limit:
                self.change_state('finish')
            elif perception_data.device == 'VOICE':
                self.skill.say('Please ask question number ' + str(self.counter))
                rospy.loginfo(perception_data.input)
                answer = 'The answer of the question ' + str(perception_data.input) + 'is'
                answer += str(answers_the_questions.answers(perception_data.input))
                self.skill.say(answer)
                self.counter += 1