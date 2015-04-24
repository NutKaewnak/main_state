__author__ = 'nicole'
from include.abstract_task import AbstractTask


class BasicFunctional(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.subtask = self.change_state_with_subtask('moveToPickPlace', 'MoveToLocation')
            if self.subtask is not None:
                self.subtask.to_location('pickPlace')

        elif self.state is 'moveToPickPlace':
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
                    self.subtask.to_location('Final')

        elif self.state is '10question':
            if self.subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('detect', 'SearchAndMoveToPeople')

        elif self.state is 'detect':
            # answer random question
            if self.subtask.state is 'finish':
                self.subtask = self.change_state_with_subtask('exit', 'Answer several question')

        elif self.state is 'exit':
            if self.subtask.state is 'finish':
                self.subtask = None
                self.subtask = self.change_state_with_subtask('finish', 'LeaveArena')

        # Don't forget to add task to task_book