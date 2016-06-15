import rospy
import tf
from geometry_msgs.msg import Vector3, PoseStamped, PointStamped
from include.abstract_subtask import AbstractSubtask
from include.location_information import *
from include.object_information import read_object_info
from include.get_distance import get_distance
from include.transform_point import transform_point

__author__ = "AThousandYears"


class MoveToLocation(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.location = None
        self.move = None
        self.slide = None
        self.goal = PointStamped()
        self.goal_theta = 0
        self.tf_listener = tf.TransformListener()
        self.location_list = {}
        read_location_information(self.location_list)
        self.object_info = read_object_info()

    def to_location(self, location_name):
        self.location = location_name
        rospy.loginfo('Move to '+location_name)
        location_point = self.location_list[location_name].position
        print 'type(location_point)', type(location_point)
        print 'dir(location_point)', dir(location_point)
        self.goal.header.frame_id = '/map'
        self.goal.point.x = location_point.x
        self.goal.point.y = location_point.y
        self.goal_theta = location_point.theta
        self.move = self.skillBook.get_skill(self, 'MoveBaseAbsolute')
        self.move.set_position(location_point.x, location_point.y, location_point.theta)
        self.change_state('move')

    def perform(self, perception_data):
        if self.state is 'move':
            # check if base succeed
            if self.move.state is 'succeeded':
                if get_distance(self.perception_module.base_status.position, self.goal) > 1:
                    self.change_state('move_slide_to_goal')
                    self.slide = self.skillBook.get_skill(self, 'MoveBaseRelativeTwist')
                    point = transform_point(self.tf_listener, self.goal.point, '/base_link')
                    self.slide.set_position(point.x, point.y, self.goal_theta)
                else:
                    self.change_state('finish')
            elif self.move.state is 'aborted' or self.move.state is 'preempted':
                if get_distance(self.perception_module.base_status.position, self.goal) < 1.5:
                    self.change_state('move_slide_to_goal')
                    self.slide = self.skillBook.get_skill(self, 'MoveBaseRelativeTwist')
                    point = transform_point(self.tf_listener, self.goal.point, '/base_link')
                    self.slide.set_position(point.x, point.y, self.goal_theta)
                else:
                    rospy.loginfo('Aborted')
                    self.change_state('error')

        if self.state is 'move_slide_to_goal':
            if self.slide.state is 'succeeded':
                self.change_state('finish')
