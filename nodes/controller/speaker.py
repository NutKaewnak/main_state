import rospy
import subprocess

__author__ = "AThousandYears"


class Speaker:
    def __init__(self):
        self.process = None
        self.temp = []

    def speak(self, message):
        rospy.loginfo("Robot speak: " + message)
        self.process = subprocess.Popen('pico2wave -w temp.wav "' + message + '" && aplay temp.wav', shell=True)
        self.temp.append(self.process)

    def is_finish(self):
        if self.process is None:
            return False
        elif self.process.poll() != 0:
            return False
        else:
            self.process = None
            return True
