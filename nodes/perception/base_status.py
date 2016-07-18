import rospy
from tf.transformations import euler_from_quaternion
from move_base_msgs.msg import MoveBaseActionResult, MoveBaseActionFeedback
from include.abstract_perception import AbstractPerception
from include.devices import Devices
from delay import Delay
import threading

__author__ = "AThousandYears"


class BaseStatusPerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/navigation/move_base/result', MoveBaseActionResult, self.callback_base_status)
        rospy.Subscriber('/navigation/move_base/feedback', MoveBaseActionFeedback, self.callback_base_position)
        self.position = None
        self.flag = False

    def callback_delay(self):
        self.broadcast(Devices.BASE_STATUS, 3)
        self.flag = False

    def callback_base_status(self, data):
        if data.status.status == 3:
            if not self.flag:
                self.flag = True
                threading.Timer(5, self.callback_delay).start()
            return
        self.broadcast(Devices.BASE_STATUS, data.status.status)

    def callback_base_position(self, data):
        position = data.feedback.base_position.pose.position
        orientation = data.feedback.base_position.pose.orientation
        quaternion = (0, 0, orientation.z, orientation.w)
        rpy_angle = euler_from_quaternion(quaternion)
        self.position = (position.x, position.y, rpy_angle[2])
