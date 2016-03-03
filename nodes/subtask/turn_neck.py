from include.abstract_subtask import AbstractSubtask

__author__ = 'nicole'


class TurnNeck(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill

    def perform(self, perception_data):
        if self.state is 'init':
            self.change_state('wait_for_command')

        elif self.state is 'receive_command':
            if self.skill.state is 'succeed':
                self.change_state('finish')
            elif self.skill.state is 'aborted':
                self.change_state('error')

    def turn(self, pitch, yaw):
        self.skill = self.skillBook.get_skill(self, 'TurnNeck')
        self.skill.turn(pitch, yaw)
        self.change_state('receive_command')
