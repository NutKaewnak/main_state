import rospy
from include.abstract_subtask import AbstractSubtask
from include.get_distance import get_distance
from subprocess import call
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float64

__author__ = 'Frank'


class FollowMe(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.count = 0
        self.goal_array = []

    def perform(self, perception_data):
        if self.state is 'init':
            self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
            self.change_state('follow_init')

        elif self.state is 'follow_init':
            if perception_data.device is self.Devices.PEOPLE:
                distance = 3.0  # set to maximum
                id = None
                for person in perception_data.input:
                    if person.personpoints.point.x < distance:
                        distance = person.personpoints.point.x
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
                    distance = get_distance(person.personpoints.point, self.follow.last_point)
                    if person.personpoints.point.x >= self.follow.last_point.x - 0.25 and distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)

            elif perception_data.device is 'VOICE' and 'go back' in perception_data.input:
                self.goal_array = self.follow.goal_array

                # TODO: erase this debug code
                print 'follow me subtask goal array'
                print self.goal_array

                self.change_state('abort')

    def start(self):
        set_pan_angle_topic = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        set_pan_angle_topic.publish(Float64(0))
        set_angle_topic = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        set_angle_topic.publish(Float64(0))
        self.change_state('init')

    def stop(self):
        set_pan_angle_topic = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
        set_pan_angle_topic.publish(Float64(0))
        set_angle_topic = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
        set_angle_topic.publish(Float64(0))
        self.change_state('wait_for_command')
