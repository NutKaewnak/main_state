import rospy
from tf.transformations import euler_from_quaternion
from move_base_msgs.msg import MoveBaseActionResult, MoveBaseActionFeedback
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = "AThousandYears"


class BaseStatusPerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/navigation/move_base/result', MoveBaseActionResult, self.callback_base_status)
        rospy.Subscriber('/navigation/move_base/feedback', MoveBaseActionFeedback, self.callback_base_position)

        self.position = (0, 0, 0)

    def callback_base_status(self, data):
        self.broadcast(Devices.BASE_STATUS, data.status.status)

    def callback_base_position(self, data):
        position = data.feedback.base_position.pose.position
        orientation = data.feedback.base_position.pose.orientation
        quaternion = (0, 0, orientation.z, orientation.w)
        rpy_angle = euler_from_quaternion(quaternion)
        self.position = (position.x, position.y, rpy_angle[2])