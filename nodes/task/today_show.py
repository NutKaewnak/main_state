from math import sqrt
import rospy
from std_msgs.msg import Float64
from include.abstract_task import AbstractTask

__author__ = 'nicole'


class TodayShow(AbstractTask):
    def __init__(self, planning_module):
        AbstractTask.__init__(self, planning_module)
        self.follow = None
        self.move = None
        self.count = 0

    def perform(self, perception_data):
        if self.state is 'init':
            set_pan_angle_topic = rospy.Publisher('/dynamixel/tilt_controller/command', Float64)
            set_pan_angle_topic.publish(Float64(0))
            set_angle_topic = rospy.Publisher('/dynamixel/pan_controller/command', Float64)
            set_angle_topic.publish(Float64(0))
            if perception_data.device is self.Devices.VOICE:
                if 'follow me' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I will follow you.')
                    self.follow = self.subtaskBook.get_subtask(self, 'FollowPerson')
                    self.change_state('follow_init')
                elif 'i will ask' in perception_data.input:
                    self.subtaskBook.get_subtask(self, 'Say').say('I prepared to answer the questions.')
                    self.change_state('answer_5_question')
                elif perception_data.device is self.Devices.VOICE and 'robot backward' in perception_data.input:
                    self.change_state('robot_backward')

        elif self.state is 'follow_init':
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
            elif perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                self.change_state('stop')
            elif perception_data.device is self.Devices.VOICE and 'robot backward' in perception_data.input:
                self.change_state('robot_backward')

        elif self.state is 'follow':
            # recovery follow
            if self.follow.state is 'abort' and perception_data.device is self.Devices.PEOPLE:
                min_distance = 0.7  # set to maximum
                id = None
                for person in perception_data.input:
                    distance = self.get_distance(person.personpoints, self.follow.last_point)
                    if person.personpoints.x >= self.follow.last_point.x - 0.25 and distance < min_distance:
                        min_distance = distance
                        id = person.id
                if id is not None:
                    self.follow.set_person_id(id)
            elif perception_data.device is self.Devices.VOICE and 'robot stop' in perception_data.input:
                self.change_state('stop')
            elif perception_data.device is self.Devices.VOICE and 'robot backward' in perception_data.input:
                self.change_state('robot_backward')

        elif self.state is 'answer_5_question':
            self.subtaskBook.get_subtask(self, 'QuestionAnswer')
            self.change_state('wait_for_question')

        elif self.state is 'wait_for_question':
            if self.current_subtask.state is 'finish':
                self.change_state('stop')

        elif self.state is 'stop':
            self.subtaskBook.get_subtask(self, 'MoveRelative').set_position(0, 0, 0)
            self.subtaskBook.get_subtask(self, 'Say').say('I Stoped.')
            self.change_state('init')

        # elif self.state is 'robot_backward':
        #     self.subtaskBook.get_subtask(self, 'MoveRelative').set_position(-1, 0, 0)
        #     self.change_state('backing')

        elif self.state is 'backing':
            if self.current_subtask.state is 'succeeded':
                self.change_state('stop')

    @staticmethod
    def get_distance(point_a, point_b):
        return sqrt((point_a.x - point_b.x)**2 + (point_a.y - point_b.y)**2)
