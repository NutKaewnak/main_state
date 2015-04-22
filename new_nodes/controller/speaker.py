__author__ = "AThousandYears"

import rospy
from subprocess import call


class Speaker:
    def __init__(self):
        pass

    def speak(self, message):
        rospy.loginfo("Robot speak: " + message)
        call(["espeak", "-ven+f4", message, "-s 120"])
