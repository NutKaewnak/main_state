__author__ = 'nicole'

from math import sqrt
from include.abstract_subtask import AbstractSubtask
from geometry_msgs.msg import Vector3


class FindPeople(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = self.current_skill
        self.subtask = self.current_subtask
        self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')

        self.nearest_people = None

    def perform(self, perception_data):
        if self.state is 'init' and perception_data.device is self.Devices.PEOPLE:
            min_distance = 4.0  # set to maximum
            point = None
            for person in perception_data.input:
                distance = sqrt(person.personpoints.x ** 2 + person.personpoints.y ** 2)
                if distance < min_distance:
                    min_distance = distance
                    point = person.personpoints

            if point is not None:
                self.nearest_people = self.getUnitVector(point, 0.5)

    def getUnitVector(self, point, extend_distance):
        new_point = Vector3()
        size = sqrt(point.x ** 2 + point.y ** 2)
        new_point.x, new_point.y = point.x/size, point.y/size
        new_point.x, new_point.y = new_point.x * (size-extend_distance), new_point.y * (size-extend_distance)
        return new_point

# Don't forget to add this subtask to subtask book
