#!/usr/bin/env python
import rospy
import sys
import testByINVK

from control_module import ControlModule
from planning_module import PlanningModule
from perception_module import PerceptionModule


__author__ = "AThousandYears"


class MainState:
    def __init__(self, task="GPSR"):
        rospy.init_node(task)
        self.task = task

        self.controlModule = ControlModule()
        self.planningModule = PlanningModule(self)
        self.perceptionModule = PerceptionModule(self)
        # set reference to perception module
        self.planningModule.set_perception(self.perceptionModule)

        self.planningModule.taskBook.book['SeparateClothesOP'].testByInvk = testByINVK

        rospy.loginfo('initial complete')
        rospy.spin()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        MainState(sys.argv[1])
    else:
        MainState()
