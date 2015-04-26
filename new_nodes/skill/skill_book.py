__author__ = "AThousandYears"

from move_base_absolute import MoveBaseAbsolute
from move_base_relative import MoveBaseRelative
from rips_out import RipsOut
from say import Say
from detect_people_with_gesture import DetectPeopleWithGesture


class SkillBook:
    def __init__(self, control_module):
        self.book = dict()
        self.book['MoveBaseAbsolute'] = MoveBaseAbsolute(control_module)
        self.book['MoveBaseRelative'] = MoveBaseRelative(control_module)
        self.book['RipsOut'] = RipsOut(control_module)
        self.book['Say'] = Say(control_module)
        self.book['DetectPeopleWithGesture'] = DetectPeopleWithGesture(control_module)

    def get_skill(self, subtask, skill_name):
        self.book[skill_name].reset()
        subtask.current_skill = self.book[skill_name]
        return self.book[skill_name]

    def set_perception(self, perception_module):
        for skill in self.book:
            self.book[skill].set_perception(perception_module)