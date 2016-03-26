import actionlib
from clothing_type_classification.msg import FindClothesGoal, FindClothesAction

__author__ = "kandithws"


class ClothesDetectorController:
    def __init__(self):
        self.controller = actionlib.SimpleActionClient('/clothes_detection_node', FindClothesAction)

    def set_new_goal(self):
        self.controller.send_goal(FindClothesGoal())
