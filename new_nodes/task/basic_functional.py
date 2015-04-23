__author__ = 'nicole'
from include.abstract_task import AbstractTask


class BasicFunctional(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            self.subtask = self.change_state_with_subtask('moveToPick&Place', 'MoveToLocation')
            if self.subtask is not None:
                self.subtask.move.to_location('pick&place')

        elif self.state is 'moveToPick&Place':
            if self.subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('grab', 'Grab')
            if self.subtask is not None:
                self.subtask.grab()
                # recognize both object
                # Grab.normal().grab(self.object)

        elif self.state is 'grab':
            if self.object.isKnown is True:
                pass
                # if Grab.normal().state is STATE.SUCCESS:
                #   Grab.place().at(self.object.location)
            elif self.object.isKnown is False:
                pass
                # if Grab.normal().state is STATE.SUCCEED:
                #   Grab.place().at('bin')
            self.change_state('place')

        elif self.state is 'place':
            # if Grab.place().state is STATE.SUCCEED:
            if self.subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('10question', 'MoveToLocation')
                if self.subtask is not None:
                    self.subtask.move.to_location('Final')

        elif self.state is '10question':
            if self.subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('detect', 'SearchAndMoveToPeople')

        elif self.state is 'detect':
            # answer random question
            # if done:
             if self.subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('exit', 'MoveToLocation')
                if self.subtask is not None:
                    self.subtask.move.to_location('exit')

        elif self.state is 'exit':
            if self.subtask.state is exit:
                # say I will now stop
                self.change_state('finish')
        # Don't forget to add task to task_book
