__author__ = 'AThousandYears'
import rospy

from include.abstract_subtask import AbstractSubtask
from math import atan, sqrt
from geometry_msgs.msg import Vector3


class FollowPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')
        self.last_point = Vector3()
        self.set_neck_angle_topic = rospy.Publisher('/hardware_bridge/set_neck_angle', Vector3)
        self.person_id = None
        self.distance_from_last = 9999.0

    def set_person_id(self, person_id):
        self.person_id = person_id
        self.change_state('follow')

    def perform(self, perception_data):
        if self.state is 'follow' and perception_data.device is self.Devices.PEOPLE:
            rospy.loginfo("Track Person id %d", self.person_id)
            point = None
            for person in perception_data.input:
                if person.id == self.person_id:
                    point = person.personpoints
            if point is not None:
                theta = atan(point.y/point.x) 
                size = sqrt(point.x**2 + point.y**2)
                x, y = point.x/size*(size-0.6), point.y/size*(size-0.6)
                neck_ang = Vector3()
                neck_ang.x = -0.0
                neck_ang.z = theta
                self.set_neck_angle_topic.publish(neck_ang)
                self.move.set_position(x, y, theta)
                self.distance_from_last = sqrt((point.x - self.last_point.x) ** 2 + (point.y - self.last_point.y) ** 2)
                self.last_point = point
            else:
                rospy.loginfo("Stop Robot")
                self.change_state('abort')
                self.move.stop()
