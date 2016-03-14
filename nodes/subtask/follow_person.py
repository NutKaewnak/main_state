import rospy
from include.abstract_subtask import AbstractSubtask
from math import atan, sqrt
from geometry_msgs.msg import Twist, Vector3

__author__ = 'AThousandYears'


class FollowPerson(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None
        self.move = None
        self.turn_base = None
        self.turn_neck = None
        self.last_point = Vector3()
        self.person_id = None
        self.distance_from_last = 9999.0
        self.offset_from_person = 0.4

    def set_person_id(self, person_id):
        self.person_id = person_id
        self.change_state('follow')

    def perform(self, perception_data):
        if self.state is 'init':
            self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.turn_neck = self.skillBook.get_skill(self, 'TurnNeck')
            self.turn_base = rospy.Publisher('/base/cmd_vel', Twist)
            self.turn_neck.turn(-0.1, 0.0)
            self.change_state('wait')

        elif self.state is 'follow' and perception_data.device is self.Devices.PEOPLE:
            rospy.loginfo("Track Person id %d", self.person_id)
            point = None
            for person in perception_data.input:
                if person.id == self.person_id:
                    point = person.personpoints

            if point is not None:
                theta = atan(point.y/point.x)
                self.turn_neck.turn(-0.1, theta)

                size = sqrt(point.x**2 + point.y**2)

                x = max(point.x/size*(size-self.offset_from_person), 0)
                y = max(point.y/size*(size-self.offset_from_person), 0)
                angle = Twist()
                if theta >= 0.1:
                    angle.angular.z = theta/2
                    # self.turn_base.publish(angle)
                elif theta <= -0.1:
                    angle.angular.z = theta/2

                if x >= 0.1:
                    angle.linear.x = 0.2
                    # self.turn_base.publish(angle)
                elif x <= -0.1:
                    angle.linear.x = -0.2

                print angle
                self.turn_base.publish(angle)

                # self.move.set_position(x, y, theta)
                self.distance_from_last = sqrt((point.x - self.last_point.x) ** 2 + (point.y - self.last_point.y) ** 2)
                self.last_point = point

            else:
                rospy.loginfo("Stop Robot")
                # self.skillBook.get_skill(self, 'Say').say('I cannot find you. Please come in front of me.')
                self.turn_neck.turn(-0.1, 0.0)
                self.move.stop()
                self.turn_base.publish(Twist())
                self.change_state('abort')

        elif perception_data.device is self.Devices.VOICE:
            if perception_data.input == 'robot waiting':
                self.skillBook.get_skill(self, 'Say').say('I stop.')
                self.move.stop()
                self.change_state('abort')
