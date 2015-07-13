__author__ = 'Nicole'
import rospy
from include.delay import Delay
from include.abstract_subtask import AbstractSubtask


class ObjectRecognition(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.found_object = None
        self.delay = Delay()

    def perform(self, perception_data):
        if self.state is 'init':
            self.delay.wait(150)
            self.found_object = []
            # set perception lowest
            # set neck 0, -0.3
            if perception_data.device is 'OBJECT':
                if perception_data.input.status is 'no_table':
                    self.change_state('move_to_table')
                elif perception_data.input.status is 'no_object':
                    self.change_state('find_object')
                elif perception_data.input.status is 'found_object':
                    self.change_state('save_object')

        elif self.state is 'move_to_table':
            self.skill = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.skill.set_position(0.5, 0, 0)
            self.change_state('move_closer_to_shelf')

        elif self.state is 'move_closer_to_shelf':
            if self.skill.state is 'succeeded':
                if perception_data.input.status is 'no_table':
                    self.change_state('move_to_table')
                elif perception_data.input.status is 'no_object':
                    self.change_state('find_object')
                elif perception_data.input.status is 'found_object':
                    self.change_state('save_object')

            elif self.skill.state is 'aborted':
                self.skill.set_position(-0.1, 0, 0)
                if perception_data.input.status is 'no_object':
                    self.change_state('find_object')
                elif perception_data.input.status is 'found_object':
                    self.change_state('save_object')



                    # Don't forget to add this subtask to subtask book