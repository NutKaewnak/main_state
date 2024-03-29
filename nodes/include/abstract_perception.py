import rospy

from perception_data import PerceptionData

__author__ = "AThousandYears"


class AbstractPerception:
    def __init__(self, planning_module):
        self.planningModule = planning_module
        self.current_input = None

    def broadcast(self, device, data):
        # rospy.loginfo("Receive " + str(data) + " From " + str(device))
        perception_data = PerceptionData(device, data)
        self.current_input = perception_data
        self.planningModule.perform(perception_data)
