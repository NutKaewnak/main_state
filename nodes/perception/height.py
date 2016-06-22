import rospy
from control_msgs.msg import FollowJointTrajectoryActionResult, FollowJointTrajectoryFeedback
from include.abstract_perception import AbstractPerception
from include.devices import Devices

__author__ = 'Nicole'


class Height(AbstractPerception):
    def __init__(self, planning_module):
        AbstractPerception.__init__(self, planning_module)
        self.height_data = HeightData()
        rospy.Subscriber('/dynamixel/torso_controller/state', 
                         FollowJointTrajectoryFeedback, self.callback_position)
        rospy.Subscriber('/dynamixel/torso_controller/follow_joint_trajectory/result',
                         FollowJointTrajectoryActionResult, self.callback_status)

    def callback_position(self, data):
        self.height_data.position = data.actual.positions[0]  # 0.02 0.2
        self.broadcast(Devices.HEIGHT, self.height_data)

    def callback_status(self, data):
        self.height_data.status = data.status.status
        self.height_data.position = data.current_pos
        self.broadcast(Devices.HEIGHT, self.height_data)


class HeightData:
    def __init__(self):
        self.position = None
        self.status = None

        # Don't forget to add this perception into perception_module
