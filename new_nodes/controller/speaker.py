__author__ = "AThousandYears"

import rospy
import subprocess


class Speaker:
    def __init__(self):
        self.process = None

    def speak(self, message):
        rospy.loginfo("Robot speak: " + message)
        self.process = subprocess.Popen(["espeak", "-ven+f4", message, "-s 120"])

    def is_finish(self):
        if self.process is None:
            return False
        elif self.process.poll() != 0:
            return False
        else:
            self.process = None
            return True