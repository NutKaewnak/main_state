__author__ = "AThousandYears"


class AbstractSkill:
    def __init__(self, control_module):
        self.state = 'init'
        self.last_state = None
        self.controlModule = control_module
        self.perception_module = None
        self.Devices = None
        self.perception_data = None

    def reset(self):
        self.state = 'init'
        self.last_state = None

    def set_perception(self, perception_module):
        self.perception_module = perception_module
        self.Devices = perception_module.Devices

    def act(self, perception_data):
        self.perception_data = perception_data
        self.perform(perception_data)

    def change_state(self, new_state):
        self.last_state = self.state
        self.state = new_state

    def perform(self, perception_data):
        # must define your own perform
        if self.state is 'init':
            self.state = 'succeed'

    def wait(self, time):
        self.perception_module.delay.set_waiting_time(time)
