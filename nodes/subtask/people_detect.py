from math import sqrt
from include.abstract_subtask import AbstractSubtask
from geometry_msgs.msg import Vector3
from include.delay import Delay

__author__ = 'nicole'


class PeopleDetect(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.timer = Delay()
        self.period = 30
        self.nearest_people = None
        self.is_found = False

    def perform(self, perception_data):
        if self.state is 'init':
            self.timer.wait(self.period)
            self.change_state('finding')

        elif self.state is 'finding' and perception_data.device is self.Devices.PEOPLE \
                and perception_data.input != []:
            min_distance = 4.0  # set to maximum
            point = None
            for person in perception_data.input:
                distance = sqrt(person.personpoints.x ** 2 + person.personpoints.y ** 2)
                if distance < min_distance:
                    min_distance = distance
                    point = person.personpoints

            if point is not None:
                self.nearest_people = self.get_unit_vector(point, 0.5)
                self.is_found = True
            else:
                self.is_found = False

        elif not self.timer.is_waiting():
            self.change_state('not_found')

    @staticmethod
    def get_unit_vector(point, extend_distance):
        new_point = Vector3()
        size = sqrt(point.x ** 2 + point.y ** 2)
        new_point.x, new_point.y = point.x/size, point.y/size
        new_point.x, new_point.y = new_point.x * (size-extend_distance), new_point.y * (size-extend_distance)
        return new_point

    def set_timer(self, second):
        self.period = second
        self.timer.wait(self.period)
