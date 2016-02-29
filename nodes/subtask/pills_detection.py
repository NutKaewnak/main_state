__author__ = 'CinDy'
import rospy
from include.abstract_subtask import AbstractSubtask


class PillsDetection(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.turn_neck = self.skillBook.get_skill(self, 'TurnNeck')
        self.detect_objects = None
        self.pill_pos = None
        self.pill_name = 'object'
        self.pills_dic = {}
        self.speak = None
        self.turn_range = 0
        self.shelf_height = 60
        self.pitch_neck = 0

    def start(self):
        self.detect_objects = self.subtaskBook.get_subtask(self, 'ObjectsDetection')
        self.change_state('set_neck')

    def perform(self, perception_data):
        if self.state is 'set_neck':
            self.turn_neck.turn_relative(self, self.pitch_neck, -0.34)
            self.change_state('detecting')

        elif self.state is 'detecting':
            if self.turn_neck.state is 'successed':
                self.detect_objects.start()
                self.change_state('get_data')

        elif self.state is 'get_data':
            if self.detect_objects.state is 'finish':
                self.pill_pos = self.detect_objects.objects[0].point
                # self.pill_name = self.detect_objects.name
                self.pills_dic[self.pill_name] = self.pill_pos
                self.speak = self.subtaskBook.get_subtask(self, 'Say')
                self.speak.say(self.pill_name)
                self.change_state('speaking')

        elif self.state is 'speaking':
            if self.speak.state is 'finish':
                # turn left to right
                self.turn_neck.turn_relative(self, 0, -0.11)
                self.change_state('turn_neck')

        elif self.state is 'turn_neck':
            if self.turn_neck.state is 'successed':
                if self.turn_neck.pan < 0.34:
                    # add +y turn range
                    self.change_state('detecting')
                else:
                    self.change_state('get_next_line')

        elif self.state is 'get_next_line':
            # add +z
            self.pitch_neck -= 0.1225
            if self.pitch_neck > -0.994:
                self.change_state('set_neck')
            else:
                self.change_state('finish')


# Don't forget to add this subtask to subtask book