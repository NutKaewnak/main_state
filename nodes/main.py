#!/usr/bin/env python
__author__ = "AThousandYears"

import rospy
import sys

from control_module import ControlModule
from planning_module import PlanningModule
from perception_module import PerceptionModule


class MainState:
    def __init__(self, task="GPSR"):
        rospy.init_node(task)
        self.task = task
        self.controlModule = ControlModule()
        self.planningModule = PlanningModule(self)
        self.perceptionModule = PerceptionModule(self)
        # set reference to perception module
        self.planningModule.set_perception(self.perceptionModule)

        rospy.loginfo('initial complete')
        rospy.spin()


if __name__ == "__main__":
    print "Remove all the goddamn sound"
    if len(sys.argv) >= 2:
        MainState(sys.argv[1])
    else:
        MainState()
