from include.abstract_skill import AbstractSkill

__author__ = 'cin'


class WebCommu(AbstractSkill):
    def __init__(self, control_module):
        AbstractSkill.__init__(self, control_module)
        # self.controlModule

    def set_info(self, status, table, order):
        self.controlModule.web_commu.set_data(status, table, order)
        self.change_state('sending')

    def perform(self, perception_data):
        if self.state is 'sending':
            self.change_state('succeeded')
