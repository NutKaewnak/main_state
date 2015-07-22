__author__ = "AThousandYears"


class AbstractSubtask:
    def __init__(self, planning_module):
        self.state = 'init'
        self.last_state = None
        self.perception_module = None
        self.Devices = None
        self.skillBook = planning_module.skillBook
        self.current_skill = None
        self.subtaskBook = None
        self.current_subtask = None
        self.perception_data = None

    def reset(self):
        self.state = 'init'
        self.last_state = None

    def set_subtask_book(self, planning_module):
        self.subtaskBook = planning_module.subtaskBook

    def set_perception(self, perception_module):
        self.perception_module = perception_module
        self.Devices = perception_module.Devices

    def change_state(self, new_state):
        self.last_state = self.state
        self.state = new_state

    def act(self, perception_data):
        self.perception_data = perception_data
        if self.current_skill is not None:
            self.current_skill.act(perception_data)
        if self.current_subtask is not None:
            self.current_subtask.act(perception_data)
        self.perform(perception_data)

    def perform(self, perception_data):
        # must define your own perform
        if self.state is 'init':
            self.change_state('finish')

    def wait(self, time):
        self.perception_module.delay.set_waiting_time(time)
