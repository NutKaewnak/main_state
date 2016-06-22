__author__ = "AThousandYears"


class AbstractTask:
    def __init__(self, planning_module):
        self.state = 'init'
        self.last_state = None
        self.objective = None
        self.perception_module = None
        self.Devices = None
        self.subtaskBook = planning_module.subtaskBook
        self.current_subtask = None
        self.perception_data = None
        self.is_performing = False

    def reset(self):
        self.state = 'init'
        self.last_state = None

    def set_perception(self, perception_module):
        self.perception_module = perception_module
        self.Devices = perception_module.Devices

    def change_state(self, new_state):
        self.last_state = self.state
        self.state = new_state

    def change_state_with_subtask(self, new_state, new_subtask):
        if self.current_subtask is None or self.current_subtask.state is 'finish':
            self.change_state(new_state)
            return self.subtaskBook.get_subtask(self, new_subtask)

    def roll_back_state_to(self, target_state):
        self.state = target_state

    def act(self, perception_data):
        self.perception_data = perception_data
        if self.current_subtask is not None:
            self.current_subtask.act(perception_data)
        self.perform(perception_data)
        self.is_performing = False

    def perform(self, perception_data):
        # must define your own perform
        pass

    def wait(self, time):
        self.perception_module.delay.set_waiting_time(time)
