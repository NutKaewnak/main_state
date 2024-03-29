import rospy
import actionlib
from object_3d_detector.msg import Object3DsGoal, Object3DsAction
from std_msgs.msg import String

__author__ = "Frank"


class Object3dsDetectorController:
    def __init__(self):
        self.detector = actionlib.SimpleActionClient('/object/cluster_extraction', Object3DsAction)

    def set_new_goal(self):
        self.detector.send_goal(Object3DsGoal())
