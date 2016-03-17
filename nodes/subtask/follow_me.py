import rospy
from include.abstract_task import AbstractTask
from include.get_distance import get_distance
from subprocess import call
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float64

__author__ = 'Frank'

class FollowMe(AbstractSubtask):
    def __init__(self, planning_module):
        self.follow = None
        self.move = None
        self.count = 0

    def perform(self, perception_data):
        # if self.state is 'init':
        #     set_pan_angle_topic = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        #     set_pan_angle_topic.publish(Float64(0))
        #     set_angle_topic = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        #     set_angle_topic.publish(Float64(0))
        #     self.change_state('wait_for_command')

        if self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE:
                distance = 9999.0  # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.x < distance:
                        distance = person.personpoints.x
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
                    self.change_state('follow')

        elif self.state is 'follow':
            # recovery follow
            if self.follow.state is 'abort' and perception_data.device is self.Devices.PEOPLE:
                min_distance = 0.7  # set to maximum
                id = None
                for person in perception_data.input:
                    distance = get_distance(person.personpoints, self.follow.last_point)
                    if person.personpoints.x >= self.follow.last_point.x - 0.25 and distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)

    def start(self):
        set_pan_angle_topic = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        set_pan_angle_topic.publish(Float64(0))
        set_angle_topic = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        set_angle_topic.publish(Float64(0))
        self.change_state('follow_init')

    def stop(self):
        set_pan_angle_topic = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        set_pan_angle_topic.publish(Float64(0))
        set_angle_topic = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        set_angle_topic.publish(Float64(0))
        self.change_state('wait_for_command')