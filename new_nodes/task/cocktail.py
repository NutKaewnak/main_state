__author__ = 'nicole'
from include.abstract_task import AbstractTask


class Cocktail(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            if self.state is 'init':
                self.change_state_with_subtask('movePassDoor', 'MovePassDoor')

        elif self.state is 'movePassDoor':
            self.subtask = self.change_state_with_subtask('gotoKitchenRoom', 'MoveToLocation')
            if self.subtask is not None:
                self.subtask.to_location('kitchen counter')

        elif self.state is 'movePassDoor':
            # self.subtask = # search for people
            pass


# Don't forget to add task to task_book