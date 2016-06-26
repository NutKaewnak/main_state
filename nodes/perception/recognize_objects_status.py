from object_recognition_v2.msg import RecognizeObjectsFeedback, RecognizeObjectsResult
from include.abstract_perception import AbstractPerception
from include.devices import Devices
import rospy

__author__ = "Frank"


class RecognizeObjectsPerception(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        rospy.Subscriber('/object/recognize_objects/result', RecognizeObjectsResult, self.callback_recognize_objects_status)
        rospy.Subscriber('/object/recognize_objects/feedback', RecognizeObjectsFeedback, self.callback_base_position)

    def callback_recognize_objects_status(self, data):
        header = data.header

        for obj in data.result.objects:
            obj.header = header
        self.broadcast(Devices.RECOGNIZE_OBJECTS, data)

    def callback_base_position(self, data):
        position = data.feedback.base_position.pose.position
        # orientation = data.feedback.base_position.pose.orientation
        # quaternion = (0, 0, orientation.z, orientation.w)
        # rpy_angle = euler_from_quaternion(quaternion)
        # self.position = (position.x, position.y, rpy_angle[2])
