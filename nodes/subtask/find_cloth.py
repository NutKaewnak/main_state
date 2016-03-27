import rospy
from include.abstract_subtask import AbstractSubtask
from clothing_type_classification.msg import Clothes

__author__ = 'nicole'


class FindCloth(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None
        self.detected_clothes = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.skill = self.skillBook.get_skill('DetectClothes')
            self.trials = 1
            self.change_state('try_to_detect')

        elif self.state is 'try_to_detect':
            if self.trials == 3:
                self.change_state('not_found')
            self.skill.detect()
            self.change_state('wait_for_input')

        elif self.state is 'wait_for_input':
            if self.skill.state is 'succeeded':
                self.detected_clothes = self.skill.detected_clothes
                self.change_state('finish')
            elif self.skill.state is 'not_found':
                self.change_state('try_to_detect')
                self.trials += 1

    def get_description_string(self):
        if not self.detected_clothes:
            return 'I can\'t find any cloth left.'
        else:
            white = 0
            non_white = 0
            unknown = 0
            for i in self.detected_clothes:
                i = Clothes(i)
                if i.type == 1:
                    if i.color == 2:
                        white += 1
                    elif i.color == 3:
                        non_white += 1
                    elif i.color == 4:
                        unknown += 1

            return 'From clothes in front of me, I found ' + str(white) + ' white clothes and, '\
                   + str(non_white) + ' coloured clothes, '