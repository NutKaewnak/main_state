import rospy
import tf
from include.abstract_subtask import AbstractSubtask
from math import atan, sqrt, pi
from geometry_msgs.msg import Twist, Vector3, PoseStamped, Pose2D, PointStamped
from tf.transformations import quaternion_from_euler
from include.transform_point import transform_point
from include.delay import Delay

__author__ = 'Frank Tower'


class FollowLeg(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.skill = None
        self.move = None
        self.last_point = Vector3()
        self.person_id = None
        self.distance_from_last = 9999.0
        self.offset_from_person = 0.3
        self.tf_listener = tf.TransformListener()
        self.isLost = False
        self.last_theta = 0

    def set_person_id(self, person_id):
        self.person_id = person_id
        self.change_state('follow')

    def perform(self, perception_data):
        if self.state is 'init':
            self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.turn_neck = self.skillBook.get_skill(self, 'TurnNeck')
            self.timer = Delay()
            self.change_state('wait')

        elif self.state is 'follow' and perception_data.device is self.Devices.PEOPLE_LEG:
            rospy.loginfo("Track Person id %d", self.person_id)
            position = None
            orientation = None
            print self.state
            for person in perception_data.input.people:
                if person.id == self.person_id:
                    position = person.pose.position
                    orientation = person.pose.orientation

            if position is not None:
                theta = atan(position.y/position.x)
                # self.move.set_position(position.x/2, position.y/2, theta)

                self.distance_from_last = sqrt(
                    (position.x - self.last_point.x) ** 2 + (position.y - self.last_point.y) ** 2)
                print theta, self.distance_from_last
                if theta > 0.4 and not self.timer.is_waiting():
                    self.move.set_position(0, 0, 0.4)
                    self.last_theta = theta
                    self.timer.wait(1)
                elif theta < -0.4 and not self.timer.is_waiting():
                    self.move.set_position(0, 0, -0.4)
                    self.last_theta = theta
                    self.timer.wait(1)
                elif self.distance_from_last > 0.4 and not self.timer.is_waiting() and position.x > 0.4:
                    self.timer.wait(1)
                    self.move.set_position(min(position.x - 0.4, 0.6), position.y, theta)
                # position_map = self.tf_listener.transformPoint('map', PointStamped(header=perception_data.input.header, point=position))

                # distance = sqrt(
                #     (position.x - self.last_point.x) ** 2 + (position.y - self.last_point.y) ** 2)

                # self.distance_from_last = sqrt(
                #     (position.x - self.last_point.x) ** 2 + (position.y - self.last_point.y) ** 2)
                    self.last_point = position
                    self.last_theta = theta
                print self.last_point
            elif position is None:
                # print self.move.state
                if not self.isLost:
                    self.move.set_position(self.last_point.x - 0.5, self.last_point.y, self.last_theta)
                    self.isLost = True
                    print "Lost: ", self.isLost
                elif self.isLost:
                    min_distance = 99
                    guess_id = -1
                    for person in perception_data.input.people:
                        # if person.id == self.person_id:
                        position = person.pose.position
                        orientation = person.pose.orientation

                        # position_map = self.tf_listener.transformPoint('map',
                        #                                                PointStamped(header=perception_data.input.header,
                        #                                                             point=position))

                        distance = sqrt(
                            (position.x - self.last_point.x) ** 2 + (position.y - self.last_point.y) ** 2)
                        if distance < min_distance:
                            min_distance = distance
                            guess_id = person.id

                        print guess_id, distance

                    if min_distance < 0.6 and guess_id != -1:
                        self.set_person_id(guess_id)
                        rospy.loginfo("Change To Person ID:" + str(guess_id))

            # else:
            #     rospy.loginfo("Stop Robot")
                # self.skillBook.get_skill(self, 'Say').say('I cannot find you. Please come in front of me.')
                # self.turn_neck.turn(0, 0)
                # self.move.stop()
                # self.change_state('abort')

        elif perception_data.device is self.Devices.VOICE:
            if perception_data.input == 'stop':
                self.skillBook.get_skill(self, 'Say').say('I stop.')
                self.move.stop()
                self.change_state('abort')
