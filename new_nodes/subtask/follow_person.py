import rospy
from include.abstract_subtask import AbstractSubtask
from math import atan, sqrt
from geometry_msgs.msg import Vector3

__author__ = 'AThousandYears'


class FollowPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.move = None
        self.turn_neck = None
        self.skill = None
        self.last_point = Vector3()
        self.person_id = None
        self.distance_from_last = 9999.0

        self.offset_from_person = 0.6

    def set_person_id(self, person_id):
        self.person_id = person_id
        self.change_state('follow')

    def perform(self, perception_data):
        if self.state is 'init':
            self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.turn_neck = self.skillBook.get_skill(self, 'TurnNeck')
            self.turn_neck.turn(-0.2, 0.0)
            self.change_state('wait')

        elif self.state is 'follow' and perception_data.device is self.Devices.PEOPLE:
            rospy.loginfo("Track Person id %d", self.person_id)
            point = None
            for person in perception_data.input:
                if person.id == self.person_id:
                    point = person.personpoints
            if point is not None:
                theta = atan(point.y/point.x) 
                self.turn_neck.turn(-0.2, theta)

                size = sqrt(point.x**2 + point.y**2)
                x, y = point.x/size*(size-self.offset_from_person), point.y/size*(size-self.offset_from_person)

                self.move.set_position(x, y, theta)
                self.distance_from_last = sqrt((point.x - self.last_point.x) ** 2 + (point.y - self.last_point.y) ** 2)
                self.last_point = point

            else:
                rospy.loginfo("Stop Robot")
                self.skillBook.get_skill(self, 'Say').say('I cannot find you. Please come in front of me.')
                self.move.stop()
                self.change_state('abort')
