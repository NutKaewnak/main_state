import rospy
import actionlib
from object_recognition_v2.msg import RecognizeObjectsGoal, RecognizeObjectsAction
from std_msgs.msg import String

__author__ = "Frank"

class RecognizeObjectsObController:
    def __init__(self):
        self.recognize_objects = actionlib.SimpleActionClient('/object/recognize_objects', RecognizeObjectsAction)

    def set_new_goal(self, object_names):
        names = []
        for name in object_names:
            names.append(String(name))
        self.recognize_objects.send_goal(RecognizeObjectsGoal(names))
