from include.abstract_task import AbstractTask

__author__ = 'cin'


class TestWebCommu(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.subtask = None
        self.table = None

    def perform(self, perception_data):
        if self.state is 'init':
            # Do something
            if perception_data.device is self.Devices.VOICE:
                if 'lamyai follow me' in perception_data.input:
                    self.subtask = self.subtaskBook.get_subtask(self, 'WebCommu')
                    self.subtask.send_info('active', '', '')

                elif 'lamyai standby mode' in perception_data.input:
                    self.subtask = self.subtaskBook.get_subtask(self, 'WebCommu')
                    self.subtask.send_info('standby', '', '')

                elif 'table a' in perception_data.input:
                    self.table = perception_data.input
                    self.change_state('order')
                

            # Don't forget to add task to task_book
            # Don't forget to create launch file
