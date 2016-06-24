import rospy
import tf
from include.abstract_subtask import AbstractSubtask
from math import atan, sqrt, pi, atan2
from std_msgs.msg import Header
from geometry_msgs.msg import Twist, Vector3, PoseStamped, Pose2D, PointStamped, Point
# from cob_perception_msgs.msg import PositionMeasurementArray
from tf.transformations import quaternion_from_euler
from include.transform_point import transform_point
from include.delay import Delay
from visualization_msgs.msg import *
from nav_msgs.srv import GetPlan

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
        self.path = []
        self.guess_id = None


    def set_person_id(self, person_id):
        self.person_id = person_id
        self.change_state('follow')

    def perform(self, perception_data):
        if self.state is 'init':
            self.move = self.skillBook.get_skill(self, 'MoveBaseRelative')
            self.timer = Delay()
            self.marker_pub = rospy.Publisher("/visualization_marker", Marker)

            self.change_state('wait')

        elif self.state is 'follow' and perception_data.device is self.Devices.PEOPLE_LEG:
            rospy.loginfo("Track Person id %s", self.person_id)
            position = None
            orientation = None
            for person in perception_data.input.people:
                if person.object_id == self.person_id:
                    position = person.pos
                    # orientation = person.pose.orientation

            if position is not None:
                theta = atan2(position.y, position.x)

                self.distance_from_last = sqrt(
                    (position.x - self.last_point.x) ** 2 + (position.y - self.last_point.y) ** 2)

                if position.x > 1 and not self.timer.is_waiting():
                    self.timer.wait(1)
                    size = sqrt(position.x ** 2 + position.y ** 2)

                    x = max(position.x / size * (size * 0.5), 0)
                    y = position.y / size * (size * 0.5)
                    self.move.set_position_without_clear_costmap(x, y, theta)

                self.last_point = position
                self.last_theta = theta

                box_marker = Marker()

                box_marker.header.frame_id = "/base_link"

                box_marker.type = Marker.CUBE
                box_marker.scale.x = 0.2
                box_marker.scale.y = 0.2
                box_marker.scale.z = 0.2
                box_marker.color.r = 0.0
                box_marker.color.g = 0.5
                box_marker.color.b = 0.5
                box_marker.color.a = 0.6

                box_marker.pose.position.x = position.x + 0.2
                box_marker.pose.position.y = position.y
                box_marker.pose.position.z = 0.2

                self.marker_pub.publish(box_marker)

            elif position is None:
                if not self.isLost:
                    self.isLost = True
                elif self.isLost:
                    min_distance = 99
                    self.guess_id = -1
                    for person in perception_data.input.people:
                        position = person.pos
                        # orientation = person.pose.orientation
                        distance = sqrt(
                            (position.x - self.last_point.x) ** 2 + (position.y - self.last_point.y) ** 2)
                        if distance < min_distance:
                            min_distance = distance
                            self.guess_id = person.object_id
                    if min_distance < 0.4 and self.guess_id != -1:
                        self.set_person_id(self.guess_id)
                        rospy.loginfo("Change To Person ID:" + str(self.guess_id))

        # elif perception_data.device is self.Devices.VOICE:
        #     if perception_data.input == 'stop':
        #         self.skillBook.get_skill(self, 'Say').say('I stop.')
        #         self.move.stop()
        #         self.change_state('abort')

