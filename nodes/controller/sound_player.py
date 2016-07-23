import subprocess
import os
import signal

__author__ = "cindy"


class SoundPlayer:
    def __init__(self):
        self.process = None

    def speak(self, sound):
        print sound
        self.process = subprocess.Popen('aplay ' + sound, shell=True, preexec_fn=os.setsid)

    def terminate_sound(self):
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        print 'controller kill---------------------'
        self.process = None

    def is_finish(self):
        if self.process is None:
            return False
        elif self.process.poll() != 0:
            return False
        else:
            self.process = None
            return True
