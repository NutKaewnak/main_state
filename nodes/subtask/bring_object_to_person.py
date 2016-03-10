from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class BringGrabbingObjectToPerson(AbstractSubtask):
    """This subtask will bring object in hand (eg. drinks) to known operator."""
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.name = None
        self.person_location = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.name = None

        elif self.state is 'start':
            self.subtask = self.subtaskBook(self, 'MoveToLocation')
            self.subtask.to_location(self.location)
            self.change_state('move_to_person_room_location')

        elif self.state is 'move_to_person_room_location':
            if self.current_subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'DetectAndMoveToPeople')
                self.change_state('detect_and_move_to_people')
            elif self.current_subtask.state is 'aborted':
                # try 2nd way the room or report back to main state
                self.change_state('error')

        elif self.state is 'detect_and_move_to_people':
            if self.current_subtask.state is 'finish':

                self.change_state('finish')

    def start(self, name, person_location):
        self.name = name
        self.person_location = person_location
        self.change_state('start')
