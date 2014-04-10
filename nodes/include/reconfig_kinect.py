#!/usr/bin/env python
import rospy
import roslib
import time
import dynamic_reconfigure.client

roslib.load_manifest('main_state')


class Reconfig:
    def __init__(self):
        try:
            self.client = dynamic_reconfigure.client.Client("camera/driver", timeout=5, config_callback=self.callback)
        except:
            rospy.loginfo("Cannot Config")
        self.depthMode = 8
        self.depth_registered = True
        self.setConfig()

    def changeDepthResolution(self, mode):
        self.depthMode = mode
        self.setConfig()

    def changeDepthRegistered(self, depth_registered):
        self.depth_registered = depth_registered
        self.setConfig()

    def callback(self, config):
        rospy.loginfo("Config {depth_mode}".format(**config))

    def setConfig(self):
        try:
            self.client.update_configuration({"depth_mode": self.depthMode, "depth_registered": self.depth_registered})
        except:
            rospy.loginfo("Cannot Config")
		
