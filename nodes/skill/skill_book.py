from move_base_absolute import MoveBaseAbsolute
from move_base_relative import MoveBaseRelative
from rips_out import RipsOut
from say import Say
from confirm import Confirm
from turn_neck import TurnNeck
from pick import Pick
from set_height_relative import SetHeightRelative
from count import Count
from grasp import Grasp
from recognize_objects import RecognizeObjects

__author__ = "AThousandYears"


class SkillBook:
    def __init__(self, control_module):
        self.book = dict()
        self.book['MoveBaseAbsolute'] = MoveBaseAbsolute(control_module)
        self.book['MoveBaseRelative'] = MoveBaseRelative(control_module)
        self.book['RipsOut'] = RipsOut(control_module)
        self.book['Say'] = Say(control_module)
        self.book['Confirm'] = Confirm(control_module)
        self.book['TurnNeck'] = TurnNeck(control_module)
        self.book['Pick'] = Pick(control_module)
        self.book['SetHeightRelative'] = SetHeightRelative(control_module)
        self.book['Count'] = Count(control_module)
        self.book['Grasp'] = Grasp(control_module)
        self.book['RecognizeObjects'] = RecognizeObjects(control_module)

    def get_skill(self, subtask, skill_name):
        self.book[skill_name].reset()
        subtask.current_skill = self.book[skill_name]
        return self.book[skill_name]

    def set_perception(self, perception_module):
        for skill in self.book:
            self.book[skill].set_perception(perception_module)