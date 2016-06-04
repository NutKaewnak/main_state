import rospy
from include.abstract_subtask import AbstractSubtask
from include.location_information import read_location_information
from math import hypot, atan, pi, sin, cos
from geometry_msgs.msg import Pose2D
__author__ = 'CinDy'


class DetectDoor(AbstractSubtask):
    def __init__(self, planning_module):
        AbstractSubtask.__init__(self, planning_module)
        self.move = None
        self.front_door = None
        self.handle_location = None
        self.location_list = {}
        self.to_location = None
        self.arm_pose = None
        read_location_information(self.location_list)

    def perform(self, perception_data):
        if self.state is 'init':
            minimum = 999
            robot_position = self.perception_module.base_status.position
            for location_name in self.location_list:
                if 'door' in location_name:
                    door_pos = Pose2D()
                    door_pos.x = self.location_list[location_name].position.x
                    door_pos.y = self.location_list[location_name].position.y
                    door_pos.theta = self.location_list[location_name].theta

                    distance = abs(hypot(door_pos.x, door_pos.y) - hypot(robot_position[0], robot_position[1]))
                    if distance < minimum:
                        minimum = distance
                        self.to_location.x = door_pos.x
                        self.to_location.y = door_pos.y

                    if abs(atan(robot_position[0], robot_position[1]) - door_pos.theta) \
                            < abs(atan(robot_position[0], robot_position[1]) - (door_pos.theta + pi) % pi):
                        self.to_location.theta = (door_pos.theta + pi) % pi
                    else:
                        self.to_location.theta = door_pos.theta
                    self.to_location.x = round(door_pos.x - 0.6*sin(self.to_location.theta), 5)
                    self.to_location.y = round(door_pos.y - 0.6*cos(self.to_location.theta), 5)

                self.move = self.subtaskBook.get_subtask(self, 'MoveAbsolute')
                self.move.set_position(self.to_location.x, self.to_location.y, self.to_location.theta)
                self.change_state('move')

        elif self.state is 'move':
            if self.move.state is 'finish':
                self.arm_pose = self.subtaskBook.get_subtask(self, 'ArmStaticPose')
                self.arm_pose.static_pose('arm_normal')
                self.change_state('open_door')
        elif self.state is 'open_door':
            if self.arm_pose.state is 'finish':
                self.move = self.subtaskBook.get_subtask(self, 'MovePassDoor')
                self.change_state('pass_door')
        elif self.state is 'pass_door':
            if self.move.state is 'finish':
                self.change_state('finish')

