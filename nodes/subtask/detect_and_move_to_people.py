from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class DetectAndMoveToPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.target_person_name = None
        self.pos = None

    def perform(self, perception_data):
        if self.state is 'init':
            self.pos = None
            self.skillBook.get_skill(self, 'TurnNeck').turn(0, 0)
            self.subtask = self.subtaskBook.get_subtask(self, 'PeopleDetect')
            self.change_state('find_people')

        elif self.state is 'find_people':
            if self.subtask.is_found():
                if len(self.subtask.people_array) == 1:
                    self.pos = self.subtask.get_point()
                    self.change_state('found_people')

                elif len(self.subtask.people_array) > 1:
                    if self.target_person_name is not None:
                        self.change_state('call_person_to_wave_his_hand')

            elif self.subtask.state is 'not_found':
                self.skillBook.get_skill('Say').say(self, 'I can not found anyone.')
                self.change_state('not_found')

        elif self.state is 'call_person_to_wave_his_hand':
            pass

        elif self.state is 'found_people':
            if self.current_subtask.state is 'finish':
                self.subtask = self.subtaskBook.get_subtask(self, 'MoveRelative')
                self.subtask.set_position(self.pos.x, self.pos.y, self.pos.theta)
                self.change_state('move_to_found_people')

        elif self.state is 'move_to_found_people':
            if self.current_subtask.state is 'finish':
                self.change_state('finish')

    def start(self, target_person_name=None):
        self.target_person_name = target_person_name
