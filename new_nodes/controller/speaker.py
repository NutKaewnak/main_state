__author__ = "AThousandYears"

import rospy
import threading
from subprocess import call


class Speaker:
    def __init__(self):
        self.lock = threading.Lock()

    def speak(self, message):
        #if self.lock.locked():
        #    return
        #with self.lock:
            rospy.loginfo("Robot speak: " + message)
            call(["espeak", "-ven+f4", message, "-s 120"])
