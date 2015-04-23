__author__ = "AThousandYears"

from move_pass_door import MovePassDoor
from move_to_location import MoveToLocation
from register import Register
from introduce import Introduce


class SubtaskBook:
    def __init__(self, planning_module):
        self.book = dict()
        self.book['MovePassDoor'] = MovePassDoor(planning_module)
        self.book['MoveToLocation'] = MoveToLocation(planning_module)
        self.book['Introduce'] = Introduce(planning_module)
        self.book['Register'] = Register(planning_module)

    def get_subtask(self, task, subtask_name):
        self.book[subtask_name].reset()
        task.current_subtask = self.book[subtask_name]
        return self.book[subtask_name]

    def set_perception(self, perception_module):
        for subtask in self.book:
            self.book[subtask].set_perception(perception_module)

    def set_subtask_book(self, planning_module):
        for subtask in self.book:
            self.book[subtask].set_subtask_book(planning_module)