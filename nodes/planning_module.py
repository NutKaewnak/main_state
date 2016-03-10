__author__ = "AThousandYears"

from skill.skill_book import SkillBook
from subtask.subtask_book import SubtaskBook
from task.task_book import TaskBook


class PlanningModule:

    def __init__(self, main_state):
        self.task = main_state.task
        self.perceptionModule = None

        self.skillBook = SkillBook(main_state.controlModule)
        self.subtaskBook = SubtaskBook(self)
        self.subtaskBook.set_subtask_book(self)
        self.taskBook = TaskBook(self)

    def set_perception(self, perception_module):
        self.skillBook.set_perception(perception_module)
        self.subtaskBook.set_perception(perception_module)
        self.taskBook.set_perception(perception_module)

        self.perceptionModule = perception_module

    def perform(self, perception_data):
        if self.perceptionModule is not None:
            if self.perceptionModule.delay.is_waiting():
                return

        self.taskBook.book[self.task].act(perception_data)
